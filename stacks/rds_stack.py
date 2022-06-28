#!/usr/bin/env python3

from aws_cdk import (
    aws_ec2 as ec2,
    aws_rds as rds,
    RemovalPolicy, Stack
)

from constructs import Construct

class MySqlStack(Stack):
    def __init__(
        self, scope:Construct,
        id:str,
        vpc,
        db_name:str,                ## database name
        instance_type=None,       ## ec2.InstanceType
        engine_version=None,      ## MySQL Engine Version
        **kwargs) -> None:
        
        super().__init__(scope, id, **kwargs)

        # Instance Type: m4.large
        if not instance_type:
            instance_type = ec2.InstanceType.of(ec2.InstanceClass.MEMORY4, ec2.InstanceSize.LARGE)

        # Engine version: ver 8.0.28
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_rds/MysqlEngineVersion.html
        if not engine_version:
            engine_version = rds.MysqlEngineVersion.VER_8_0_28

        # MySQL RDS Database Instance
        self.db = rds.DatabaseInstance(self, "MySQL",
            database_name=db_name,
            engine=rds.DatabaseInstanceEngine.mysql(version=engine_version),
            instance_type=instance_type,
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_group_name="Private"),
            port=3306,
            removal_policy=RemovalPolicy.DESTROY,
            deletion_protection=False
        )
