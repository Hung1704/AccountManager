# Account Management System

## Overview

This system is designed to automate account management tasks such as user creation, VPN configuration, RSA key generation, process group management, and more. By leveraging JSON configuration files, the system simplifies complex server operations, making it easier to manage large-scale student and TA accounts efficiently.

## Key Features

* **User Account Management**: Automate the creation, deletion, and management of student and TA accounts.
* **VPN Configuration**: Easily configure VPN access for users through automated account creation and password management.
* **Process Group Management**: Add or remove users from designated process groups.
* **RSA Key Generation**: Automatically generate RSA key pairs for secure login.
* **Quota Management**: Set and reset user and group storage quotas.
* **Password Reset**: Automate password generation and management.
* **Account Suspension & Activation**: Ban or unlock accounts as needed.

## Usage Instructions

### Running the Script

The main Python script `account.py` is designed to execute commands based on the provided JSON configuration file. You can run the script using the `01_run` command:

```bash
./01_run -r <json_config_file>
```

For example, to create accounts based on the `create.json` file, run:

```bash
./01_run -r create.json
```

If the operation requires administrative privileges, run the script with `sudo`:

```bash
sudo python account.py -r <json_config_file>
```

### JSON Configuration Files

Each JSON file defines a specific operation, such as account creation, password resetting, or VPN configuration. Below is a list of the main JSON files and what they do:

1. **`create.json`**  
**Description**: Creates user accounts, including both students and TAs. Sets up home directories, quotas, and passwords.  
**Command**:

   ```bash
   ./01_run -r create.json
   ```

2. **`reset_passwd.json`**  
**Description**: Resets passwords for existing accounts. You can choose random password generation or set predefined formats.  
**Command**:

   ```bash
   ./01_run -r reset_passwd.json
   ```

3. **`add_vpn.json`**  
**Description**: Creates VPN accounts with auto-generated passwords and saves the configuration for VPN systems.  
**Command**:

   ```bash
   ./01_run -r add_vpn.json
   ```

4. **`ban_users.json`**  
**Description**: Bans user accounts, disabling their access temporarily.  
**Command**:

   ```bash
   ./01_run -r ban_users.json
   ```

5. **`unlock_binding_account.json`**  
**Description**: Unlocks user accounts and optionally binds them with additional configurations such as RSA keys.  
**Command**:

   ```bash
   ./01_run -r unlock_binding_account.json
   ```

6. **`add_process_group.json`**  
**Description**: Adds users to specific process groups, granting them access to certain system resources.  
**Command**:

   ```bash
   ./01_run -r add_process_group.json
   ```

7. **`remove_process_group.json`**  
**Description**: Removes users from specified process groups, revoking their access.  
**Command**:

   ```bash
   ./01_run -r remove_process_group.json
   ```

8. **`reset_quota.json`**  
**Description**: Resets the storage quotas for user accounts, ensuring that soft and hard limits are properly set.  
**Command**:

   ```bash
   ./01_run -r reset_quota.json
   ```

9. **`reset_expire_day.json`**  
**Description**: Resets the expiration dates for accounts, extending or limiting their access periods.  
**Command**:

   ```bash
   ./01_run -r reset_expire_day.json
   ```

10. **`remove_vpn.json`**  
**Description**: Deletes VPN accounts for users, removing their access to the VPN.  
**Command**:

  ```bash
  ./01_run -r remove_vpn.json
  ```

### Example Workflow

1. **Create New User Accounts**  
Create student and TA accounts using the `create.json` configuration:

   ```bash
   ./01_run -r create.json
   ```

2. **Reset Passwords for Accounts**  
Reset passwords for the created accounts:

   ```bash
   ./01_run -r reset_passwd.json
   ```

3. **Assign Process Groups**  
Add users to a specific process group:

   ```bash
   ./01_run -r add_process_group.json
   ```

4. **Generate VPN Accounts**  
Create VPN accounts and set up their configurations:

   ```bash
   ./01_run -r add_vpn.json
   ```

5. **Unlock User Accounts**  
Unlock user accounts that were previously banned:

   ```bash
   ./01_run -r unlock_binding_account.json
   ```

## Environment Requirements

* **Linux OS** (Tested on CentOS and Rocky Linux)
* **Python 2.x** (for compatibility with older systems)
* **Administrative Privileges** for actions like account creation, quota setting, and VPN configuration.
* **SSH Access** for managing RSA keys and secure login setups.

## Folder Structure

The folder structure of this system is as follows:

```bash
.
├── 00_template.json             # Template for creating new JSON configurations
├── 01_run                       # Main script to execute the account.py Python script
├── account.py                   # Core Python script for account and VPN management
├── add_process_group.json        # JSON for adding process groups to accounts
├── add_vpn.json                  # JSON for adding VPN accounts
├── ban_users.json                # JSON for banning user accounts
├── copy_rsa_passwd.json          # JSON for copying RSA keys and passwords
├── create.json                   # JSON for creating user accounts
├── delete.json                   # JSON for deleting accounts
├── README.md                     # This README file
├── remove_process_group.json     # JSON for removing process groups from accounts
├── remove_vpn.json               # JSON for deleting VPN accounts
├── reset_expire_day.json         # JSON for resetting account expiration dates
├── reset_inactive_day.json       # JSON for resetting account inactive periods
├── reset_passwd.json             # JSON for resetting account passwords
├── reset_quota.json              # JSON for resetting user quotas
├── RSA_key/                      # Directory for storing RSA key files
├── server_passwd/                # Directory containing server account passwords
├── unlock_binding_account.json   # JSON for unlocking and binding accounts
├── VPN_config/                   # Directory for storing VPN configuration files
└── VPN_passwd/                   # Directory for storing VPN account passwords
```

## Conclusion

This Account Management System is designed to streamline and automate the administrative processes involved in managing large-scale student and TA accounts. By utilizing JSON configuration files, it allows flexibility and repeatability in managing users, quotas, VPNs, and process groups with minimal effort. Simply modify the JSON files to suit your needs, run the script, and the system will handle the rest.

