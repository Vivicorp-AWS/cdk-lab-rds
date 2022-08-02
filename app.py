#!/usr/bin/env python3
# Ref:
# https://github.com/aws-samples/aws-cdk-examples/tree/master/python/new-vpc-alb-asg-mysql
# https://github.com/aws-samples/aws-cdk-examples/blob/master/python/rds/aurora/aurora.py
from dotenv import load_dotenv
import os

import aws_cdk as cdk
from aws_cdk import Environment

from stacks.vpc_stack import VPCStack
from stacks.iam_stack import IAMStack
from stacks.ec2_stack import EC2Stack
from stacks.rds_stack import MySQLStack, MariaDBStack, PostgreSQLStack

load_dotenv()
# Set stack name's prefix
if os.getenv("STACKNAME_PREFIX"):
    STACKNAME_PREFIX = "-" + os.getenv("STACKNAME_PREFIX") + "-"
else:
    STACKNAME_PREFIX = "-"

# Set the default region to deploy workloads
if os.getenv("REGION"):
    REGION = os.getenv("REGION")
else:
    REGION = 'us-east-1'

# Set the default database engine to deploy Amazon RDS workload.
if os.getenv("DB_ENGINE"):
    DB_ENGINE = os.getenv("DB_ENGINE")
else:
    DB_ENGINE = 'MySQL'

# Set CDK Environment object to assign default region
ENV = Environment(
    region=REGION
    )

app = cdk.App()

iam_stack = IAMStack(
    app, f"cdk{STACKNAME_PREFIX}iam",
    env=ENV
    )

vpc_stack = VPCStack(
    app, f"cdk{STACKNAME_PREFIX}vpc",
    env=ENV
    )

ec2_stack = EC2Stack(
    app, f"cdk{STACKNAME_PREFIX}ec2",
    env=ENV,
    vpc=vpc_stack.vpc,
    role=iam_stack.ssmrole
)

if DB_ENGINE == 'MySQL':
    rds_stack = MySQLStack(
        app, f"cdk{STACKNAME_PREFIX}rds",
        env=ENV,
        description="MySQL Instance Stack",
        vpc=vpc_stack.vpc,
        allow_connection_from_instance=ec2_stack.instance
        )
elif DB_ENGINE == 'MariaDB':
    rds_stack = MariaDBStack(
        app, f"cdk{STACKNAME_PREFIX}rds",
        env=ENV,
        description="MariaDB Instance Stack",
        vpc=vpc_stack.vpc,
        allow_connection_from_instance=ec2_stack.instance
    )
elif DB_ENGINE == 'PostgreSQL':
    rds_stack = PostgreSQLStack(
        app, f"cdk{STACKNAME_PREFIX}rds",
        env=ENV,
        description="PostgreSQL Instance Stack",
        vpc=vpc_stack.vpc,
        allow_connection_from_instance=ec2_stack.instance
    )
else:
    raise ValueError('No available database engine option specified. Options: "MySQL", "MariaDB", "PostgreSQL"')


app.synth()
