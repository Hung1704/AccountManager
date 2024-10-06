# README for Account Management System

## Overview

This system allows you to manage user accounts, VPN configurations, RSA keys, and other server-related settings through a series of JSON files and scripts. The scripts automate actions such as account creation, password reset, process group management, VPN management, and account suspension.

## Directory Structure
|-- 01_run                      # Main script to execute the account.py Python script
|-- RSA_key                     # Contains generated RSA key files
|   |-- 2024_Fall_cylee.key      # RSA private key for the cylee course
|   `-- 2024_Fall_cylee.key.pub  # RSA public key for the cylee course
|-- VPN_config                  # VPN configuration files
|   `-- 2024_Fall_cylee_VPN_Config.txt  # VPN configuration for the cylee course
|-- VPN_passwd                  # Stores VPN account passwords
|   `-- 2024_Fall_cylee_VPN.csv  # VPN accounts and their corresponding passwords for the cylee course
|-- account.py                  # Python script to manage accounts, VPNs, and other settings
|-- *.json                      # JSON configuration files for various tasks (detailed below)
|-- server_passwd               # Contains passwords for server accounts
|   `-- 2024_Fall_cylee_EEHPC.csv  # Passwords for server accounts of the cylee course
`-- readme                      # This README file


## Folder Descriptions
### RSA_key/: 
This folder contains RSA key pairs (private and public keys) for the accounts. These keys are used for secure access and authentication.

Example: 2024_Fall_cylee.key and 2024_Fall_cylee.key.pub represent the private and public RSA keys for the cylee course in the Fall 2024 term.

### VPN_config/: 
This folder stores the VPN configuration files, which are used to configure VPN access for users. The VPN configuration files contain details such as account names and passwords.

Example: 2024_Fall_cylee_VPN_Config.txt contains VPN configuration for the cylee course.

### VPN_passwd/: 
This folder contains CSV files that store VPN accounts and their associated passwords.

Example: 2024_Fall_cylee_VPN.csv lists the VPN accounts and their passwords for the cylee course.

### server_passwd/: 
This folder stores server account passwords in CSV format.

Example: 2024_Fall_cylee_EEHPC.csv contains the server account names and passwords for the cylee course.

## How to Use the System
You can execute the scripts using the ./01_run command, which runs the account.py Python script with the specified options.

### Usage Examples
#### Run a JSON configuration file:
./01_run -r <JSON file>
Example:
./01_run -r remove_vpn.json

This command will run the account.py script and pass the remove_vpn.json file as the configuration.

#### Run the Python script with sudo (for privileged actions):
sudo python account.py -r <JSON file>

Example:
sudo python account.py -r remove_vpn.json

This is useful for actions that require administrative privileges, such as modifying user accounts, setting passwords, or configuring VPNs.

### JSON Configuration Files
The system uses JSON files to define specific actions. Here are some examples:

add_process_group.json: Adds users to specified process groups.
add_vpn.json: Creates VPN accounts and assigns passwords.
ban_users.json: Temporarily disables user accounts.
create.json: Creates new user accounts based on the specified details.
remove_process_group.json: Removes users from specified process groups.
remove_vpn.json: Deletes VPN accounts.
reset_expire_day.json: Resets the account expiration date.
reset_inactive_day.json: Resets the inactive period for user accounts.
reset_passwd.json: Resets the passwords for user accounts.
reset_quota.json: Resets the disk quota for user accounts.
Running the Script
To run the script with different configurations, use the following format:

./01_run -r <read_json> -w <write_json>
Example:
If you want to read the configuration from remove_vpn.json and write the output to log_output.json, use the following:
./01_run -r remove_vpn.json -w log_output.json
This will execute the script with the specified read and write JSON files.