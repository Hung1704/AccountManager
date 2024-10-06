# Account Management System

## Overview

This system automates account management tasks, such as user creation, VPN configuration, RSA key generation, process group management, and more. By leveraging JSON configuration files, the system simplifies complex server operations, making it easier to manage large-scale student and TA accounts efficiently.

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

## JSON Configuration Files and Parameter Explanations

Each JSON file defines a specific operation, such as account creation, password resetting, or VPN configuration. Below is a list of the main JSON files, their purposes, and a detailed explanation of the key parameters in each file:

### 1\. **`create.json`**

**Description**: Creates user accounts (students and TAs), sets up home directories, quotas, and passwords.

**Parameters**:

* `creator`: (String) The name of the person or system creating the accounts.
* `course_name`: (String) The course or group name associated with the accounts.
* `term`: (String) The term or semester, e.g., `2024_Fall`.
* `stu_from`, `stu_to`: (Int) The starting and ending numbers for student accounts.
* `TA_from`, `TA_to`: (Int) The starting and ending numbers for TA accounts.
* `Enable_Create`: (Boolean) Whether to enable account creation.
* `Enable_Set_Process_Group`: (Boolean) Whether to enable process group assignments.
* `process_groups`: (Array) List of process groups to which users will be added.
* `Enable_Change_Password`: (Boolean) Whether to enable password changes.
* `Random_Password`: (Boolean) If true, generate random passwords; otherwise, use a fixed format.
* `prefix`, `special_length`, `suffix_length`, `special_chars`: (String/Int) Parameters for generating random passwords (prefix, length of special characters, and suffix).
* `Enable_Set_User_Quota`: (Boolean) Whether to set storage quotas for users.
* `student_quota_bsoft`, `student_quota_bhard`: (String) Soft and hard quota limits for student accounts.
* `ta_quota_bsoft`, `ta_quota_bhard`: (String) Soft and hard quota limits for TA accounts.

**Command**:

```bash
./01_run -r create.json
```

### 2\. **`reset_passwd.json`**

**Description**: Resets passwords for existing accounts.

**Parameters**:

* `Enable_Change_Password`: (Boolean) Whether to enable password resetting.
* `Random_Password`: (Boolean) If true, generates random passwords; otherwise, uses predefined formats.
* `prefix`, `special_length`, `suffix_length`, `special_chars`: (String/Int) Parameters for generating new passwords.

**Command**:

```bash
./01_run -r reset_passwd.json
```

### 3\. **`add_vpn.json`**

**Description**: Creates VPN accounts with auto-generated passwords.

**Parameters**:

* `Enable_Create_VPN`: (Boolean) Whether to enable VPN account creation.
* `VPN_Random_Password`: (Boolean) If true, generate random VPN passwords.
* `VPN_password_prefix`, `VPN_password_special_length`, `VPN_password_suffix_length`, `VPN_password_special_chars`: (String/Int) Parameters for generating VPN passwords.

**Command**:

```bash
./01_run -r add_vpn.json
```

### 4\. **`ban_users.json`**

**Description**: Temporarily disables or "bans" user accounts.

**Parameters**:

* `Enable_Set_Expire_Day`: (Boolean) Whether to enable account suspension by setting an expiration date.
* `expiry`: (String) The date on which the accounts will be suspended (e.g., `2024-09-19`).

**Command**:

```bash
./01_run -r ban_users.json
```

### 5\. **`unlock_binding_account.json`**

**Description**: Unlocks user accounts and optionally binds them with additional configurations like RSA keys.

**Parameters**:

* `Enable_Unlock_Account`: (Boolean) Whether to unlock banned or suspended accounts.
* `Enable_Set_Process_Group`: (Boolean) Whether to add users to process groups after unlocking.

**Command**:

```bash
./01_run -r unlock_binding_account.json
```

### 6\. **`add_process_group.json`**

**Description**: Adds users to specified process groups.

**Parameters**:

* `Enable_Set_Process_Group`: (Boolean) Whether to enable process group assignments.
* `process_groups`: (Array) List of process groups to which users will be added.

**Command**:

```bash
./01_run -r add_process_group.json
```

### 7\. **`remove_process_group.json`**

**Description**: Removes users from specified process groups.

**Parameters**:

* `Enable_Remove_Process_Group`: (Boolean) Whether to enable the removal of users from process groups.
* `Remove_process_groups`: (Array) List of process groups from which users will be removed.

**Command**:

```bash
./01_run -r remove_process_group.json
```

### 8\. **`reset_quota.json`**

**Description**: Resets storage quotas for user accounts.

**Parameters**:

* `Enable_Set_User_Quota`: (Boolean) Whether to enable quota resetting for users.
* `student_quota_bsoft`, `student_quota_bhard`: (String) New soft and hard quota limits for student accounts.
* `ta_quota_bsoft`, `ta_quota_bhard`: (String) New soft and hard quota limits for TA accounts.

**Command**:

```bash
./01_run -r reset_quota.json
```

### 9\. **`reset_expire_day.json`**

**Description**: Resets the expiration date for accounts.

**Parameters**:

* `Enable_Set_Expire_Day`: (Boolean) Whether to enable resetting the expiration dates for accounts.
* `expiry`: (String) New expiration date for the accounts (e.g., `2025-02-01`).

**Command**:

```bash
./01_run -r reset_expire_day.json
```

### 10\. **`remove_vpn.json`**

**Description**: Deletes VPN accounts.

**Parameters**:

* `Enable_Delete_VPN`: (Boolean) Whether to delete VPN accounts.

**Command**:

```bash
./01_run -r remove_vpn.json
```

### 11\. **`copy_rsa_passwd.json`**

**Description**: Copies RSA keys and password files.

**Parameters**:

* `Enable_Generate_RSA_Key`: (Boolean) Whether to generate RSA key pairs for user authentication.
* `Enable_Copy_Files`: (Boolean) Whether to copy the generated RSA key files and password CSVs to designated locations.

**Command**:

```bash
./01_run -r copy_rsa_passwd.json
```

## Example Workflow

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

This Account Management System simplifies the complex task of managing multiple accounts, including user creation, password management, and VPN configuration, with full automation through JSON configuration files. Each JSON file parameter is designed to provide flexibility in managing users, quotas, VPNs, and process groups with minimal effort.


