import re
import os
import json
import argparse
from tabulate import tabulate
import itertools
from pysec import SecurityTemplate


def main():
    configure()
    if args.pos == 'init':
        init_repo()
    if args.pos == 'configure':
        configure_repo()
    if args.pos == 'commit':
        commit_repo()
    if args.pos == 'destroy':
        destroy_repo()
    if args.pos == 'status':
        status_repo()
    if args.pos == 'stage':
        stage_repo()


def configure():
    global args

    parser = argparse.ArgumentParser(description='PySec-AWS CLI')
    subparsers = parser.add_subparsers(help='Initiate a new PySec repo', dest='pos')

    parser.add_argument('-u', '--use-profile', help="Use AWS Profile", action="store_true")
    parser.add_argument('-id', '--aws-access-key-id', type=str, help="AWS Credentials Key ID", action="store",
                                default=None)
    parser.add_argument('-s', '--aws-secret-access-key', type=str, help="AWS Credentials Secret", action="store",
                                default=None)
    parser.add_argument('-y', '--yes', help="Skip validation", action="store_true", default=False)

    parser_init = subparsers.add_parser('init', help='Initiate folder as PySec repo')
    parser_init.add_argument('-f', '--folder-path', type=str, help="Input File Path", action="store", default=os.getcwd())

    parser_configure = subparsers.add_parser('configure', help='Configure repository metadata')
    parser_configure.add_argument('-v', '--vpc-id', type=str, help="VPC ID for Security Group", action="store",
                               required=True)
    parser_configure.add_argument('-g', '--group-name', type=str, help="Security Group name", default=None, action="store")

    parser_configure.add_argument('-r', '--aws-region', type=str, help="AWS Region to commit to", action="store", required=True)
    parser_configure.add_argument('-p', '--aws-profile-name', type=str, help="AWS Credentials profile name", action="store",
                                  default=None)

    parser_destroy = subparsers.add_parser('destroy', help='Destroy repo and stack')
    parser_destroy.add_argument('-s', '--skip-stack', help="Skip stack removal", action="store_true", default=False)

    parser_commit = subparsers.add_parser('commit', help='Commit rules in folder to CloudFormation')
    parser_status = subparsers.add_parser('status', help='Get pysec repository status')
    parser_stage = subparsers.add_parser('stage', help='Stage a change')

    args = parser.parse_args()
    if args.use_profile and (args.aws_access_key_id or args.aws_secret_access_key):
        print "--use-profile and --aws-access-key-id/--aws-secret-access-key are mutually exclusive"
        exit(1)


def stage_repo():
    session = SecurityTemplate(folder_path=os.getcwd())
    session.generate_template(session.get_config('state', 'pysec-state', 'groupname'),
                              session.get_config('state', 'pysec-state', 'vpc'))
    cf_data = session.to_cfdict()
    if args.use_profile:
        session.aws_auth(profile_name=session.get_config('state', 'pysec-state', 'defaultprofile'),
                         region_name=session.get_config('state', 'pysec-state', 'region'))
    else:
        session.aws_auth(aws_access_key_id=args.aws_access_key_id, aws_secret_access_key=args.aws_secret_access_key,
                         region_name=session.get_config('state', 'pysec-state', 'region'))

    session.check_hashes()
    if session.diff and session.get_config('state', 'pysec-state', 'stackname') != 'None':
        table = []
        count = 0
        stack_name = session.get_config('state', 'pysec-state', 'stackname')
        group_name=session.get_config('state', 'pysec-state', 'groupname')
        running_template_resources = json.loads(session.get_template(stack_name).replace("\'", '"'))['Resources'][
            group_name]['Properties']['SecurityGroupIngress']
        proposed_template_resources = cf_data['Resources'][group_name]['Properties']['SecurityGroupIngress']
        diff = list(itertools.ifilterfalse(lambda x: x in running_template_resources, proposed_template_resources)) \
            + list(itertools.ifilterfalse(lambda x: x in proposed_template_resources, running_template_resources))
        for d in diff:
            d_pretty = "CIDR-IP: {i} FROM: {f} TO: {t} PROTOCOL: {p}".format(i=d.get('CidrIp'), f=d.get('FromPort'),
                                                                             t=d.get('ToPort'), p=d.get('IpProtocol'))
            for rule in running_template_resources:
                if d == rule:
                    action = '\x1b[6;30;41m' + '-- removal --' + '\x1b[0m'
                else:
                    action = '\x1b[6;30;42m' + '++ addition ++' + '\x1b[0m'
            count += 1
            table.append([count, d_pretty, session.group_name, action])
        print tabulate(table, headers=["#", "Suggested Change", "Security Group", "Action"])
    else:
        print "[INFO] No changes to stage."
        exit(0)


