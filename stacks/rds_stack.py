#!/usr/bin/env python3

from aws_cdk import (
    aws_ec2 as ec2,
    aws_rds as rds,
    RemovalPolicy, Stack
)

from constructs import Construct

class MySQLStack(Stack):
    def __init__(
        self, scope:Construct,
        id:str,
        vpc,
        allow_connection_from_instance,
        db_name:str="db",  # Default Database name: "db"
        instance_type:ec2.InstanceType=ec2.InstanceType.of(
            ec2.InstanceClass.MEMORY4, ec2.InstanceSize.LARGE),  # Default instance type: m4.large
        engine_version:rds.MysqlEngineVersion=rds.MysqlEngineVersion.VER_8_0_28, # Default: MySQL v8.0.28
        **kwargs) -> None:
        
        super().__init__(scope, id, **kwargs)

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

        if allow_connection_from_instance:
            self.db.connections.allow_from(allow_connection_from_instance, ec2.Port.tcp(3306), "Inbound from EC2")

class MariaDBStack(Stack):
    def __init__(
        self, scope:Construct,
        id:str,
        vpc,
        allow_connection_from_instance,
        db_name:str="db",  # Default Database name: "db"
        instance_type:ec2.InstanceType=ec2.InstanceType.of(
            ec2.InstanceClass.MEMORY4, ec2.InstanceSize.LARGE),  # Default instance type: m4.large
        engine_version:rds.MariaDbEngineVersion=rds.MariaDbEngineVersion.VER_10_5_9,  # Default: MariaDB v10.5.9
        **kwargs) -> None:
        
        super().__init__(scope, id, **kwargs)

        # MySQL RDS Database Instance
        self.db = rds.DatabaseInstance(self, "MariaDB",
            database_name=db_name,
            engine=rds.DatabaseInstanceEngine.maria_db(version=engine_version),
            instance_type=instance_type,
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_group_name="Private"),
            port=3306,
            removal_policy=RemovalPolicy.DESTROY,
            deletion_protection=False
        )

        if allow_connection_from_instance:
            self.db.connections.allow_from(allow_connection_from_instance, ec2.Port.tcp(3306), "Inbound from EC2")

class PostgreSQLStack(Stack):
    def __init__(
        self, scope:Construct,
        id:str,
        vpc,
        allow_connection_from_instance,
        db_name:str="db",  # Default Database name: "db"
        instance_type:ec2.InstanceType=ec2.InstanceType.of(
            ec2.InstanceClass.MEMORY4, ec2.InstanceSize.LARGE),  # Default instance type: m4.large
        engine_version:rds.PostgresEngineVersion=rds.PostgresEngineVersion.VER_14_2,  # Default: PostgreSQL v14.2
        **kwargs) -> None:
        
        super().__init__(scope, id, **kwargs)

        # MySQL RDS Database Instance
        self.db = rds.DatabaseInstance(self, "PostgreSQL",
            database_name=db_name,
            engine=rds.DatabaseInstanceEngine.postgres(version=engine_version),
            instance_type=instance_type,
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_group_name="Private"),
            port=5432,
            removal_policy=RemovalPolicy.DESTROY,
            deletion_protection=False
        )

        if allow_connection_from_instance:
            self.db.connections.allow_from(allow_connection_from_instance, ec2.Port.tcp(5432), "Inbound from EC2")
