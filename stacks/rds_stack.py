#!/usr/bin/env python3

from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_rds as rds,
    SecretValue,
    Duration,
    aws_logs as logs,
    RemovalPolicy, 
)

from constructs import Construct

class MySQLStack(Stack):
    def __init__(
        self, scope:Construct,
        id:str,
        vpc,
        db_params,
        db_name:str="db",  # Default Database name: "db"
        security_groups=None,
        instance_type:ec2.InstanceType=ec2.InstanceType.of(
            ec2.InstanceClass.T4G, ec2.InstanceSize.MICRO),  # Default instance type: db.t4g.micro
        engine_version:rds.MysqlEngineVersion=rds.MysqlEngineVersion.VER_8_0_32, # Default: MySQL v8.0.32
        **kwargs) -> None:
        
        super().__init__(scope, id, **kwargs)

        # MySQL for RDS Database Instance
        self.db = rds.DatabaseInstance(self, "MySQL",
            credentials=rds.Credentials.from_username(
                username=db_params["username"],
                password=SecretValue.unsafe_plain_text(db_params["password"])
            ),
            database_name=db_name,
            instance_identifier=db_params["identifier"],
            engine=rds.DatabaseInstanceEngine.mysql(version=engine_version),
            instance_type=instance_type,
            backup_retention=Duration.days(0),
            cloudwatch_logs_retention=logs.RetentionDays.ONE_MONTH,
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_group_name="Private"),
            port=3306,
            security_groups=security_groups,
            removal_policy=RemovalPolicy.DESTROY,
            deletion_protection=False
        )


class MariaDBStack(Stack):
    def __init__(
        self, scope:Construct,
        id:str,
        vpc,
        db_params,
        db_name:str="db",  # Default Database name: "db"
        security_groups=None,
        instance_type:ec2.InstanceType=ec2.InstanceType.of(
            ec2.InstanceClass.T4G, ec2.InstanceSize.MICRO),  # Default instance type: db.t4g.micro
        engine_version:rds.MariaDbEngineVersion=rds.MariaDbEngineVersion.VER_10_6_8,  # Default: MariaDB v10.6.8
        **kwargs) -> None:
        
        super().__init__(scope, id, **kwargs)

        # MariaDB for RDS Database Instance
        self.db = rds.DatabaseInstance(self, "MariaDB",
            credentials=rds.Credentials.from_username(
                username=db_params["username"],
                password=SecretValue.unsafe_plain_text(db_params["password"])
            ),
            database_name=db_name,
            instance_identifier=db_params["identifier"],
            engine=rds.DatabaseInstanceEngine.maria_db(version=engine_version),
            instance_type=instance_type,
            backup_retention=Duration.days(0),
            cloudwatch_logs_retention=logs.RetentionDays.ONE_MONTH,
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_group_name="Private"),
            port=3306,
            security_groups=security_groups,
            removal_policy=RemovalPolicy.DESTROY,
            deletion_protection=False
        )

class PostgreSQLStack(Stack):
    def __init__(
        self, scope:Construct,
        id:str,
        vpc,
        db_params,
        db_name:str="postgres",  # Default Database name: "postgres". Can't use PostgreSQL's reserved name "db" as database name
        security_groups=None,
        instance_type:ec2.InstanceType=ec2.InstanceType.of(
            ec2.InstanceClass.T4G, ec2.InstanceSize.MICRO),  # Default instance type: db.t4g.micro
        engine_version:rds.PostgresEngineVersion=rds.PostgresEngineVersion.VER_15_2,  # Default: PostgreSQL v15.2
        **kwargs) -> None:
        
        super().__init__(scope, id, **kwargs)

        # PostgreSQL for RDS Database Instance
        self.db = rds.DatabaseInstance(self, "PostgreSQL",
            credentials=rds.Credentials.from_username(
                username=db_params["username"],
                password=SecretValue.unsafe_plain_text(db_params["password"])
            ),
            database_name=db_name,
            instance_identifier=db_params["identifier"],
            engine=rds.DatabaseInstanceEngine.postgres(version=engine_version),
            instance_type=instance_type,
            backup_retention=Duration.days(0),
            cloudwatch_logs_retention=logs.RetentionDays.ONE_MONTH,
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_group_name="Private"),
            port=5432,
            security_groups=security_groups,
            removal_policy=RemovalPolicy.DESTROY,
            deletion_protection=False
        )
