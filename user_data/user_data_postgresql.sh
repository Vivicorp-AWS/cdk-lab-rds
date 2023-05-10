#!/bin/bash

# Install necessary packages
sudo yum install -y jq
# [NOTE] At this time, topic "postgresql15" is not available in the repository
sudo amazon-linux-extras install -y postgresql14

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
# Ref: https://www.postgresqltutorial.com/postgresql-getting-started/postgresql-sample-database/
echo "[INFO] Downloading example database (dvdrental)"
cd /tmp
curl -L https://www.postgresqltutorial.com/wp-content/uploads/2019/05/dvdrental.zip -O
unzip dvdrental.zip

# Import example database
echo "[INFO] Importing example database"
PGPASSWORD=$DATABASE_PASSWORD psql --host=$DATABASE_HOSTNAME --username=$DATABASE_USERNAME --dbname=postgres -c "CREATE DATABASE dvdrental;"
PGPASSWORD=$DATABASE_PASSWORD pg_restore --host=$DATABASE_HOSTNAME --username=$DATABASE_USERNAME --dbname=dvdrental -c ./dvdrental.tar

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
PGPASSWORD=$DATABASE_PASSWORD psql --host=$DATABASE_HOSTNAME --username=$DATABASE_USERNAME --dbname=postgres
EOF

chmod +x /srv/login_database.sh