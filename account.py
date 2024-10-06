#!/usr/bin/env python2

import os
import random
import string
import subprocess
import json
import shutil
import argparse
import getpass
#==============================================================================#
# vvv Please modify the following variables as needed vvv #
#==============================================================================#
################################################################
# 0 Default Jason file read
################################################################
Enable_read_jason_file = False
Enable_write_jason_file = False
default_read_json_file_path = "delete.json"
default_write_json_file_path = "cylee.json"
################################################################
# 1 Variable must be set before running the script
################################################################
# creator     = "YourName"                              # 1.1 Name of the creator
# course_name = "YourCourse"                            # 1.2 Course name
creator     = "LHLAIB"                                  # 1.1 Name of the creator
course_name = "vlsi"                                   # 1.2 Course name
term        = "2024_Fall"                               # 1.3 Term, e.g., 2024_Fall or 2024_Spring
################################################################
stu_from    = 1                                     # 1.4 Starting student number
stu_to      = 1                                     # 1.5 Ending student number
TA_from     = 0                                     # 1.6 Starting TA number
TA_to       = 0                                     # 1.7 Ending TA number
################################################################
# 2 Account settings (Enable account creation, process group assignment, etc.)
################################################################
# 2.1.0 Create account
################################################################
Enable_Create               = False                   # Enable account creation
course_dir = "/RAID2/COURSE/{}/{}/".format(term,course_name)  # Course directory path
################################################################
# 2.2 Process group assignment
################################################################
Enable_Set_Process_Group    = False                  # Enable process group assignment
process_groups              = ["U18"]                    # Process groups to add users to
Enable_Remove_Process_Group = False                 # Enable process group removal
Remove_process_groups       = ["U18"]                    # Process groups to add users to
# process_groups             = ["C18", "U18", "ADFP"]# Process groups to add users to
################################################################
# 2.3 Password Change settings
################################################################
Enable_Change_Password  = False      # Enable password setting
Random_Password         = True      # True: Random password, False: Set course_name password
prefix                  = "EEHPC"   # Password prefix
special_length          = 3         # Length of special characters in the middle
suffix_length           = 4         # Random suffix length
special_chars           = '!@#$%^&*'# random password = prfix + special + suffix
#random.seed(4)                     # Set random seed if needed
################################################################
# 3 Quota settings (Soft and hard limits for students and TAs)
################################################################
# 3.1 User quota (students and TAs)
################################################################
Enable_Set_User_Quota   = False
student_quota_bsoft     = "30G"     # Student quota soft limit
student_quota_bhard     = "35G"     # Student quota hard limit
ta_quota_bsoft          = "50G"     # TA quota soft limit
ta_quota_bhard          = "55G"     # TA quota hard limit
################################################################
# 3.2 Group quota 
################################################################
Enable_Set_Group_Quota  = False
group_quota_bsoft       = "3T"      # Group quota bsoft
group_quota_bhard       = "3T"      # Group quota bhard
################################################################
# 4 Chage settings for account expiry, inactive period, etc.
################################################################
# 4.1 Account expiry settings
################################################################
Enable_Set_Expire_Day = False
# expiry = "2025-02-01"                       # Account expiry date
# set expirty today to ban the user
expiry = "2024-09-19"                         # Account expiry date
################################################################
# 4.2 Inactive period settings
################################################################
Enable_Set_Days_Inactive = False
# set date as today
# date = "2024-09-19" 
date = subprocess.check_output(["date", "+%Y-%m-%d"]).strip()
inactive_days = 60                          # Inactive period    
################################################################
mindays = 0
maxdays = 180
warndays = 14
last = subprocess.check_output(["date", "-d", "-181 days", "+%s"]).strip()
lastday = int(last) / 86400
################################################################
# 5 File copy settings
################################################################
Enable_Generate_RSA_Key = False              # Enable or disable the RSA key generation
Enable_Copy_Files = False                    # Enable or disable the file copy operation
destination_base = os.path.expanduser("~/Documents/EEHPC_Account/COURSE/")  # Base destination directory for file copies
Enable_Unlock_Account = True               # Enable or disable the account unlock operation
################################################################
# 6 VPN Config Generation
################################################################
Enable_Create_VPN                   = False      # Enable VPN account creation
VPN_Random_Password                 = False      # True: Random password, False: Set course_name password
VPN_password_prefix                 = "EEHPC_VPN"   # Password prefix
VPN_password_special_length         = 3         # Length of special characters in the middle
VPN_password_suffix_length          = 4         # Random suffix length
VPN_password_special_chars          = '!@#$%^&*'# random password = prfix + special + suffix
#random.seed(4)                     # Set random seed if needed


################################################################
# 7.1 Delete account
################################################################
Enable_Delete               = False                  # Enable account deletion
Enable_Backup_HomeDir       = False                   # Enable home directory backup
BackUp_dir                  = "/RAID2/COURSE/BackUp/{}/".format(term)  # Backup directory path

################################################################
# 7.2 VPN Delete
################################################################
Enable_Delete_VPN           = False                  # Enable VPN account deletion   
original_config = """
config user group
    edit "SSLVPN-Group"
        set member "arj"
    next
end
"""
################################################################
#==============================================================================#
# ^^^ Please modify the above variables as needed ^^^ #
#==============================================================================#










################################################################
# Define Color string
################################################################
ERROR = '\033[91m[ERROR] '
INFO = '\033[94m[INFO] '
MESSAGE = '\033[37m[MESSAGE] '
WARNING = '\033[93m[WARNING] '
SUCCESS = '\033[92m[OK] '
ENDC = '\033[0m'
YELLO = '\033[33m'



################################################################
# 2. Account settings Function Definitions
################################################################

# Function to create header in /etc/passwd if enabled
def create_header():
    if Enable_Create:
        command = "echo '# >>> Creator: {}, Term: {}, Course: {}, Date: {}, Exp: {} <<< ' | sudo tee -a /etc/passwd".format(creator, term, course_name, date, expiry)
        subprocess.call(command, shell=True)
        print(MESSAGE + "[{}] [Account] Header added to /etc/passwd.".format(course_name) + ENDC)

# Function to generate random passwords based on prefix, special characters, and suffix length
def generate_random_password():
    if Random_Password:  
        suffix = ''.join(random.choice(string.ascii_letters.replace('i', '').replace('l', '').replace('I', '').replace('L', '').replace('O', '').replace('o', '')  + string.digits.replace('0', '')) for _ in range(suffix_length))
        special = ''.join(random.choice(special_chars) for _ in range(special_length))
        return "{}{}{}".format(prefix, special, suffix)
    else:
        return "{}".format(course_name)

