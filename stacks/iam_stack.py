from aws_cdk import (
    aws_iam as iam,
    aws_rds as rds,
    Stack
)
from constructs import Construct

class IAMStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Role with "AmazonSSMManagedInstanceCore" Managed Policy
        # Ref 1: https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_iam/ManagedPolicy.html
        # Ref 2: https://github.com/aws-samples/aws-cdk-examples/blob/master/python/ec2/instance/app.py
        self.ssmrole = iam.Role(self, "EC2SSMInstanceProfile",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            description="Allows EC2 instances to call AWS services on your behalf."
        )
        self.ssmrole.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))

        self.db_secret = rds.DatabaseSecret(self, "DatabaseSecret",
            username="databaseuser",
            secret_name="rds-secret",
        )
