from aws_cdk import CfnOutput, Stack, NestedStack
import aws_cdk.aws_ec2 as ec2
from constructs import Construct

class VPCStack(NestedStack):

    def __init__(self, scope: Construct, id: str, db_engine:str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # VPC in 2 azs, including 1 public and 1 private subnet in each az
        self.vpc = ec2.Vpc(
            self, "VPC",
            max_azs=2,
            ip_addresses=ec2.IpAddresses.cidr("10.10.0.0/16"),
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
        
        # Security group for EC2
        self.sg_ec2 = ec2.SecurityGroup(
            self, "EC2SecurityGroup",
            vpc=self.vpc,
            allow_all_outbound=True,
        )


        # Security group for MySQL/MariaDB RDS instance
        self.sg_rds = ec2.SecurityGroup(
            self, "RDSSecurityGroup",
            vpc=self.vpc,
            allow_all_outbound=True,
        )

        if db_engine in ("MySQL", "MariaDB"):
            self.sg_rds.add_ingress_rule(self.sg_ec2, ec2.Port.tcp(3306))
        elif db_engine == "PostgreSQL":
            self.sg_rds.add_ingress_rule(self.sg_ec2, ec2.Port.tcp(5432))

        # CfnOutput(self, "Output",
        #                value=self.vpc.vpc_id)