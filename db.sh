#!/bin/bash

# Function to check if PostgreSQL is installed
check_postgres_installed() {
    if ! command -v psql > /dev/null; then
        echo "PostgreSQL is not installed. Installing..."
        # Install PostgreSQL
        sudo apt update
        sudo apt install postgresql postgresql-contrib -y
    fi
}

# Variables
DB_NAME="sukdb"
DB_USER="sukadmin"
DB_PASS="sukpass"

# Check if PostgreSQL is installed
check_postgres_installed

# Create database
echo "Creating database $DB_NAME..."
sudo -u postgres psql -c "CREATE DATABASE $DB_NAME;"

# Create user with password
echo "Creating user $DB_USER..."
sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';"

# Grant all privileges on database to user
echo "Granting privileges to $DB_USER on database $DB_NAME..."
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"

echo "Database setup complete."
