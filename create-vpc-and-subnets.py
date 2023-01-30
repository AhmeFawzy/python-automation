import boto3

# Create a resource for the EC2 service
ec2_resource = boto3.resource('ec2', region_name='eu-west-3')
ec2 = boto3.client('ec2', region_name='eu-west-3')

# Create a VPC
new_vpc = ec2_resource.create_vpc(CidrBlock="10.0.0.0/16")

# Tag the VPC
new_vpc.create_tags(Tags=[{'Key':'Name','Value':'my-vpc'}])

# Create two subnets in the VPC
subnet1=new_vpc.create_subnet(CidrBlock="10.0.1.0/24")
subnet1.create_tags(Tags=[{'Key': 'Name', 'Value': 'my-subnet-1'}])

subnet2=new_vpc.create_subnet(CidrBlock="10.0.2.0/24")
subnet2.create_tags(Tags=[{'Key': 'Name', 'Value': 'my-subnet-2'}])


# Retrieve all VPCs
vpcs = ec2.describe_vpcs().get('Vpcs', [])

# Loop through each VPC and print its information
for vpc in vpcs:
    vpc_id = vpc['VpcId']
    vpc_cidr = vpc['CidrBlock']
    vpc_state = vpc['State']
    vpc_is_default = vpc.get('IsDefault', False)
    print("VPC ID: ", vpc_id)
    print("VPC CIDR: ", vpc_cidr)
    print("VPC State: ", vpc_state)
    print("Is default VPC: ", vpc_is_default)
    subnets = ec2.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc['VpcId']]}]).get('Subnets', [])
    for subnet in subnets:
        print(">>>Subnet Information:")
        print("    -Subnet ID: ", subnet['SubnetId'])
        print("    -Subnet CIDR: ", subnet['CidrBlock'])
        print("    -Subnet Availability Zone: ", subnet['AvailabilityZone'])
        print("    -Subnet Name: ", [tag['Value'] for tag in subnet.get('Tags', []) if tag['Key'] == 'Name'])
    print("------------------")