# Function to initialize CSV file for account and password storage
def initialize_csv():
    # check if server passwd directory exists
    if not os.path.exists("./server_passwd"):
        os.makedirs("./server_passwd")
        # change onwer and group to root:Manager for the passwd directory
        command = "sudo chown root:Manager ./server_passwd"
        subprocess.call(command, shell=True)
        # chane permission to 770 for the passwd directory
        command = "sudo chmod 770 ./server_passwd"
        subprocess.call(command, shell=True)
        print(MESSAGE + "[Password] Password directory created." + ENDC)
    if Enable_Change_Password:
        csv_file = "./server_passwd/{}_{}_EEHPC.csv".format(term, course_name)
        command = "echo 'Account,Password' > {}".format(csv_file)
        subprocess.call(command, shell=True)
        # change onwer and group to root:Manager for the csv file
        command = "sudo chown root:Manager {}".format(csv_file)
        # chane permission to 770 for the csv file
        command = "sudo chmod 770 {}".format(csv_file)
        subprocess.call(command, shell=True)
        print(MESSAGE + "[{}] [Password] Password file created.".format(csv_file) + ENDC)

# Function to create course directory if it does not exist
def create_course_directory():
    if Enable_Create:
        if not os.path.exists(course_dir):
            os.makedirs(course_dir)
            print(MESSAGE + "[Directory] '{}' has been created.".format(course_dir) + ENDC)
        else:
            print(WARNING + "[Directory] '{}' already exists.".format(course_dir) + ENDC)

# Function to create course group and set group quota
def create_course_group():
    if Enable_Create or Enable_Set_Group_Quota:
        command = "getent group {} || sudo groupadd {}".format(course_name, course_name)
        subprocess.call(command, shell=True)
        print(WARNING + "[{}] [Group] Group has been created or already exists.".format(course_name) + ENDC)

    if Enable_Set_Group_Quota:
        command = "sudo xfs_quota -x -c 'limit -g bsoft={} bhard={} {}' /RAID2".format(group_quota_bsoft, group_quota_bhard, course_name)
        subprocess.call(command, shell=True)
        print(MESSAGE + "[{}] [Quota] Set bsoft={} and bhard={} as Group quota.".format(course_name, group_quota_bsoft, group_quota_bhard) + ENDC)

# Function to create accounts (students or TAs)
def create_account(role, from_num, to_num, quota_bsoft, quota_bhard):
    # check if from or to is 0
    if from_num == 0:
        return
    if to_num == 0:
        to_num = from_num

    for i in range(from_num, to_num + 1):
        # Format the username
        if role == "student":
            new_user = "{}{:03d}".format(course_name, i)
        else:
            new_user = "{}TA{:02d}".format(course_name, i)

        print("=====================================================================")
        print(INFO + "Processing account '{}'...".format(new_user) + ENDC)
        new_user_dir = os.path.join(course_dir, new_user)

        # Create user if enabled
        if Enable_Create:
            command = "sudo useradd -g {} -d {} -s /bin/tcsh {}".format(course_name, new_user_dir, new_user)
            subprocess.call(command, shell=True)
            print(MESSAGE + "[{}] [Account] User account has been created.".format(new_user) + ENDC)

        # Generate and set password if enabled
        if Enable_Change_Password:
            password = generate_random_password()
            command = "echo '{}' | sudo passwd --stdin {}".format(password, new_user)
            subprocess.call(command, shell=True)
            csv_file = "./server_passwd/{}_{}_EEHPC.csv".format(term, course_name)
            command = "echo '{},{}' >> {}".format(new_user, password, csv_file)
            subprocess.call(command, shell=True)
            print(MESSAGE + "[{}] [Password] set '{}' password for user.".format(new_user, password) + ENDC)

        # Set user quota if enabled
        if Enable_Set_User_Quota:
            command = "sudo xfs_quota -x -c 'limit bsoft={} bhard={} {}' /RAID2".format(quota_bsoft, quota_bhard, new_user)
            subprocess.call(command, shell=True)
            print(MESSAGE + "[{}] [Quota] Set bsoft={} and bhard={} as User quota.".format(new_user, quota_bsoft, quota_bhard) + ENDC)

        # Set account expiry and password settings if enabled
        if Enable_Set_Expire_Day:
            command = "sudo chage --expiredate {} {}".format(expiry, new_user)
            subprocess.call(command, shell=True)
            print(MESSAGE + "[{}] [Expiry] Set '{}' as account expiry date.".format(new_user, expiry) + ENDC)

        # Set inactive period if enabled
        if Enable_Set_Days_Inactive:
            command = "sudo chage --lastday {} --inactive {} --mindays {} --maxdays {} --warndays {} {}".format(lastday, inactive_days, mindays, maxdays, warndays, new_user)
            subprocess.call(command, shell=True)
            print(MESSAGE + "[{}] [Inactive] Set '{}' as inactive period.".format(new_user, inactive_days) + ENDC)

        # Add user to process groups if enabled
        if Enable_Set_Process_Group:
            for group in process_groups:
                command = "sudo gpasswd -a {} {}".format(new_user, group)
                subprocess.call(command, shell=True)
                print(MESSAGE + "[{}] [Process] Added to '{}' group.".format(new_user, group) + ENDC)
        
        # Remove user from process groups if enabled
        if Enable_Remove_Process_Group:
            for group in Remove_process_groups:
                command = "sudo gpasswd -d {} {}".format(new_user, group)
                subprocess.call(command, shell=True)
                print(MESSAGE + "[{}] [Process] Removed from '{}' group.".format(new_user, group) + ENDC)

        # Print account expiry details
        # command = "sudo chage -l {}".format(new_user)
        # subprocess.call(command, shell=True)
        print(SUCCESS + "Processing account '{}' completed.".format(new_user) + ENDC)

################################################################
# 3 Quota settings Function Definitions
################################################################
# Function to report quota usage for the course group
def report_quota_usage():
    print("=====================================================================")
    print(INFO + "Reporting quota usage..." + ENDC)
    command = "sudo xfs_quota -x -c 'report -ugbih' /RAID2 | grep {}".format(course_name)
    subprocess.call(command, shell=True)
    print(INFO + "[{}] [Quota] Quota usage reported.".format(course_name) + ENDC)

