#!/bin/bash

# Install necessary packages
sudo yum install -y mariadb jq

# Generate a script for user to install example database
cat > /srv/install_example_database.sh << \EOF
# Retrive database identifier, username, and password from secret,
# and retrive database hostname by describe database instances
export SECRET_ID=PLACEHOLDER_SECRET_ID

echo "[INFO] Getting database identifier, username, and password from secret"
export DATABASE_IDENTIFIER=$(aws secretsmanager get-secret-value \
  --secret-id $SECRET_ID \
  --query SecretString \
  --output text | jq -r .database)
export DATABASE_USERNAME=$(aws secretsmanager get-secret-value \
  --secret-id $SECRET_ID \
  --query SecretString \
  --output text | jq -r .username)
export DATABASE_PASSWORD=$(aws secretsmanager get-secret-value \
  --secret-id $SECRET_ID \
  --query SecretString \
  --output text | jq -r .password)
export DATABASE_HOSTNAME=$(aws rds describe-db-instances \
  --db-instance-identifier $DATABASE_IDENTIFIER \
  --output json | jq -r ".DBInstances[0].Endpoint.Address")

# Retrive example database
# Ref: https://dev.mysql.com/doc/index-other.html
echo "[INFO] Downloading example database (employees)"
curl -L https://github.com/datacharmer/test_db/releases/download/v1.0.7/test_db-1.0.7.tar.gz -o /tmp/test_db.tar.gz
tar -zxvf /tmp/test_db.tar.gz -C /tmp
cd /tmp/test_db

# Import example database
echo "[INFO] Importing example database"
mysql -h$DATABASE_HOSTNAME -u$DATABASE_USERNAME -p$DATABASE_PASSWORD -t < ./employees.sql

echo "[INFO] Process finished."
EOF

chmod +x /srv/install_example_database.sh

# Generate a script for user to login database
cat > /srv/login_database.sh << \EOF
# Retrive database identifier, username, and password from secret,
# and retrive database hostname by describe database instances
echo "[INFO] Getting database identifier, username, and password from secret"
export SECRET_ID=PLACEHOLDER_SECRET_ID
export DATABASE_IDENTIFIER=$(aws secretsmanager get-secret-value \
  --secret-id $SECRET_ID \
  --query SecretString \
  --output text | jq -r .database)
export DATABASE_USERNAME=$(aws secretsmanager get-secret-value \
  --secret-id $SECRET_ID \
  --query SecretString \
  --output text | jq -r .username)
export DATABASE_PASSWORD=$(aws secretsmanager get-secret-value \
  --secret-id $SECRET_ID \
  --query SecretString \
  --output text | jq -r .password)
export DATABASE_HOSTNAME=$(aws rds describe-db-instances \
  --db-instance-identifier $DATABASE_IDENTIFIER \
  --output json | jq -r ".DBInstances[0].Endpoint.Address")

# Login database
mysql -h$DATABASE_HOSTNAME -u$DATABASE_USERNAME -p$DATABASE_PASSWORD
EOF

chmod +x /srv/login_database.sh