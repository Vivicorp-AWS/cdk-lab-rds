import os, sys
import aws_cdk as cdk
from aws_cdk import (
    Environment,
    aws_iam as iam,
    aws_secretsmanager as secretsmanager,
    aws_rds as rds,
)
from aws_cdk.assertions import (
    Template,
    )
from dotenv import load_dotenv
from stacks.iam_stack import IAMStack

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
if os.getenv("DB_IDENTIFIER"):
    DB_IDENTIFIER = os.getenv("DB_IDENTIFIER")
else:
    print("Please specify DB_IDENTIFIER in .env file")
    sys.exit(1)

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

# Aggregrate database related parameters
db_params = {
    "username": DB_USERNAME,
    "password": DB_PASSWORD,
    "identifier": DB_IDENTIFIER,
    "engine": DB_ENGINE,
}

# Set CDK Environment object to assign default region
ENV = Environment(
    region=REGION
    )

app = cdk.App()

iam_stack = IAMStack(
    app, f"cdk{STACKNAME_PREFIX}iam",
    env=ENV,
    db_params=db_params,
    description="IAM principal stack",
    )

template = Template.from_stack(iam_stack)

def test_number_of_iam_role():
    # There should be 1 IAM role as EC2 instance profile
    template.resource_count_is("AWS::IAM::Role", 1)

def test_number_of_iam_policy():
    # There should be 2 IAM policies
    template.resource_count_is("AWS::IAM::Policy", 2)

def test_db_secret_is_secretsmanager_secret():
    # DB secret should be a secretsmanager.Secret
    assert isinstance(iam_stack.db_secret, secretsmanager.ISecret)
