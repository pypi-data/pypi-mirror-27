# pysec-aws
Repository approach to security groups, create easy to modify files and use cloudformation to manage your security groups.

## Sample Text File and Syntax
```
## File:   rules.pysec
## Syntax: <ip-address>/<cidr>:<portFrom>-<portTo>^<protocol>

52.35.22.100/32:80-443^tcp
52.35.22.101/32:443^udp
52.35.23.0/21:80^tcp
```

## Install

```bash
pip install pysec-aws
```

## Usage From Shell

```bash
# Initiate a new repository of rules, folder path defaults to current directory.
$ pysec init --folder-path /my-repo
$

# Configure the new repository with required configuration items, --aws-profile-name will search for AWS credential profile
$ pysec configure --vpc-id vpc-12345678 --group-name MySecurityGroup --aws-region us-west-2 --aws-profile-name myprofile
$

# Get a digest of VPC Flow logs - who is connecting to my endpoint?
$ pysec --use-profile testflow --log-group myFlowLogs --log-stream eni-63e3e655-all --look-back 1
Querying log stream eni-63e3e655-all from 1514052976000 to 1514139376000 showing FLOW DIGEST report

  Hits  From             To             ACCEPT/REJECT
------  ---------------  -------------  ---------------
  4391  172.31.42.101    191.88.99.255  ACCEPT
   827  46.23.161.189    172.31.42.101  REJECT
   719  141.214.87.12    172.31.42.101  REJECT
   714  73.72.82.97      172.31.42.101  REJECT
   711  73.72.82.147     172.31.42.101  REJECT
   611  73.72.82.158     172.31.42.101  REJECT
   110  87.93.20.244     172.31.42.101  REJECT

## Add / Remove rules in rules.pysec ##
echo "52.33.24.1/32:80^tcp" >> rules.pysec

# Get repository status
$ pysec status
File Path            MD5 Hash (Committed)              MD5 Hash (Current)                Diff?
-------------------  --------------------------------  --------------------------------  -------
/my-repo/rules.pysec f6722d7eabfcfb0df9bdbb80b7439fdf  654e160cd132a40ed630da0c4d2d8032  True

# Stage a change
$ pysec --use-profile stage
  #  Suggested Change                                      Security Group    Action
---  ----------------------------------------------------  ----------------  --------------
  1  CIDR-IP: 52.33.24.1/32 FROM: 80 TO: 80 PROTOCOL: tcp  MySecurityGroup   ++ addition ++
  2  CIDR-IP: 52.35.23.0/32 FROM: 80 TO: 80 PROTOCOL: tcp  MySecurityGroup   -- removal --

# Get a digest of VPC Flow logs - who is connecting to my endpoint?
$ pysec --use-profile testflow --log-group myFlowLogs --log-stream eni-63e3e655-all --look-back 1
Querying log stream eni-63e3e655-all from 1514052976000 to 1514139376000 showing CHANGE RISK report

  Hits  From             To             ACCEPT/REJECT
------  ---------------  -------------  ---------------
   835  52.33.24.0       191.88.99.255  ACCEPT
   691  52.35.22.100     191.88.99.255  ACCEPT
   647  52.35.22.101     191.88.99.255  ACCEPT
    32  52.33.24.1       172.31.42.101  REJECT

# Commit the changes using profile
$ pysec --use-profile --yes commit
[INFO] Creating Stack arn:aws:cloudformation:us-west-2:123456789123:stack/PysecSecurityGroup-DH447K/0ef530a0-e74a-14e7-9c17-50d5ca789eae
[INFO] Stack created successfully

# Destroy stack and repository
$ pysec --use-profile --yes destroy
[INFO] Deleting Stack arn:aws:cloudformation:us-west-2:123456789123:stack/PysecSecurityGroup-DH447K/0ef530a0-e74a-14e7-9c17-50d5ca789eae
[INFO] Stack deleted successfully
```

## Usage From Code

