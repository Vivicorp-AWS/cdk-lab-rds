# Ref: https://github.com/aws-samples/aws-cdk-examples/blob/master/python/ec2/instance/app.py
from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    App, Stack, NestedStack
)
from constructs import Construct
from typing import Optional

# Load user data for different database engine
with open("./user_data/user_data_mysql.sh") as f:
    user_data_mysql = f.read()

with open("./user_data/user_data_postgresql.sh") as f:
    user_data_postgresql = f.read()

class EC2Stack(NestedStack):

    def __init__(
            self, scope: Construct,
            id: str,
            vpc,
            security_group,
            role:iam.Role,
            db_engine:str,
            db_secret_name:str,
            **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Amazon Linux AMI
        amzn_linux = ec2.MachineImage.latest_amazon_linux2(
            cpu_type=ec2.AmazonLinuxCpuType.X86_64,
            edition=ec2.AmazonLinuxEdition.STANDARD,
            )
        
        # Choose the user data by database engine
        if db_engine in ("MySQL", "MariaDB"):
            self.user_data = user_data_mysql
        elif db_engine == "PostgreSQL":
            self.user_data = user_data_postgresql
        
        # Replace the placeholser string of secret id with secret name
        self.user_data = self.user_data.replace("PLACEHOLDER_SECRET_ID", db_secret_name)

        # Create instance in public usbnet,
        # with public assigned and AmazonSSMManagedInstanceCore policy
        self.instance = ec2.Instance(self, "Lab Bastion",
            instance_type=ec2.InstanceType("t3.micro"),
            machine_image=amzn_linux,
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_group_name="Public"),
            role=role,
            security_group=security_group,
            user_data=ec2.UserData.custom(self.user_data),
            )