################################################################
# 5. File copy settings Function Definitions
################################################################
# Function to generate RSA key pair
def generate_rsa_key():
    if Enable_Generate_RSA_Key:
        print("=====================================================================")
        print(INFO + "Generating RSA key pair..." + ENDC)
        if not os.path.exists("./RSA_key"):
            os.makedirs("./RSA_key")
            # change onwer and group to root:Manager for the RSA key directory
            command = "sudo chown root:Manager ./RSA_key"
            subprocess.call(command, shell=True)
            # chane permission to 770 for the RSA key directory
            command = "sudo chmod 770 ./RSA_key"
            subprocess.call(command, shell=True)
            print(MESSAGE + "[RSA] RSA key directory created." + ENDC)

        # Construct the filename based on term and course
        filename = "./RSA_key/{}_{}.key".format(term, course_name)
        
        # Command to generate RSA key pair
        command = "ssh-keygen -t rsa -b 2048 -f {} -N ''".format(filename)
        subprocess.call(command, shell=True)

        # remove the filename.key.pub file
        command = "rm -f {}.pub".format(filename)
        print(INFO + "Removing public key file: {}.pub".format(filename) + ENDC)
        subprocess.call(command, shell=True)

        # change onwer and group to root:Manager for the RSA key file
        command = "sudo chown root:Manager {}".format(filename)
        subprocess.call(command, shell=True)

        # change permission to 770 for the RSA key file
        command = "sudo chmod 770 {}".format(filename)
        
        # Output message
        print(MESSAGE + "[{}] [Key] RSA key pair has been generated and saved as {}.".format(course_name, filename) + ENDC)

# Function to copy CSV and key files to the destination directory
def copy_files():
    if Enable_Copy_Files:
        print("=====================================================================")
        print(INFO + "Copying files to destination directory..." + ENDC)
        # Construct destination directory path
        destination_dir = os.path.join(destination_base, term, course_name)

        # Command to create the directory if it doesn't exist
        command = "sudo mkdir -p {}".format(destination_dir)
        subprocess.call(command, shell=True)
        print(MESSAGE + "[{}] [Directory] Target directory checked/created.".format(course_name) + ENDC)

        # File paths
        csv_file = "./server_passwd/{}_{}_EEHPC.csv".format(term, course_name)
        key_file = "./RSA_key/{}_{}.key".format(term, course_name)
        if Enable_Create_VPN:
            vpn_csv_file = "./VPN_passwd/{}_{}_VPN.csv".format(term, course_name)

        # Check if CSV file exists and copy it
        if os.path.isfile(csv_file):
            command = "sudo /usr/bin/cp {} {}".format(csv_file, destination_dir)
            subprocess.call(command, shell=True)
            print(MESSAGE + "[{}] [File] CSV file: {} copied to {}.".format(course_name, csv_file, destination_dir) + ENDC)
        else:
            print(WARNING + "[{}] [File] CSV file {} does not exist.".format(course_name, csv_file) + ENDC)

        # Check if Key file exists and copy it
        if os.path.isfile(key_file):
            command = "sudo /usr/bin/cp {} {}".format(key_file, destination_dir)
            subprocess.call(command, shell=True)
            print(MESSAGE + "[{}] [File] Key file: {} copied to {}.".format(course_name, key_file, destination_dir) + ENDC)
        else:
            print(WARNING + "[{}] [File] Key file: {} does not exist.".format(course_name, key_file) + ENDC)

        # Check if VPN CSV file exists and copy it
        if Enable_Create_VPN:
            if os.path.isfile(vpn_csv_file):
                command = "sudo /usr/bin/cp {} {}".format(vpn_csv_file, destination_dir)
                subprocess.call(command, shell=True)
                print(MESSAGE + "[{}] [File] VPN CSV file: {} copied to {}.".format(course_name, vpn_csv_file, destination_dir) + ENDC)
            else:
                print(WARNING + "[{}] [File] VPN CSV file: {} does not exist.".format(course_name, vpn_csv_file) + ENDC)

        # change onwer and group to root:Manager for the entire directory
        command = "sudo chown -R root:Manager {}".format(destination_dir)
        subprocess.call(command, shell=True)
        # change permission to 770 for the entire directory
        command = "sudo chmod -R 770 {}".format(destination_dir)
        subprocess.call(command, shell=True)
        print(SUCCESS + "[File] File copy operation completed." + ENDC)

def rename_files(file_pattern, old_suffix="_old"):
    # Get the directory and file pattern for renaming
    for file in file_pattern:
        if os.path.isfile(file):
            counter = 1
            # Generate a new file name with a counter appended
            new_file = "{}{}_{:02d}{}".format(file[:-4], old_suffix, counter, file[-4:])  # file[-4:] preserves the file extension

            # Increment the counter if the file already exists
            while os.path.exists(new_file):
                counter += 1
                new_file = "{}{}_{:02d}{}".format(file[:-4], old_suffix, counter, file[-4:])

            # Rename the file
            print(MESSAGE + "Renaming file {} to {}.".format(file, new_file) + ENDC)
            shutil.move(file, new_file)
        else:
            print(WARNING + "File {} does not exist.".format(file) + ENDC)

def rename_INFO_files(file_pattern, old_suffix="_old"):
    # Get the directory and file pattern for renaming
    for file in file_pattern:
        if os.path.isfile(file):
            counter = 1
            # Generate a new file name with a counter appended
            new_file = "{}{}_{:02d}{}".format(file[:-5], old_suffix, counter, file[-5:])  # file[-4:] preserves the file extension

            # Increment the counter if the file already exists
            while os.path.exists(new_file):
                counter += 1
                new_file = "{}{}_{:02d}{}".format(file[:-5], old_suffix, counter, file[-5:])

            # Rename the file
            print(MESSAGE + "Renaming file {} to {}.".format(file, new_file) + ENDC)
            shutil.move(file, new_file)
        else:
            print(WARNING + "File {} does not exist.".format(file) + ENDC)

def unlock_account_lock(new_user):
    destination_dir = "/root/Documents/EEHPC_Account/COURSE/{}/{}".format(term, course_name)
    lock_file = "{}/LOCK/{}.lock".format(destination_dir, new_user)

    if os.path.exists(lock_file):
        print(MESSAGE + "Removing lock file {}.".format(lock_file) + ENDC)

        os.remove(lock_file)
    else:
        print(WARNING + "Lock file {} does not exist.".format(lock_file) + ENDC)

