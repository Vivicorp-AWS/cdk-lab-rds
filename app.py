#!/usr/bin/env python3
# Ref:
# https://github.com/aws-samples/aws-cdk-examples/tree/master/python/new-vpc-alb-asg-mysql
# https://github.com/aws-samples/aws-cdk-examples/blob/master/python/rds/aurora/aurora.py
from dotenv import load_dotenv
import os
import sys

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

# Set the default database name
if os.getenv("DB_NAME"):
    DB_NAME = os.getenv("DB_NAME")
else:
    DB_NAME = "database"

# Set the default database username
if os.getenv("DB_USERNAME"):
    DB_USERNAME = os.getenv("DB_USERNAME")
else:
    print("Please specify DB_USERNAME in .env file")
    sys.exit(1)

# Set the default database password
if os.getenv("DB_PASSWORD"):
    DB_PASSWORD = os.getenv("DB_PASSWORD")
else:
    print("Please specify DB_PASSWORD in .env file")
    sys.exit(1)

# Set CDK Environment object to assign default region
ENV = Environment(
    region=REGION
    )

app = cdk.App()

iam_stack = IAMStack(
    app, f"cdk{STACKNAME_PREFIX}iam",
    env=ENV,
    db_name=DB_NAME,
    db_username=DB_USERNAME,
    db_password=DB_PASSWORD,
    description="IAM principal stack",
    )

ssm_role = iam_stack.ssmrole

vpc_stack = VPCStack(
    app, f"cdk{STACKNAME_PREFIX}vpc",
    env=ENV,
    description="VPC stack",
    )

sg_rds = vpc_stack.sg_rds
sg_ec2 = vpc_stack.sg_ec2

ec2_stack = EC2Stack(
    app, f"cdk{STACKNAME_PREFIX}ec2",
    env=ENV,
    description="EC2 instance stack",
    vpc=vpc_stack.vpc,
    security_group=sg_ec2,
    role=ssm_role,
)

# [TODO] Inject db_secret
if DB_ENGINE == 'MySQL':
    rds_stack = MySQLStack(
        app, f"cdk{STACKNAME_PREFIX}rds",
        env=ENV,
        description="MySQL instance stack",
        vpc=vpc_stack.vpc,
        db_name=DB_NAME,
        db_username=DB_USERNAME,
        db_password=DB_PASSWORD,
        )
elif DB_ENGINE == 'MariaDB':
    rds_stack = MariaDBStack(
        app, f"cdk{STACKNAME_PREFIX}rds",
        env=ENV,
        description="MariaDB instance stack",
        vpc=vpc_stack.vpc,
        allow_connection_from_instance=ec2_stack.instance
    )
elif DB_ENGINE == 'PostgreSQL':
    rds_stack = PostgreSQLStack(
        app, f"cdk{STACKNAME_PREFIX}rds",
        env=ENV,
        description="PostgreSQL instance stack",
        vpc=vpc_stack.vpc,
        allow_connection_from_instance=ec2_stack.instance
    )
else:
    raise ValueError('No available database engine option specified. Options: "MySQL", "MariaDB", "PostgreSQL"')


app.synth()
