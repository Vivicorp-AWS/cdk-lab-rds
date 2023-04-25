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
            ec2.InstanceClass.T4G, ec2.InstanceSize.MICRO),  # Default instance type: db.t4g.micro
        engine_version:rds.MysqlEngineVersion=rds.MysqlEngineVersion.VER_8_0_32, # Default: MySQL v8.0.32
        **kwargs) -> None:
        
        super().__init__(scope, id, **kwargs)

        # MySQL for RDS Database Instance
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
            ec2.InstanceClass.T4G, ec2.InstanceSize.MICRO),  # Default instance type: db.t4g.micro
        engine_version:rds.MariaDbEngineVersion=rds.MariaDbEngineVersion.VER_10_6_8,  # Default: MariaDB v10.6.8
        **kwargs) -> None:
        
        super().__init__(scope, id, **kwargs)

        # MariaDB for RDS Database Instance
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
        db_name:str="postgres",  # Default Database name: "postgres". Can't use PostgreSQL's reserved name "db" as database name
        instance_type:ec2.InstanceType=ec2.InstanceType.of(
            ec2.InstanceClass.T4G, ec2.InstanceSize.MICRO),  # Default instance type: db.t4g.micro
        engine_version:rds.PostgresEngineVersion=rds.PostgresEngineVersion.VER_15_2,  # Default: PostgreSQL v15.2
        **kwargs) -> None:
        
        super().__init__(scope, id, **kwargs)

        # PostgreSQL for RDS Database Instance
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
