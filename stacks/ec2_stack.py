# Ref: https://github.com/aws-samples/aws-cdk-examples/blob/master/python/ec2/instance/app.py
from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    App, Stack
)
from constructs import Construct
from typing import Optional

with open("./user_data/user_data.sh") as f:
    user_data = f.read()

class EC2Stack(Stack):

    def __init__(self, scope: Construct, id: str, vpc, security_group=None, role:iam.Role=None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Amazon Linux AMI
        amzn_linux = ec2.MachineImage.latest_amazon_linux2(
            cpu_type=ec2.AmazonLinuxCpuType.X86_64,
            edition=ec2.AmazonLinuxEdition.STANDARD,
            )

        # Create instance in public usbnet,
        # with public assigned and AmazonSSMManagedInstanceCore policy
        self.instance = ec2.Instance(self, "Lab Bastion",
            instance_type=ec2.InstanceType("t3.micro"),
            machine_image=amzn_linux,
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_group_name="Public"),
            role=role,
            security_group=security_group,
            user_data=ec2.UserData.custom(user_data),
            )