def unlock_account(role, from_num, to_num):
    if not Enable_Unlock_Account:
        return
    if from_num == 0:
        return
    if to_num == 0:
        to_num = from_num
    
    destination_dir = "/root/Documents/EEHPC_Account/COURSE/{}/{}".format(term, course_name)
    for i in range(from_num, to_num + 1):
        # Format the username based on the role (student or TA)
        if role == "student":
            new_user = "{}{:03d}".format(course_name, i)
        else:
            new_user = "{}TA{:02d}".format(course_name, i)
        print("=====================================================================")
        print(INFO + "Unlock account '{}'...".format(new_user) + ENDC)
        # Unlock the account lock
        unlock_account_lock(new_user)

        # NDA file renaming
        nda_files = [f for f in os.listdir("{}/NDA".format(destination_dir)) if f.startswith("{}_".format(new_user)) and f.endswith("_NDA.png")]
        rename_files([os.path.join(destination_dir, "NDA", file) for file in nda_files])

        # STU file renaming
        stu_files = [f for f in os.listdir("{}/STU".format(destination_dir)) if f.startswith("{}_".format(new_user)) and f.endswith("_stu.png")]
        rename_files([os.path.join(destination_dir, "STU", file) for file in stu_files])

        # INFO file renaming
        info_files = [f for f in os.listdir("{}/INFO".format(destination_dir)) if f == "{}_info.xlsx".format(new_user)]
        rename_INFO_files([os.path.join(destination_dir, "INFO", file) for file in info_files])

        print(SUCCESS + "Account {} unlocked and files renamed.".format(new_user) + ENDC)



################################################################
# 6 VPN Config Generation Function Definitions
################################################################
def generate_vpn_password():
    if VPN_Random_Password:
        # Generate random suffix and special characters
        suffix = ''.join(random.choice(string.ascii_letters.replace('i', '').replace('l', '').replace('I', '').replace('L', '').replace('O', '').replace('o', '') + string.digits.replace('0', '')) for _ in range(VPN_password_suffix_length))
        special = ''.join(random.choice(VPN_password_special_chars) for _ in range(VPN_password_special_length))
        return "{}{}{}".format(VPN_password_prefix, special, suffix)
    else:
        # If random password generation is disabled, use course_name as prefix
        return "{}".format(course_name)
    
# Function to initialize CSV file for VPN account and password storage
def initialize_vpn_csv():
    if not os.path.exists("./VPN_passwd"):
        os.makedirs("./VPN_passwd")
        # change onwer and group to root:Manager for the VPN passwd directory
        command = "sudo chown root:Manager ./VPN_passwd"
        subprocess.call(command, shell=True)
        # chane permission to 770 for the VPN passwd directory
        command = "sudo chmod 770 ./VPN_passwd"
        subprocess.call(command, shell=True)
        print(MESSAGE + "[VPN] VPN password directory created." + ENDC)
    if Enable_Create_VPN:
        vpn_csv_file = "./VPN_passwd/{}_{}_VPN.csv".format(term, course_name)
        command = "echo 'Account,Password' > {}".format(vpn_csv_file)
        subprocess.call(command, shell=True)
        # change onwer and group to root:Manager for the csv file
        command = "sudo chown root:Manager {}".format(vpn_csv_file)
        subprocess.call(command, shell=True)
        # chane permission to 770 for the csv file
        command = "sudo chmod 770 {}".format(vpn_csv_file)
        subprocess.call(command, shell=True)
        print(MESSAGE + "[{}] [VPN] VPN account file: {} created.".format(course_name, vpn_csv_file) + ENDC)

# Function to append VPN account and password to CSV file
def append_vpn_account_to_csv(account, password):
    vpn_csv_file = "./VPN_passwd/{}_{}_VPN.csv".format(term, course_name)
    command = "echo '{},{}' >> {}".format(account, password, vpn_csv_file)
    subprocess.call(command, shell=True)
    # print(MESSAGE + "[{}] [VPN] set '{}' password for VPN account.".format(account, password) + ENDC)

# Function to create VPN configuration and store account/password
def create_vpn_config():
    if not Enable_Create_VPN:
        return

    # Initialize VPN CSV file
    initialize_vpn_csv()
    # Start VPN configuration
    print("")
    print(WARNING + "[VPN] vvv Please copy the following configuration to FortiGate Console. vvv\n " + ENDC)
    print("+------------------------------------------------------------+")
    vpn_config = []
    vpn_config.append("config user local\n")

    # Create TA VPN accounts
    create_vpn_accounts("TA", TA_from, TA_to, vpn_config)

    # Create Student VPN accounts
    create_vpn_accounts("student", stu_from, stu_to, vpn_config)

    vpn_config.append("end\n")

    # Generate VPN group configuration for SSLVPN-Group
    generate_vpn_group_config( "student", stu_from, stu_to, vpn_config)
    generate_vpn_group_config( "TA", TA_from, TA_to, vpn_config)


    # check if VPN passwd directory exists
    if not os.path.exists("./VPN_config"):
        os.makedirs("./VPN_config")
        # change onwer and group to root:Manager for the VPN config directory
        command = "sudo chown root:Manager ./VPN_config"
        subprocess.call(command, shell=True)
        # chane permission to 770 for the VPN config directory
        command = "sudo chmod 770 ./VPN_config"
        subprocess.call(command, shell=True)
        print(MESSAGE + "[VPN] VPN configuration directory created." + ENDC)

    # Save VPN configuration to file
    vpn_config_file = "./VPN_config/{}_{}_VPN_Config.txt".format(term, course_name)
    with open(vpn_config_file, 'w') as f:
        f.write("\n".join(vpn_config))
    
    # change onwer and group to root:Manager for the VPN config file
    command = "sudo chown root:Manager {}".format(vpn_config_file)
    subprocess.call(command, shell=True)
    # Print config command
    print("\n".join(vpn_config)) 

    print("+------------------------------------------------------------+")
    print(WARNING + "[VPN] ^^^ Please copy the above configuration to FortiGate Console. ^^^\n " + ENDC)

    print(MESSAGE + "[{}] [VPN] VPN configuration saved to {}.".format(course_name, vpn_config_file) + ENDC)


# Helper function to create VPN accounts
def create_vpn_accounts(role, from_num, to_num, vpn_config):
    if from_num == 0:
        return
    if to_num == 0:
        to_num = from_num
    for i in range(from_num, to_num + 1):
        # Format the account name based on role
        if role == "student":
            new_user = "{}{:03d}".format(course_name, i)
        else:
            new_user = "{}TA{:02d}".format(course_name, i)

        # print(INFO + "Processing VPN account '{}'...".format(new_user) + ENDC)

        # Generate password for the VPN account
        password = generate_vpn_password()

        # Add account configuration to the VPN config
        vpn_config.append("edit {}\nset type password\nset passwd {}\nnext".format(new_user, password))

        # Write account and password to CSV using shell command
        append_vpn_account_to_csv(new_user, password)

    #print(SUCCESS + f"VPN accounts for {role} from {from_num} to {to_num} created successfully." + ENDC)

# Helper function to generate VPN group configuration for SSLVPN-Group
def generate_vpn_group_config(role, from_num, to_num, vpn_config):
    if from_num == 0:
        return
    if to_num == 0:
        to_num = from_num
    command = "config user group\nedit SSL-VPN-Group\nappend member "
    
    for i in range(from_num, to_num + 1):
        # Format the account name based on role
        if role == "student":
            new_user = "{}{:03d}".format(course_name, i)
        else:
            new_user = "{}TA{:02d}".format(course_name, i)
        command += new_user + " "
    vpn_config.append(command)
    vpn_config.append("end\n")
    
    # print (MESSAGE + "[VPN] VPN group configuration for SSLVPN-Group created." + ENDC)

