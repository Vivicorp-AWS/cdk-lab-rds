
# CDK LAB for RDS

This is a simple Lab environment for quickly building a Database and its peripheral infrastructures. Including:

* 1x Amazon RDS instance w/ single AZ deployment
* 1x VPC
  * 1x Public Subnet
  * 1x Private Subnet
* 1x EC2 w/ t2.micro instance type in Private Subnet
* 1x Lambda Function to preinstall the sample data

## Prerequisities

### Add stacks' prefix string

Provide a `.env` file with the key `STACKNAME_PREFIX` and value, or the prefix will be omit.

Example:

```
STACKNAME_PREFIX=mylab
```

Provide a `.env` file with the key `REGION` and value, or the region will set set to "us-east-1" as default.

Example:

```
REGION=us-east-2
```

### Set region to deploy

## Usage

Deploy stacks:

```bash
cdk deploy <stack name>  # Deploy specitic stack
cdk deploy cdk-iam  # e.g: Deploy the IAM stack if no STACKNAME_PREFIX specified
cdk deploy cdk-mylab-iam  # e.g: Deploy the IAM stack if no STACKNAME_PREFIX assigned as "mylab"
cdk deploy --all # Deploy all stacks
cdk deploy --all --require-approval=never  # Deploy all stacks without asking yes or no
```

Destroy stacks:

```bash
cdk destroy <stack name>  # Destroy specitic stack
cdk destroy cdk-iam  # e.g: Destroy the IAM stack if no STACKNAME_PREFIX specified
cdk destroy cdk-mylab-iam  # e.g: Destroy the IAM stack if no STACKNAME_PREFIX assigned as "mylab"
cdk destroy --all # Destroy all stacks
```

## Components to deploy

* IAM Stack (`cdk-<prefix>-iam-stack`)
  * A role called `EC2SSMInstanceProfile` with `AmazonSSMManagedInstanceCore` managed policy to connect to the EC2 instance used as development environment
* VPC Stack (`cdk-<prefix>-vpc-stack`)
  * A brand new VPC with 2 Availability Zones to create subnets
  * 2 public subnets in each AZ
  * 2 private subnets in each AZ
* EC2 Stack (`cdk-<prefix>-ec2-stack`)
  * A `t2.micro` free instance with `EC2SSMInstanceProfile` role attached
* RDS Stack (`cdk-<prefix>-rds-stack`)
  * A RDS for MySQL `v8.0.28` database instance in private subnets

## Todos

1. Use environment variable to choose which RDS engine to be deployed. Options: MySQL, MariaDB, PostgreSQL
2. Create another security group to be used on Glue Jobs to connect RDS
  * Create a new inbound rule in RDS's security group, with settings:
    * Type: MySQL (so the protocal and port range will sutomatically be assigned to TCP, 3389)
    * Source: this security group
3. Create a new inbound rule in RDS's security group, with settings:
    * Type: MySQL (so the protocal and port range will sutomatically be assigned to TCP, 3389)
    * Source: EC2's default security group
4. Create a Lambda Function to preinstall the sample data
