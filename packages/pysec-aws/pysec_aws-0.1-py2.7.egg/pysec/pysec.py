from troposphere import Output, Ref, Template
import troposphere.ec2 as ec2
from troposphere.ec2 import SecurityGroupRule
import re
import os
import netaddr
import random
import string


class CFConversion:

    def __init__(self, input_file_path):
        self.vpc_id = ''
        self.random_identifier = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        self.troposphere = Template()
        self.parsed_map = {'requests': []}

        if os.path.isfile(input_file_path):
            self.file_path = input_file_path
            self.data_lines = self.read_file(input_file_path)
        else:
            raise OSError("File not found or invalid ->" + str(input_file_path))

        self.map_lines()

    def __repr__(self):
        return str(self.parsed_map)

    @staticmethod
    def read_file(file_path):
        line_list = []
        with open(file_path, 'r') as f:
            for i in f.readlines():
                line_list.append(i.rstrip('\n'))
            return line_list

    def map_lines(self):
        ip_regex = r'[0-9]+(?:\.[0-9]+){3}'
        cidr_regex = r'(\/|\\)([0-9]|[1-2][0-9]|[3][0-2]|[0-2])($|[:^])'
        port_regex = r'(\:)([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])|($|[:\^])'
        range_regex = r'(\-)([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])|($|[:\^])'
        protocol_regex = r'(\^)(\btcp\b|\budp\b|\bicmp\b)'

        for line in self.data_lines:

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

            map_object = {'ip': ip_address, 'cidr': ip_cidr, 'fromPort': from_port, 'toPort': to_port,
                          'ipProtocol': ip_protocol}

            self.parsed_map['requests'].append(map_object)
        print "[INFO] File loaded successfully - " + str(len(self.data_lines)) + ' ingress rules detected'

    def generate_template(self, group_name, vpc):
        if not group_name:
            group_name = self.random_identifier

        security_group_description = 'Security group created by automated process - ' + str(group_name)
        security_group_rules = []

        if re.match(r'(\bvpc\b\-[a-zA-Z0-9]{6,})', vpc):
            self.vpc_id = vpc
        else:
            raise ValueError("VPC ID is invalid or malformed -> " + vpc)

        for r in self.parsed_map['requests']:
            ip_address_with_cidr = r['ip'] + '/' + r['cidr']
            security_group_rules.append(
                SecurityGroupRule(
                    IpProtocol=r['ipProtocol'],
                    FromPort=r['fromPort'],
                    ToPort=r['toPort'],
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
        print "[INFO] Generated Troposphere object"

    def to_file(self, output_file_path, format):
        with open(output_file_path, 'w') as f:
            if format == 'json':
                f.write(self.troposphere.to_json())
            elif format in ['yml', 'yaml']:
                f.write(self.troposphere.to_yaml())
        print "[INFO] CF Template flushed to disk: " + str(output_file_path)