################################################################
# 7. Account Deletion Function Definitions
################################################################
# Fucntion to Delete account and VPN account
def delete_all_account():
    # Return if deletion is not enabled
    if not Enable_Delete:
        return
    
    # Backup the entire course directory if backup is enabled
    if Enable_Backup_HomeDir:
        # Define backup path and original course directory path
        backup_course_dir = BackUp_dir
        original_course_dir = course_dir

        # Create the backup directory if it doesn't exist
        if not os.path.exists(backup_course_dir):
            os.makedirs(backup_course_dir)
            print(SUCCESS + "[Directory] '{}' has been created.".format(backup_course_dir) + ENDC)
        else:
            print(WARNING + "[Directory] '{}' already exists.".format(backup_course_dir) + ENDC)

        # Move the course directory to the backup directory
        try:
            shutil.move(original_course_dir, backup_course_dir)
            print(SUCCESS + "Course folder '{}' has been moved to '{}'.".format(original_course_dir, backup_course_dir) + ENDC)
        except Exception as e:
            print(ERROR + "Failed to move course folder '{}': {}".format(original_course_dir, e) + ENDC)
    
    delete_account("student", stu_from, stu_to)
    delete_account("TA", TA_from, TA_to)

    return

# Function to delete accounts (students or TAs)
def delete_account(role, from_num, to_num):
    if from_num == 0:
        return
    if to_num == 0:
        to_num = from_num
    # Loop through the user range
    for i in range(from_num, to_num + 1):
        # Format the username based on the role (student or TA)
        if role == "student":
            new_user = "{}{:03d}".format(course_name, i)
        else:
            new_user = "{}TA{:02d}".format(course_name, i)

        print(INFO + "Processing account '{}'...".format(new_user) + ENDC)



        command = "sudo userdel -f {}".format(new_user)
        print(INFO + "User account '{}' has been deleted.".format(new_user) + ENDC)

        # Execute the deletion command
        subprocess.call(command, shell=True)
        print(MESSAGE + "[{}] [Account] User account has been deleted.".format(new_user) + ENDC)

# Function to delete VPN accounts
def delete_vpn_all_account():
    if not Enable_Delete_VPN:
        return
    delete_vpn_account("student", stu_from, stu_to)
    delete_vpn_account("TA", TA_from, TA_to)
    return       

# Function to delete VPN accounts based on role (student or TA) and range
def delete_vpn_account(role, from_num, to_num):
    if from_num == 0:
        return
    if to_num == 0:
        to_num = from_num
    # Parse the original configuration text to get the user group members
    lines = original_config.split("\n")
    members_line = next(line for line in lines if "set member" in line)
    members = members_line.split()[2:]  # Extract the list of members

    # Create the list of accounts to be deleted based on the role and range
    accounts_to_remove = []
    for i in range(from_num, to_num + 1):
        if role == "TA":
            accounts_to_remove.append('"{}TA{:02d}"'.format(course_name, i))
        elif role == "student":
            accounts_to_remove.append('"{}{:03d}"'.format(course_name, i))

    # Remove the specified accounts from the members list
    updated_members = [member for member in members if member not in accounts_to_remove]

    # Generate new configuration commands
    new_config = []
    new_config.append("config user group\n")
    new_config.append('edit "SSLVPN-Group"\n')
    new_config.append("set member " + " ".join(updated_members) + "\n")
    new_config.append("end\n")

    # Delete accounts from local user configuration
    new_config.append("config user local\n")
    
    # Generate delete commands for the accounts
    for account in accounts_to_remove:
        account_name = account.strip('"')  # Remove quotes around the account
        new_config.append("delete {}\nnext".format(account_name))

    new_config.append("end\n")

    print(WARNING + "[VPN] vvv Please copy the following configuration to FortiGate Console. vvv\n " + ENDC)
    print("+------------------------------------------------------------+")
    print("\n".join(new_config))
    print("+------------------------------------------------------------+")

    return

################################################################
# 8. Ohter Function Definitions
################################################################

# Function to sync NIS accounts after creating user accounts
def sync_nis():
    if Enable_Create or Enable_Change_Password or Enable_Set_Days_Inactive or Enable_Set_Expire_Day or Enable_Delete or Enable_Remove_Process_Group or Enable_Set_Process_Group:
        print("=====================================================================")
        print(INFO + "Syncing NIS accounts..." + ENDC)
        
        commands = [
            "cd /var/yp",
            "sudo make > yp_make.log 2>&1",
            "cd -"
        ]
        
        command = " \n ".join(commands)
        subprocess.call(command, shell=True)
        
        # check if ERROR in yp_make.log
        with open("/var/yp/yp_make.log", "r") as f:
            log = f.read()
            if "ERROR" in log:
                print(ERROR + "NIS accounts synchronization failed. Check /var/yp/yp_make.log for details." + ENDC)
            else:
                print(SUCCESS + "NIS accounts synchronized successfully." + ENDC)


    
