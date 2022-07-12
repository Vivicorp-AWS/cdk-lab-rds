from aws_cdk import CfnOutput, Stack
import aws_cdk.aws_ec2 as ec2
from constructs import Construct

class VpcStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # VPC in 2 azs, including 1 public and 1 private subnet in each az
        self.vpc = ec2.Vpc(
            self, "VPC",
            max_azs=2,
            cidr="10.10.0.0/16",
            # configuration will create 2 groups in 2 AZs = 4 subnets.
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PUBLIC,
                    name="Public",
                    cidr_mask=24
                    ),
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                    name="Private",
                    cidr_mask=24
                    )
                ],
            )

        # CfnOutput(self, "Output",
        #                value=self.vpc.vpc_id)