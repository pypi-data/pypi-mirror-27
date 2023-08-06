#!/usr/bin/env python

from troposphere import Output, Ref, Template
import troposphere.ec2 as ec2
from troposphere.ec2 import SecurityGroupRule
import boto3
import re
import os
import sys
import netaddr
import random
import string
import glob
import ConfigParser
import hashlib


class SecurityTemplate:

    def __init__(self, **kwargs):
        self.vpc_id = None
        self.data_lines = None
        self.aws_client = None
        self.aws_session = None
        self.group_name = None
        self.stack_id = None
        self.stack_name = None
        self.stage_changeset_id = None
        self.region_name = None
        self.stack_name = None
        self.diff = False
        self.statefile = '.pysec'
        self.hashfile = '.hashes'
        self.initial_rules_file = 'rules.pysec'
        self.random_identifier = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        self.troposphere = Template()
        self.templates = []
        self.parsed_map = {'groups': []}
        self.file_path = kwargs.get('input_file_path', None)
        self.folder_path = kwargs.get('folder_path', None)

        if self.file_path and self.folder_path:
            raise OSError("input_file_path and folder_path arguments are mutually exclusive")
        elif self.file_path:
            self.read_file(self.file_path)
        elif self.folder_path:
            self.file_list = self.read_folder(self.folder_path)
        else:
            pass

    def __repr__(self):
        return str(self.parsed_map)

    def get_config(self, type, section, item):
        config = ConfigParser.RawConfigParser()
        if type == 'state':
            if os.path.exists(self.statefile):
                config.read(self.statefile)
            else:
                raise EnvironmentError("Repository not initialized, .pysec file not found")
            return config.get(section, item)
        elif type == 'hash':
            if os.path.exists(self.hashfile):
                config.read(self.hashfile)
            else:
                raise EnvironmentError("Repository not initialized, .hashes file not found")
            return config.get(section, item)

    def get_hash(self, f):
        with open(f, 'r') as hf:
            md5_hash_file = hashlib.md5(hf.read()).hexdigest()
        return md5_hash_file

    def check_hashes(self):
        for f in self.file_list:
            with open(f, 'r') as hf:
                md5_hash_file = hashlib.md5(hf.read()).hexdigest()
            md5_hash_config = self.get_config('hash', 'hashes', f)
            if md5_hash_file != md5_hash_config:
                self.diff = True

    def create_hashfile(self):
        config = ConfigParser.ConfigParser()
        config.add_section('hashes')
        if not os.path.exists(self.hashfile):
            with open(self.hashfile, 'wb') as hashfile:
                config.write(hashfile)
        else:
            raise EnvironmentError("Repository already initialized, .pysec file exists in folder")

    def update_hashfile(self, file_path):
        config = ConfigParser.ConfigParser()
        with open(file_path) as f:
            md5_hash = hashlib.md5(f.read()).hexdigest()
        config.read(self.hashfile)
        config.set('hashes', file_path, md5_hash)
        if os.path.exists(self.hashfile):
            with open(self.hashfile, 'wb') as configfile:
                config.write(configfile)
        else:
            raise EnvironmentError("Repository not initialized, .pysec file not found")

    def append_statefile(self, setting, value):
        config = ConfigParser.ConfigParser()
        config.read(self.statefile)
        config.set('pysec-state', setting, value)
        if os.path.exists(self.statefile):
            with open(self.statefile, 'wb') as configfile:
                config.write(configfile)
        else:
            raise EnvironmentError("Repository not initialized, .pysec file not found")

    def create_statefile(self):
        config = ConfigParser.RawConfigParser()

        config.add_section('pysec-state')
        config.set('pysec-state', 'vpc', self.vpc_id)
        config.set('pysec-state', 'groupname', self.group_name)
        config.set('pysec-state', 'stack', self.stack_id)
        config.set('pysec-state', 'stackname', self.stack_name)
        config.set('pysec-state', 'region', self.region_name)

        if not os.path.exists(self.statefile):
            with open(self.statefile, 'wb') as configfile:
                config.write(configfile)
        else:
            raise EnvironmentError("Repository already initialized, .pysec file exists in folder")

        if not os.path.exists(self.initial_rules_file):
            open(self.initial_rules_file, 'a').close()

    def read_folder(self, folder_path):
        if os.path.isdir(folder_path):
            file_list = glob.glob(os.path.join(folder_path, '*'))
            if len(file_list) == 0:
                raise OSError("Folder path empty, you must create IP files first -> " + str(folder_path))
        else:
            raise OSError("Folder path not found or invalid -> " + str(folder_path))
        for path in file_list:
            self.read_file(path)
        return file_list

    def read_file(self, file_path):
        if os.path.isfile(file_path):
            line_list = []
            self.file_path = file_path
            with open(file_path, 'r') as f:
                for i in f.readlines():
                    line_list.append(i.rstrip('\n'))
            self.map_lines(line_list)
        else:
            raise OSError("File path not found or invalid -> " + str(file_path))

    def aws_auth(self, **kwargs):
        key = kwargs.get('aws_access_key_id', None)
        secret = kwargs.get('aws_secret_access_key', None)
        region = kwargs.get('region_name', None)
        profile_name = kwargs.get('profile_name', None)
        resource = kwargs.get('resource', None)

        if profile_name:
            self.aws_session = boto3.Session(profile_name=profile_name, region_name=region)
        else:
            self.aws_session = boto3.Session(aws_access_key_id=key, aws_secret_access_key=secret, region_name=region)

        self.aws_client = self.aws_session.client(resource)

    def get_template(self, stack_name):
        if self.aws_client:
            response = self.aws_client.get_template(StackName=stack_name)
            return response.get('TemplateBody')

    def get_log_events(self, **kwargs):
        if self.aws_client:
            response = self.aws_client.get_log_events(**kwargs)
            return response

    def create_stack(self, **kwargs):
        self.stack_name = kwargs.get('StackName', None)
        if self.aws_client:
            response = self.aws_client.create_stack(**kwargs)
            self.stack_id = response.get('StackId')
            self.append_statefile('Stack', self.stack_id)
            self.append_statefile('StackName', self.stack_name)
            print "[INFO] Creating Stack " + self.stack_id

    def delete_stack(self, stack_id):
        if self.aws_client:
            r = self.aws_client.delete_stack(StackName=stack_id)
            print "[INFO] Deleting Stack " + stack_id

    def update_stack(self, **kwargs):
        self.stack_name = kwargs.get('StackName', None)
        if self.aws_client:
            response = self.aws_client.update_stack(**kwargs)
            self.stack_id = response.get('StackId')
            print "[INFO] Updating Stack " + self.stack_id

    def delete_repo_files(self):
        if os.path.isfile(self.statefile):
            os.remove(self.statefile)
        if os.path.isfile(self.hashfile):
            os.remove(self.hashfile)

    def wait(self, stack, status):
        self.aws_client.get_waiter(status).wait(StackName=stack)

    def map_lines(self, data):
        objects = []
        ip_regex = r'[0-9]+(?:\.[0-9]+){3}'
        cidr_regex = r'(\/|\\)([0-9]|[1-2][0-9]|[3][0-2]|[0-2])($|[:^])'
        port_regex = r'(\:)([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])|($|[:\^])'
        range_regex = r'(\-)([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])|($|[:\^])'
        protocol_regex = r'(\^)(\btcp\b|\budp\b|\bicmp\b)'

        for line in data:

            if netaddr.valid_ipv4(re.findall(ip_regex, line)[0]):
                ip_address = re.findall(ip_regex, line)[0]
            else:
                raise ValueError("Invalid or no IP address provided -> " + str(line))

            if re.findall(cidr_regex, line):
                ip_cidr = re.findall(cidr_regex, line)[0][1]
            else:
                ip_cidr = '32'

            ip_cidr_notated = '/' + str(ip_cidr)

            netaddr.IPNetwork(ip_address + ip_cidr_notated)

            if re.findall(port_regex, line):
                try:
                    from_port = re.findall(port_regex, line)[0][1]
                    int(from_port)
                except (ValueError, IndexError):
                    raise ValueError("Invalid or no port provided -> " + str(line))
            else:
                raise ValueError("Invalid or no port provided -> " + str(line))

            if re.findall(range_regex, line):
                try:
                    to_port = re.findall(range_regex, line)[1][1]
                    int(to_port)
                except (ValueError, IndexError):
                    to_port = from_port
            else:
                to_port = from_port

            if from_port < to_port:
                from_port, to_port = to_port, from_port

            if re.findall(protocol_regex, line):
                try:
                    ip_protocol = re.findall(protocol_regex, line)[0][1]
                    assert ip_protocol in ['tcp', 'udp', 'icmp']
                except (AssertionError, IndexError):
                    ip_protocol = 'tcp'
            else:
                ip_protocol = 'tcp'

            object = {'ip': ip_address, 'cidr': ip_cidr, 'fromPort': from_port, 'toPort': to_port,
                      'ipProtocol': ip_protocol}
            objects.append(object)

        self.parsed_map['groups'].append(objects)

    def generate_template(self, group_name, vpc):
        if group_name:
            self.group_name = group_name
        else:
            group_name = 'Pysec' + self.random_identifier
            self.group_name = group_name

        security_group_description = 'Security group created by PySec-AWS - ' + str(group_name)
        security_group_rules = []

        if re.match(r'(\bvpc\b\-[a-zA-Z0-9]{6,})', vpc):
            self.vpc_id = vpc
        else:
            raise ValueError("VPC ID is invalid or malformed -> " + vpc)
        for group in self.parsed_map['groups']:
            for rule in group:
                ip_address_with_cidr = rule['ip'] + '/' + rule['cidr']
                security_group_rules.append(
                    SecurityGroupRule(
                        IpProtocol=rule['ipProtocol'],
                        FromPort=rule['fromPort'],
                        ToPort=rule['toPort'],
                        CidrIp=ip_address_with_cidr
                    )
                )
        security_group = self.troposphere.add_resource(ec2.SecurityGroup(
            group_name, GroupDescription=security_group_description, SecurityGroupIngress=security_group_rules,
            VpcId=vpc
        ))

        self.troposphere.add_output([
            Output(
                "SecurityGroupId",
                Description="Security Group Id",
                Value=Ref(security_group),
            )
        ])

    def to_file(self, output_file_path, format):
        with open(output_file_path, 'w') as f:
            if format == 'json':
                f.write(self.troposphere.to_json())
            elif format in ['yml', 'yaml']:
                f.write(self.troposphere.to_yaml())
        print "[INFO] CF Template flushed to disk: " + str(output_file_path)

    def to_cfdict(self):
        return self.troposphere.to_dict()

    def query_yes_no(self, question, default="yes"):
        valid = {"yes": True, "y": True, "ye": True,
                 "no": False, "n": False}
        if default is None:
            prompt = " [y/n] "
        elif default == "yes":
            prompt = " [Y/n] "
        elif default == "no":
            prompt = " [y/N] "
        else:
            raise ValueError("invalid default answer: '%s'" % default)

        while True:
            sys.stdout.write(question + prompt)
            choice = raw_input().lower()
            if default is not None and choice == '':
                return valid[default]
            elif choice in valid:
                return valid[choice]
            else:
                sys.stdout.write("Please respond with 'yes' or 'no' "
                                 "(or 'y' or 'n').\n")