################################################################
# 9 Function to display preview in table format
################################################################
def preview():
    print("\n===== Preview: Account Creation Summary =====\n")
    
    # Display account info
    print("1. Account Information")
    print("----------------------------------------------------")
    print("{:<20} | {}".format("Creator", creator))
    print("{:<20} | {}".format("Course Name", course_name))
    print("{:<20} | {}".format("Term", term))
    if stu_from == 0:
        print("{:<20} | {}".format("Student Accounts", "None"))
    elif stu_to == 0 or stu_to == stu_from:
        print("{:<20} | {}{}{:03d}{}".format("Student Accounts", YELLO, course_name, int(stu_from), ENDC))
    else:
        print("{:<20} | {}{}{:03d}{} ~ {}{}{:03d}{}".format("Student Accounts", YELLO, course_name, int(stu_from), ENDC, YELLO, course_name, int(stu_to), ENDC))
    if TA_from == 0:
        print("{:<20} | {}".format("TA Accounts", "None"))
    elif TA_to == 0 or TA_to == TA_from:
        print("{:<20} | {}{}TA{:02d}{}".format("TA Accounts", YELLO, course_name, int(TA_from), ENDC))
    else:
        print("{:<20} | {}{}TA{:02d}{} ~ {}{}TA{:02d}{}".format("TA Accounts", YELLO, course_name, int(TA_from), ENDC, YELLO, course_name, int(TA_to), ENDC))
    print("----------------------------------------------------\n\n")
    
    if not (Enable_Delete or Enable_Delete_VPN):

        # Display enabled actions
        print("2. Enabled Actions")
        print("----------------------------------------------------")
        # Create Account
        print("{:<20} | {}".format("Create Account", "Yes" if Enable_Create else "No"))
        if Enable_Create:
            print("{:<20} | {}".format("Course Directory", course_dir))
        
        # Divider
        print("----------------------------------------------------")
        
        # Password Change
        print("{:<20} | {}".format("Password Change", "Yes" if Enable_Change_Password else "No"))
        
        if Enable_Change_Password:
            print("{:<20} | {}".format("Random Password", "Yes" if Random_Password else "No"))
            if Random_Password:
                print("{:<20} | {}".format("Password Format", "{} + special({}) + suffix({})".format(prefix, special_length, suffix_length)))
            else:
                print("{:<20} | {}".format("Password Format", "Course Name"))
        
        # Divider
        print("----------------------------------------------------")
        
        # User Quota
        print("{:<20} | {}".format("Set User Quota", "Yes" if Enable_Set_User_Quota else "No"))
        if Enable_Set_User_Quota:
            print("{:<20} | {}".format("Student Quota", "Soft: {}{}{} Hard: {}{}{}".format(YELLO, student_quota_bsoft, ENDC, YELLO, student_quota_bhard, ENDC)))
            print("{:<20} | {}".format("TA Quota", "Soft: {}{}{} Hard: {}{}{}".format(YELLO, ta_quota_bsoft, ENDC, YELLO, ta_quota_bhard, ENDC)))
        
        # Divider
        print("----------------------------------------------------")
        
        # Group Quota
        print("{:<20} | {}".format("Set Group Quota", "Yes" if Enable_Set_Group_Quota else "No"))
        if Enable_Set_Group_Quota:
            print("{:<20} | {}".format("Group Quota", "Soft: {} Hard: {}".format(group_quota_bsoft, group_quota_bhard)))
        
        # Divider
        print("----------------------------------------------------")
        
        # Account Expiry
        print("{:<20} | {}".format("Set Account Expiry", "Yes" if Enable_Set_Expire_Day else "No"))
        if Enable_Set_Expire_Day:
            print("{:<20} | {}".format("Account Expiry Date", expiry))
        
        # Divider
        print("----------------------------------------------------")
        
        # Inactive Period
        print("{:<20} | {}".format("Set Inactive Period", "Yes" if Enable_Set_Days_Inactive else "No"))
        if Enable_Set_Days_Inactive:
            print("{:<20} | {}".format("Inactive Period", "{} days".format(inactive_days)))
        
        # Divider
        print("----------------------------------------------------")
        
        # Process Groups
        print("{:<20} | {}".format("Set Process Groups", "Yes" if Enable_Set_Process_Group else "No"))
        
        if Enable_Set_Process_Group and process_groups:
            print("{:<20} | {}".format("Process Groups", ', '.join(process_groups)))

        # Divider
        print("----------------------------------------------------")

        # VPN Configuration
        print("{:<20} | {}".format("Create VPN Accounts", "Yes" if Enable_Create_VPN else "No"))
        if Enable_Create_VPN:
            print("{:<20} | {}".format("VPN Password Format", "{} + special({}) + suffix({})".format(VPN_password_prefix, VPN_password_special_length, VPN_password_suffix_length)))
        
        # Divider
        print("----------------------------------------------------")

        # RSA Key Generation
        print("{:<20} | {}".format("Generate RSA Key", "Yes" if Enable_Generate_RSA_Key else "No"))
        if Enable_Generate_RSA_Key:
            print("{:<20} | {}".format("Key File", "{}_{}.key".format(term, course_name)))
        
        # Divider
        print("----------------------------------------------------")

        # Copy Files
        print("{:<20} | {}".format("Copy Files", "Yes" if Enable_Copy_Files else "No"))
        if Enable_Copy_Files:
            print("{:<20} | {}".format("Destination", destination_base))

        # Divider
        print("----------------------------------------------------")

        # Unlock Account
        print("{:<20} | {}".format("Unlock Account", "Yes" if Enable_Unlock_Account else "No"))



        print("----------------------------------------------------\n\n")

    else:
        # Display enabled actions
        print("2. Delete Actions")
        print("----------------------------------------------------")
        # Create Account
        print("{:<20} | {}".format("Delete Account", "Yes" if Enable_Delete else "No"))
        print("{:<20} | {}".format("Delete VPN Account", "Yes" if Enable_Delete_VPN else "No"))
        if Enable_Delete and Enable_Backup_HomeDir:
            print("{:<20} | {}".format("BackUp ", "Yes"))
            print("{:<20} | {}".format("Course Directory", course_dir))
            print("{:<20} | {}".format("BackUp Directory", BackUp_dir))

        # Divider
        print("----------------------------------------------------")
    
    if Enable_Remove_Process_Group or Enable_Set_Process_Group:
        print("3. Process Group Actions")
        print("----------------------------------------------------")
        print("{:<20} | {}".format("Add Process Group", "Yes" if Enable_Set_Process_Group else "No"))
        if Enable_Set_Process_Group:
            for group in process_groups:
                print("----------------------------------------------------")
                print("{:<20} | {}".format("Current Group", group))
                print("----------------------------------------------------")
                command = "getent group {}".format(group)
                subprocess.call(command, shell=True)
        print("{:<20} | {}".format("Remove Process Group", "Yes" if Enable_Remove_Process_Group else "No"))
        if Enable_Remove_Process_Group:
            for group in Remove_process_groups:
                print("----------------------------------------------------")
                print("{:<20} | {}".format("Current Group", group))
                print("----------------------------------------------------")
                command = "getent group {}".format(group)
                subprocess.call(command, shell=True)
        print("----------------------------------------------------\n\n")

    print("===== End of Preview =====\n")

    
