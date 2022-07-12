
# CDK LAB for RDS + Glue + Athena

## Prerequisities

### Add stacks' prefix string

Provide a `.env` file with the key `STACKNAME_PREFIX` and value, or the prefix will be omit.

Example:

```
STACKNAME_PREFIX=mylab
```

## Usage

Deploy stacks:

```bash
cdk deploy <stack name>  # Deploy specitic stack
cdk deploy --all # Deploy all stacks
cdk deploy --all --require-approval=never  # Deploy all stacks without asking yes or no
```

Destroy stacks:

```bash
cdk destroy <stack name>  # Destroy specitic stack
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

1. Create another security group to be used on Glue Jobs to connect RDS
  * Create a new inbound rule in RDS's security group, with settings:
    * Type: MySQL (so the protocal and port range will sutomatically be assigned to TCP, 3389)
    * Source: this security group
2. Create a new inbound rule in RDS's security group, with settings:
    * Type: MySQL (so the protocal and port range will sutomatically be assigned to TCP, 3389)
    * Source: EC2's default security group
3. IAM Role for Glue and Glue ETL
4. A Glue Connection to connect RDS
  * A Glue Connection, with this project's VPC, private subnets, the security group created in 1., and IAM role created in 3.
  * A S3 Endpoint, with this project's VPC, and private subnets
