#!/usr/bin/env python3
# Ref:
# https://github.com/aws-samples/aws-cdk-examples/tree/master/python/new-vpc-alb-asg-mysql
# https://github.com/aws-samples/aws-cdk-examples/blob/master/python/rds/aurora/aurora.py
from dotenv import load_dotenv
import os

import aws_cdk as cdk
from aws_cdk import Environment

from stacks.vpc_stack import VpcStack
from stacks.iam_stack import IAMStack
from stacks.ec2_stack import EC2Stack
from stacks.rds_stack import MySqlStack

# Set stack name prefix
# Should be named as "-<STACKNAME>", e.g: "-vivilab"
# Else, set a empty string ""
load_dotenv()

if os.getenv("STACKNAME_PREFIX"):
    STACKNAME_PREFIX = "-" + os.getenv("STACKNAME_PREFIX") + "-"
else:
    STACKNAME_PREFIX = "-"

# Set environment to assign default region
ENV = Environment(
    region="ap-northeast-1"
    )

app = cdk.App()

iam_stack = IAMStack(
    app, f"cdk{STACKNAME_PREFIX}iam",
    env=ENV
    )

vpc_stack = VpcStack(
    app, f"cdk{STACKNAME_PREFIX}vpc",
    env=ENV
    )

ec2_stack = EC2Stack(
    app, f"cdk{STACKNAME_PREFIX}ec2",
    env=ENV,
    vpc=vpc_stack.vpc,
    role=iam_stack.ssmrole
)

mysql_stack = MySqlStack(
    app, f"cdk{STACKNAME_PREFIX}mysql",
    env=ENV,
    description="MySQL Instance Stack",
    db_name="db",
    vpc=vpc_stack.vpc
    )

app.synth()