################################################################
# 10 Function to display activation info with structured formatting
################################################################
def activation_info():
    # Structured email-friendly formatting without color codes
    print("\n===== ACTIVATION INFORMATION =====\n")
    
    # System and account information
    print("----------------------------------------------------")
    print("NYCU EEHPC Account Activation System (NYCU IP Only)")
    print("Please use the following settings to activate accounts:")
    print("----------------------------------------------------")
    print("URL: http://ee20.si2.iee.nycu.edu.tw:6060/")
    print("----------------------------------------------------")
    print("{:<25}: {}".format("Account Type", "Course Account"))
    print("{:<25}: {}".format("Course Code", course_name))
    print("{:<25}: {}".format("Semester", term))  
    print("----------------------------------------------------")

    # Student account availability
    if stu_from == 0 or stu_to == 0:
        print("{:<25}: {}".format("Student Accounts", "None"))
    else:
        print("{:<25}: {}{:03d} ~ {}{:03d}".format("Student Accounts", course_name, stu_from, course_name, stu_to))
    
    # TA account availability
    if TA_from == 0 or TA_to == 0:
        print("{:<25}: {}".format("TA Accounts", "None"))
    else:
        print("{:<25}: {}TA{:02d} ~ {}TA{:02d}".format("TA Accounts", course_name, TA_from, course_name, TA_to))

    print("----------------------------------------------------")
    
    # Key file information
    print("{:<25}: {}_{}.key".format("Upload Key File", term, course_name))
    print("Please use the attached key file to complete key authentication.")
    print("----------------------------------------------------")

    # Account distribution information
    print("Please assign the accounts manually and notify students to log in and bind their accounts to obtain VPN and server passwords.")
    print("\n===== END OF ACTIVATION INFORMATION =====\n")


################################################################
# 11 Function to load variables from a selected JSON file
################################################################
def load_json(json_file):
    if json_file:
        if json_file:
            with open(json_file, 'r') as f:
                data = json.load(f)

                # Load data into corresponding variables based on categories, with defaults if not found
                global creator, course_name, term, stu_from, stu_to, TA_from, TA_to
                creator = data.get("course_info", {}).get("creator", "YourName")
                course_name = data.get("course_info", {}).get("course_name", "YourCourse")
                term = data.get("course_info", {}).get("term", "2024_Fall")
                stu_from = data.get("course_info", {}).get("stu_from", 1)
                stu_to = data.get("course_info", {}).get("stu_to", 1)
                TA_from = data.get("course_info", {}).get("TA_from", 1)
                TA_to = data.get("course_info", {}).get("TA_to", 1)

                global Enable_Create, course_dir, Enable_Set_Process_Group, process_groups, Enable_Remove_Process_Group, Remove_process_groups
                Enable_Create = data.get("account_settings", {}).get("Enable_Create", False)
                course_dir = data.get("account_settings", {}).get("course_dir", "/RAID2/COURSE/{}/{}".format(term, course_name))
                Enable_Set_Process_Group = data.get("account_settings", {}).get("Enable_Set_Process_Group", False)
                process_groups = data.get("account_settings", {}).get("process_groups", [])
                Enable_Remove_Process_Group = data.get("account_settings", {}).get("Enable_Remove_Process_Group", False)
                Remove_process_groups = data.get("account_settings", {}).get("Remove_process_groups", [])

                global Enable_Change_Password, Random_Password, prefix, special_length, suffix_length, special_chars
                Enable_Change_Password = data.get("password_settings", {}).get("Enable_Change_Password", False)
                Random_Password = data.get("password_settings", {}).get("Random_Password", True)
                prefix = data.get("password_settings", {}).get("prefix", "EEHPC")
                special_length = data.get("password_settings", {}).get("special_length", 3)
                suffix_length = data.get("password_settings", {}).get("suffix_length", 4)
                special_chars = data.get("password_settings", {}).get("special_chars", '!@#$%^&*')

                global Enable_Set_User_Quota, student_quota_bsoft, student_quota_bhard, ta_quota_bsoft, ta_quota_bhard
                Enable_Set_User_Quota = data.get("quota_settings", {}).get("Enable_Set_User_Quota", False)
                student_quota_bsoft = data.get("quota_settings", {}).get("student_quota_bsoft", "30G")
                student_quota_bhard = data.get("quota_settings", {}).get("student_quota_bhard", "35G")
                ta_quota_bsoft = data.get("quota_settings", {}).get("ta_quota_bsoft", "50G")
                ta_quota_bhard = data.get("quota_settings", {}).get("ta_quota_bhard", "55G")

                global Enable_Set_Group_Quota, group_quota_bsoft, group_quota_bhard
                Enable_Set_Group_Quota = data.get("group_quota_settings", {}).get("Enable_Set_Group_Quota", False)
                group_quota_bsoft = data.get("group_quota_settings", {}).get("group_quota_bsoft", "3T")
                group_quota_bhard = data.get("group_quota_settings", {}).get("group_quota_bhard", "3T")

                global Enable_Set_Expire_Day, expiry, Enable_Set_Days_Inactive, date, inactive_days, mindays, maxdays, warndays, lastday
                Enable_Set_Expire_Day = data.get("chage_settings", {}).get("Enable_Set_Expire_Day", False)
                expiry = data.get("chage_settings", {}).get("expiry", "2025-02-01")
                Enable_Set_Days_Inactive = data.get("chage_settings", {}).get("Enable_Set_Days_Inactive", False)
                date = data.get("chage_settings", {}).get("date", "2024-09-12")
                inactive_days = data.get("chage_settings", {}).get("inactive_days", 60)
                mindays = data.get("chage_settings", {}).get("mindays", 0)
                maxdays = data.get("chage_settings", {}).get("maxdays", 180)
                warndays = data.get("chage_settings", {}).get("warndays", 14)
                lastday = data.get("chage_settings", {}).get("lastday", 0)

                global Enable_Generate_RSA_Key, Enable_Copy_Files, destination_base, Enable_Unlock_Account
                Enable_Generate_RSA_Key = data.get("file_settings", {}).get("Enable_Generate_RSA_Key", False)
                Enable_Copy_Files = data.get("file_settings", {}).get("Enable_Copy_Files", False)
                destination_base = data.get("file_settings", {}).get("destination_base", "~/Documents/EEHPC_Account/COURSE/")
                Enable_Unlock_Account = data.get("file_settings", {}).get("Enable_Unlock_Account", False)

                global Enable_Create_VPN, VPN_Random_Password, VPN_password_prefix, VPN_password_special_length, VPN_password_suffix_length, VPN_password_special_chars
                Enable_Create_VPN = data.get("vpn_settings", {}).get("Enable_Create_VPN", False)
                VPN_Random_Password = data.get("vpn_settings", {}).get("VPN_Random_Password", False)
                VPN_password_prefix = data.get("vpn_settings", {}).get("VPN_password_prefix", "EEHPC_VPN")
                VPN_password_special_length = data.get("vpn_settings", {}).get("VPN_password_special_length", 3)
                VPN_password_suffix_length = data.get("vpn_settings", {}).get("VPN_password_suffix_length", 4)
                VPN_password_special_chars = data.get("vpn_settings", {}).get("VPN_password_special_chars", '!@#$%^&*')

                global Enable_Delete, Enable_Backup_HomeDir, BackUp_dir, Enable_Delete_VPN, original_config
                Enable_Delete = data.get("delete_settings", {}).get("Enable_Delete", False)
                Enable_Backup_HomeDir = data.get("delete_settings", {}).get("Enable_Backup_HomeDir", False)
                BackUp_dir = data.get("delete_settings", {}).get("BackUp_dir", "/RAID2/COURSE/BackUp/{}/".format(term))
                Enable_Delete_VPN = data.get("delete_settings", {}).get("Enable_Delete_VPN", False)
                original_config = data.get("delete_settings", {}).get("original_config", "config user group\nedit SSLVPN-Group\nset member 'arj'\nnext\nend")

            print(SUCCESS + "Configuration loaded from {}".format(json_file) + ENDC)
        else:
            print(WARNING + "No file selected. Using default values." + ENDC)


