from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_secretsmanager as secretsmanager,
    SecretValue
)
from constructs import Construct

class IAMStack(Stack):
    def __init__(self, scope: Construct, id: str, db_name, db_username, db_password, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Role with "AmazonSSMManagedInstanceCore" Managed Policy
        # Ref 1: https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_iam/ManagedPolicy.html
        # Ref 2: https://github.com/aws-samples/aws-cdk-examples/blob/master/python/ec2/instance/app.py
        self.ssmrole = iam.Role(self, "EC2SSMInstanceProfile",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            description="Allows EC2 instances to call AWS services on your behalf."
        )
        self.ssmrole.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))

        self.db_secret = secretsmanager.Secret(self, "DatabaseSecret",
                                               secret_object_value={
                                                   "database": SecretValue.unsafe_plain_text(db_name),
                                                   "username": SecretValue.unsafe_plain_text(db_username),
                                                   "password": SecretValue.unsafe_plain_text(db_password),
                                               }
        )

        self.ssmrole.attach_inline_policy(iam.Policy(self, "ReadDBSecretPolicy",
                                                          statements=[
            iam.PolicyStatement(
            actions=[
            "secretsmanager:GetResourcePolicy",
            "secretsmanager:GetSecretValue",
            "secretsmanager:DescribeSecret",
            "secretsmanager:ListSecretVersionIds",],
            resources=[self.db_secret.secret_arn]  # [TODO] Get secret by secret name. But should be ARN...... Create a fixed string instead?
            ),
            iam.PolicyStatement(
            actions=[
            "secretsmanager:GetRandomPassword",
            "secretsmanager:ListSecrets",],
            resources=["*"]
            )]
        ))