def status_repo():
    session = SecurityTemplate(folder_path=os.getcwd())
    print ''
    if session.get_config('state', 'pysec-state', 'stackname') != 'None':
        table = []
        for f in session.file_list:
            existing_hash = session.get_config('hash', 'hashes', f)
            current_hash = session.get_hash(f)
            if existing_hash != current_hash:
                existing_string = '\x1b[6;30;41m' + existing_hash + '\x1b[0m'
                current_string = '\x1b[6;30;41m' + current_hash + '\x1b[0m'
                match = False
            else:
                existing_string = '\x1b[6;30;42m' + existing_hash + '\x1b[0m'
                current_string = '\x1b[6;30;42m' + current_hash + '\x1b[0m'
                match = True
            table.append([f, existing_string, current_string, match])
        print tabulate(table, headers=["File Path", "MD5 Hash (Committed)", "MD5 Hash (Current)", "Diff?"])
    else:
        print "[INFO] Repository not committed, no status to show"
        exit(0)


def destroy_repo():
    session = SecurityTemplate(folder_path=os.getcwd())

    if args.use_profile:
        session.aws_auth(profile_name=session.get_config('state', 'pysec-state', 'defaultprofile'),
                         region_name=session.get_config('state', 'pysec-state', 'region'))
    else:
        session.aws_auth(aws_access_key_id=args.aws_access_key_id, aws_secret_access_key=args.aws_secret_access_key,
                         region_name=session.get_config('state', 'pysec-state', 'region'))
    stack_name = session.get_config('state', 'pysec-state', 'stackname')

    if not args.yes:
        answer = session.query_yes_no('Are you sure you want to destroy this stack -> ' + stack_name + '?')
        if answer:
            args.yes = True
        else:
            exit(0)
    else:
        pass
    if not args.skip_stack:
        session.delete_stack(stack_name)
        session.wait(stack_name, 'stack_delete_complete')
    session.delete_repo_files()


def init_repo():
    session = SecurityTemplate(folder_path=args.folder_path)

    try:
        session.create_statefile()
        session.create_hashfile()
    except EnvironmentError as e:
        print e
        exit(1)


def configure_repo():
    session = SecurityTemplate(folder_path=os.getcwd())
    group_name_regex = re.compile('[^a-zA-Z]')

    if args.group_name:
        group_name = group_name_regex.sub('', args.group_name)
    else:
        group_name = group_name_regex.sub('', os.path.split(args.folder_path)[1] + '-' + session.random_identifier)
    session.append_statefile('groupname', group_name)
    session.append_statefile('vpc', args.vpc_id)
    session.append_statefile('region', args.aws_region)
    print "[INFO] Updated Pysec Statefile"
    if args.aws_profile_name:
        session.append_statefile('defaultprofile', args.aws_profile_name)


def commit_repo():
    session = SecurityTemplate(folder_path=os.getcwd())
    session.generate_template(session.get_config('state', 'pysec-state', 'groupname'),
                              session.get_config('state', 'pysec-state', 'vpc'))
    cf_data = session.to_cfdict()

    if not args.yes:
        answer = session.query_yes_no('Are you sure you want to create a new stack?')
        if answer:
            args.yes = True
        else:
            exit(0)
    else:
        pass

    if args.use_profile:
        session.aws_auth(profile_name=session.get_config('state', 'pysec-state', 'defaultprofile'),
                         region_name=session.get_config('state', 'pysec-state', 'region'))
    else:
        session.aws_auth(aws_access_key_id=args.aws_access_key_id, aws_secret_access_key=args.aws_secret_access_key,
                         region_name=session.get_config('state', 'pysec-state', 'region'))

    if session.get_config('state', 'pysec-state', 'stack') == 'None':
        stack_name = 'PysecSecurityGroup-' + session.random_identifier
        try:
            session.create_stack(StackName=stack_name, TemplateBody=str(cf_data), OnFailure='DELETE')
            session.wait(stack_name, 'stack_create_complete')
            for f in session.file_list:
                session.update_hashfile(f)
            print "[INFO] Stack created successfully"
        except Exception as e:
            print "[INFO] Stack creation failed, rolling back -> " + str(e)

    else:
        stack_name = session.get_config('state', 'pysec-state', 'stackname')
        session.check_hashes()
        if session.diff:
            try:
                session.update_stack(StackName=stack_name, TemplateBody=str(cf_data))
                session.wait(stack_name, 'stack_update_complete')
                for f in session.file_list:
                    session.update_hashfile(f)
                print "[INFO] Stack updated successfully"
            except Exception as e:
                print "[INFO] Stack creation failed, rolling back -> " + str(e)
        else:
            print "[INFO] No changes to commit"
            exit(0)


if __name__ == "__main__":
    main()
