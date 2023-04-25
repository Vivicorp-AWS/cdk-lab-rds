# Ref: https://github.com/aws-samples/aws-cdk-examples/blob/master/python/ec2/instance/app.py
from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    App, Stack
)
from constructs import Construct
from typing import Optional

class EC2Stack(Stack):

    def __init__(self, scope: Construct, id: str, vpc, role:iam.Role=None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Amazon Linux AMI
        amzn_linux = ec2.MachineImage.latest_amazon_linux(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=ec2.AmazonLinuxEdition.STANDARD,
            virtualization=ec2.AmazonLinuxVirt.HVM,
            storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
            )

        # Create instance in public usbnet,
        # with public assigned and AmazonSSMManagedInstanceCore policy
        self.instance = ec2.Instance(self, "Instance",
            instance_type=ec2.InstanceType("t3.micro"),
            machine_image=amzn_linux,
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_group_name="Public"),
            role=role
            )