def save_to_json(save_file):

    data = {
        "course_info": {
            "creator": creator,
            "course_name": course_name,
            "term": term,
            "stu_from": stu_from,
            "stu_to": stu_to,
            "TA_from": TA_from,
            "TA_to": TA_to
        },
        "account_settings": {
            "Enable_Create": Enable_Create,
            "course_dir": course_dir,
            "Enable_Set_Process_Group": Enable_Set_Process_Group,
            "process_groups": process_groups,
            "Enable_Remove_Process_Group": Enable_Remove_Process_Group,
            "Remove_process_groups": Remove_process_groups
        },
        "password_settings": {
            "Enable_Change_Password": Enable_Change_Password,
            "Random_Password": Random_Password,
            "prefix": prefix,
            "special_length": special_length,
            "suffix_length": suffix_length,
            "special_chars": special_chars
        },
        "quota_settings": {
            "Enable_Set_User_Quota": Enable_Set_User_Quota,
            "student_quota_bsoft": student_quota_bsoft,
            "student_quota_bhard": student_quota_bhard,
            "ta_quota_bsoft": ta_quota_bsoft,
            "ta_quota_bhard": ta_quota_bhard
        },
        "group_quota_settings": {
            "Enable_Set_Group_Quota": Enable_Set_Group_Quota,
            "group_quota_bsoft": group_quota_bsoft,
            "group_quota_bhard": group_quota_bhard
        },
        "chage_settings": {
            "Enable_Set_Expire_Day": Enable_Set_Expire_Day,
            "expiry": expiry,
            "Enable_Set_Days_Inactive": Enable_Set_Days_Inactive,
            "date": date,
            "inactive_days": inactive_days,
            "mindays": mindays,
            "maxdays": maxdays,
            "warndays": warndays,
            "lastday": lastday
        },
        "file_settings": {
            "Enable_Generate_RSA_Key": Enable_Generate_RSA_Key,
            "Enable_Copy_Files": Enable_Copy_Files,
            "destination_base": destination_base,
            "Enable_Unlock_Account": Enable_Unlock_Account
        },
        "vpn_settings": {
            "Enable_Create_VPN": Enable_Create_VPN,
            "VPN_Random_Password": VPN_Random_Password,
            "VPN_password_prefix": VPN_password_prefix,
            "VPN_password_special_length": VPN_password_special_length,
            "VPN_password_suffix_length": VPN_password_suffix_length,
            "VPN_password_special_chars": VPN_password_special_chars
        },
        "delete_settings": {
            "Enable_Delete": Enable_Delete,
            "Enable_Backup_HomeDir": Enable_Backup_HomeDir,
            "BackUp_dir": BackUp_dir,
            "Enable_Delete_VPN": Enable_Delete_VPN,
            "original_config": original_config
        }
    }

    if save_file:
        with open(save_file, 'w') as f:
            json.dump(data, f, indent=4)
        print(SUCCESS + "Configuration saved to {}".format(save_file) + ENDC)

def update_config():
    global course_dir, BackUp_dir
    course_dir = "/RAID2/COURSE/{}/{}".format(term, course_name)
    BackUp_dir = "/RAID2/COURSE/BackUp/{}/".format(term)

################################################################
# 12 Main Execution
################################################################

def main():
    parser = argparse.ArgumentParser(description="Process account management JSON configuration.")
    parser.add_argument('-r', '--read', help="Specify the JSON file to read", type=str)
    parser.add_argument('-w', '--write', help="Specify the JSON file to write", type=str)

    args = parser.parse_args()

    # Read from JSON file if provided
    if args.read:
        load_json(args.read)
    else:
        if Enable_read_jason_file:
            load_json(default_read_json_file_path)


    # Save to JSON file if provided
    if args.write:
        save_to_json(args.write)
    elif Enable_write_jason_file:
        save_to_json(default_write_json_file_path)


    preview()  
    # Ask for confirmation to proceed
    confirm = raw_input("Do you want to proceed with the account creation? (yes to proceed): ").lower()
    if confirm == 'yes':
        print("=====================================================================")
        print(INFO + "Proceeding with account creation/deletion/modification..." + ENDC)
    else:
        print(WARNING + "Operation aborted by user." + ENDC)
        return False

    if Enable_Delete or Enable_Delete_VPN:
        delete_all_account()
        delete_vpn_all_account()
        
    else:
        create_header()
        initialize_csv()
        create_course_directory()
        create_course_group()
        # Create student accounts
        create_account("student", stu_from, stu_to, student_quota_bsoft, student_quota_bhard)
        # Create TA accounts
        create_account("TA", TA_from, TA_to, ta_quota_bsoft, ta_quota_bhard)
        # Report quota usage
        if Enable_Set_User_Quota or Enable_Set_Group_Quota:
            report_quota_usage()
        # Sync NIS Client
        sync_nis()  
        # Generate RSA key pair and copy files
        generate_rsa_key()
        copy_files()
        # unlock account
        unlock_account("student", stu_from, stu_to)
        unlock_account("TA", TA_from, TA_to)
        # Create VPN accounts and configuration
        create_vpn_config()
    print("=====================================================================")
    preview()
    # Display activation information
    # if Enable_Create:
    #     activation_info()
    

# Run the main function
if __name__ == "__main__":
    main()


# Useful commands for reference

# sudo xfs_quota -x -c "report -ugbih" /RAID2 | grep iclab
# sudo xfs_quota -x -c "limit -g bsoft=3T bhard=3T iclab" /RAID2
# sudo xfs_quota -x -c "limit bsoft=30G bhard=35G iclab001" /RAID2

# sudo chage -e 2025-02-01 iclab001
# sudo chage -d 0 iclab001
# sudo chage -l username

# sudo gpasswd -a iclab001 C18
# sudo gpasswd -d iclab001 C18

# sudo useradd -g iclab -d /RAID2/COURSE/iclab -s /bin/tcsh iclab001
# sudo groupadd iclab
# sudo echo "password" | passwd --stdin iclab001
# sudo userdel iclab001
# sudo chsh -s /bin/tcsh iclab001
# sudo chsh -s /bin/bash iclab001