```python
>>> import pysec
# Loading a single file
>>> p = pysec.SecurityTemplate(input_file_path='/my-repo/rules.pysec')
[INFO] File /my-repo/rules.pysec loaded successfully - 3 ingress rules detected

# Loading a folder of files
>>> p2 = pysec.SecurityTemplate(folder_path='/my-repo')
[INFO] File /my-repo/rules.pysec loaded successfully - 3 ingress rules detected
[INFO] File /my-repo/rules_02.pysec loaded successfully - 3 ingress rules detected

>>> p
{'requests': [{'toPort': '443', 'ip': '52.35.22.100', 'cidr': '32', 'ipProtocol': 'tcp', 'fromPort': '80'}, {'toPort': '443', 'ip': '52.35.22.101', 'cidr': '32', 'ipProtocol': 'udp', 'fromPort': '443'}, {'toPort': '80', 'ip': '52.35.23.0', 'cidr': '21', 'ipProtocol': 'tcp', 'fromPort': '80'}]}

>> p.generate_template(group_name='MySecurityGroup', vpc='vpc-82c92af3')
[INFO] Generated Troposphere object

>>> p.to_file(output_file_path='/my-repo/artifact.yaml', format='yml')
[INFO] CF Template flushed to disk: /my-repo/artifact.yaml

>>> p.to_file(output_file_path='/my-repo/artifact.json', format='json')
[INFO] CF Template flushed to disk: /my-repo/artifact.json

>>> p.to_cfdict()
{'Outputs': {'SecurityGroupId': {'Description': 'Security Group Id', 'Value': {'Ref': 'MySecurityGroup'}}}, 'Resources': {'MySecurityGroup': {'Type': 'AWS::EC2::SecurityGroup', 'Properties': {'SecurityGroupIngress': [{'ToPort': '443', 'FromPort': '80', 'IpProtocol': 'tcp', 'CidrIp': '52.35.22.100/32'}, {'ToPort': '443', 'FromPort': '443', 'IpProtocol': 'udp', 'CidrIp': '52.35.22.101/32'}, {'ToPort': '80', 'FromPort': '80', 'IpProtocol': 'tcp', 'CidrIp': '52.35.23.0/21'}], 'VpcId': 'vpc-82c92af3', 'GroupDescription': 'Security group created by PySec-AWS - MySecurityGroup'}}}}

```

### Artifacts

You can generate either YAML or JSON artifacts.

```yaml
Outputs:
  SecurityGroupId:
    Description: Security Group Id
    Value: !Ref 'MySecurityGroup'
Resources:
  MySecurityGroup:
    Properties:
      GroupDescription: Security group created by automated process - MySecurityGroup
      SecurityGroupIngress:
        - CidrIp: 52.35.22.100/32
          FromPort: '80'
          IpProtocol: tcp
          ToPort: '443'
        - CidrIp: 52.35.22.101/32
          FromPort: '443'
          IpProtocol: udp
          ToPort: '443'
        - CidrIp: 52.35.23.0/21
          FromPort: '80'
          IpProtocol: tcp
          ToPort: '80'
      VpcId: vpc-82c92af3
    Type: AWS::EC2::SecurityGroup
```

## Use cases

If you need to manage a lot of dynamic security group that allow access between multiple AWS accounts, you can use this to keep simple ip lists in your repo per environment / branch, and build them into cloudformation templates during your CICD process, it is easier to manage then making changes directly to a template stored on git.
Alternatively, one could automate the process of building CF templates using this tool -- pull requests can trigger build and update of existing stack (this will require contributions to this tool).

Consider a github repository as a source for whitelisted IP addresses:

```bash
Repository-Root/
├── Production/
│   ├── Service-A/
│   │   ├── .pysec       # pysec state file
│   │   ├── .hashes      # pysec files hash table
│   │   ├── rules.pysec  # pysec rules file
│   ├── Service-B/
│   │   ├── .pysec
│   │   ├── .hashes
│   │   ├── rules.pysec
├── Pre-Production/
│   ├── .../
```

Given changes to a rules file, after cloning this repository, pysec can update relevant stacks in relevant account,
this allows you to delegate control to other teams over relevant security groups, while letting you be a reviewer of
said changes.