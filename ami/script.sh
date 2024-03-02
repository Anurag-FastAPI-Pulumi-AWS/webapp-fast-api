#!/bin/bash
sudo yum update
sudo yum upgrade
sudo dnf update
sudo dnf install python3.11 -y
sudo dnf install python3.11-pip -y
sudo dnf install unzip
python3.11 -m pip --version
python3.11 -m pip install virtualenv
sudo dnf install postgresql15.x86_64 postgresql15-server -y
sudo postgresql-setup --initdb
sudo systemctl start postgresql
sudo systemctl enable postgresql
sudo systemctl status postgresql
sudo sed -i 's/ident$/md5/' /var/lib/pgsql/data/pg_hba.conf
sudo systemctl restart postgresql
NEW_PASSWORD="Anurag*98"

# Change the ssh user password
sudo passwd postgres <<EOF
${NEW_PASSWORD}
${NEW_PASSWORD}
EOF

sudo su - postgres <<EOF
# Now, change the admin database password
psql -c "ALTER USER postgres WITH PASSWORD '1234';"
psql -c "create database webappdb;"
EOF

