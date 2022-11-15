import sys
import subprocess
import re
import csv
import new_user_script
import datetime


# The Setup Class creates the needed Directory and then creates an empyt file that will be needed
class Setup:
    def __init__(self, account_type):
        # Create a directory with the account type the user chose
        subprocess.Popen(["mkdir",str(account_type)], stdout=subprocess.DEVNULL)
        subprocess.Popen(["mkdir", "logs"], stdout=subprocess.DEVNULL)
        self.account_type = account_type
        # Assign the new file and path to a variable
        n_file = (str(account_type) + "/" + str(account_type) + ".txt")
        # Create the empty file 
        subprocess.Popen(["touch", n_file], stdout=subprocess.DEVNULL)


# The Campus_OUs class gathers the campus OU's and puts them into a dictionary with numeric keys
class Campus_OUs:
    # We do not need the init method for this class so we move on
    def __init__(self):
        ...

    # The ou_dict method takes only the relevant Org Units for the desired account type and
    # Assigns them to a dictionary with numeric keys
    def ou_dict(self, account_type):
        self.account_type = account_type

        if str(self.account_type) == "staff":
            self.ou_type = "Employees"
        else:
            self.ou_type = "Students"

        self.org_unit_dict = {}

        # This will need changed when in production, rather than just read from a file
        # This will poll for the Org Units from GAM, then read the subprocess stdout
        # And assign the results to the results file first
        with open("needed_file/result.csv", mode="r") as self.csv_file_read:
            self.read_file = csv.reader(self.csv_file_read, delimiter=",")
            # Read the number of columns
            self.n_col = len(next(self.read_file))
            # Return the reader back to start of file
            self.csv_file_read.seek(0)
            # Keep track of line
            self.line_count = 0
            # Keep track of numeric value of the key
            self.dict_key_count = 0
            for row in self.read_file:
                if self.line_count == 0:
                    # Look through columns
                    for x in range(0, self.n_col):
                        # Set the column name to the header value of each column
                        self.col_name = str(row[x])
                        # Find the number of the column that has the header name of orgUnitPath
                        if str(self.col_name) == "orgUnitPath":
                            self.num = x
                            # Increase line count
                            self.line_count += 1
                else:
                    self.line_count += 1
                    if str(self.ou_type) in row[self.num]:
                        # Increase the key count so the numeric values start at 1 and not 0
                        self.dict_key_count += 1
                        # Add the numberic key and the value to the dictionary of Org Units
                        self.org_unit_dict.update(
                            {str(self.dict_key_count): row[self.num]}
                        )

        return self.org_unit_dict


# The Assign_OU class askes the user which Org Unit they want to assign the new user(s) to.
class Assign_OU:
    def __init__(self, ou):
        self.ou = ou

    def __str__(self):
        return self.ou

    @classmethod
    # Create the get class method to take the users input
    def get(cls, ou_dict):
        # Create a loop to help with invalid inputs
        while True:
            choice = input("Please select the desired Org Unit: ")
            # Check to see if the input matches any of the keys
            if str(choice) not in ou_dict:
                # If user input was not in the numeric keys, prompt them to enter a number
                # Between 1 and the length of the dictionary
                print("Invalid entry, please try again! (Enter 1-" + len(ou_dict))
            else:
                ou = ou_dict.get(choice)
                return cls(ou)


# The Campus_groups class poll GAM for the campus groups, then assignes them as values to a numeric key
class Campus_groups:
    def __init__(self):
        ...

    # The groups_dict method in production will poll GAM for the campus groups
    # Put the stdout into a file, then read the file to create the desired dictionary
    def groups_dict(self):
        self.group_dict = {}
        # Open the group_data file for reading
        with open("needed_file/group_data.csv", mode="r") as self.csv_file_read:
            self.read_file = csv.reader(self.csv_file_read, delimiter=",")
            # Read the number of columns
            self.n_col = len(next(self.read_file))
            # Move the reader back to the start of the file
            self.csv_file_read.seek(0)
            # Keep track of the lines
            self.line_count = 0
            # Keep count for the numeric dictionary keys
            self.dict_key_count = 0
            for row in self.read_file:
                if self.line_count == 0:
                    # Loop through the header columns
                    for x in range(0, self.n_col):
                        # Assing col_name to each header column value
                        self.col_name = str(row[x])
                        # Look for the number of the column thats header value is Email
                        if str(self.col_name) == "Email":
                            self.num = x
                            self.line_count += 1
                else:
                    self.line_count += 1
                    self.dict_key_count += 1
                    # Write the keys and values to the dictionary
                    self.group_dict.update({str(self.dict_key_count): row[self.num]})
        
        # Append the NO GROUPS value to the dictionary        
        self.group_dict.update({str(self.dict_key_count + 1): "NO GROUPS"})

        return self.group_dict

# The Assign_groups class askes the user what groups they user needs to be a part of if
class Assign_groups:
    def __init__(self, assigned_groups, account_type):
        self.assigned_groups = assigned_groups
        self.account_type = account_type
        self.groups = assigned_groups
        if "NO GROUPS" in str(self.groups):
             return
        # start the Add_to_group Class
        Add_to_group(self.groups, self.account_type)

    @classmethod
    # Create the get method so the user can input which groups are needed for the user
    def get(cls, campus_groups, account_type):
        assigned_groups = []

        # Take user input of the keys for which groups are needed.
        ## NOTE strip out whitespace incase user inputs spaces and use regex to check input
        group_wanted = input(
            """\nPlease enter the numbers of the groups
the user will need be a member of: (Comma seperated: ex. 1,2,3)\n"""
        )
        group_wanted = group_wanted.split(",")
        for i in range(0, len(group_wanted)):
            assigned_groups.append(campus_groups.get(group_wanted[i]))

        return cls(assigned_groups, account_type)


class Add_to_group:
    def __init__(self, groups, account_type):
        self.groups = groups
        with open(str(account_type) + "/" + str(account_type) + ".txt") as self.file:
            self.reader = csv.reader(self.file, delimiter=":")
            for row in self.reader:
                for x in range(0, len(self.groups)):
                    try:
                        self.run_gam = subprocess.Popen(
                            ["gam", "update", "group", str(self.groups[x]),"add", "user", str(row[0])], stdout=subprocess.PIPE
                        )
                        self.run_gam.wait()
                    except FileNotFoundError as e:
                        raise (e)


class Create_Account:
    def __init__(self, account_type, wanted_ou):
        #self.account_type = account_type
        self.account_type = str(account_type)
        self.wanted_ou = str(wanted_ou)
        if "&" in self.wanted_ou:
             self.wanted_ou = self.wanted_ou.replace("&", "\&")
        self.sed_params = "s,$,:" + self.wanted_ou + ","
        self.temp_file = self.account_type + "/temp_" + self.account_type + ".txt"
        self.awk_file = self.account_type + "/" + self.account_type + ".txt"
        subprocess.Popen(["touch", self.temp_file], stdout=subprocess.PIPE)
        self.edit_file = subprocess.Popen(["vim", self.temp_file])
        self.edit_file.wait()

        self.copy_file(self.temp_file, self.awk_file)

        with open(self.awk_file, mode="w") as self.file:
            self.inject_org = subprocess.Popen(
                ["sed", "-e", self.sed_params, self.temp_file], stdout=self.file
            )
            self.inject_org.wait()
            self.inject_org.communicate()


        self.gam(self.account_type, self.wanted_ou, self.awk_file)

    def copy_file(self, temp_file, awk_file):
        cp = subprocess.Popen(["cp", temp_file, awk_file], stdout=subprocess.PIPE)
        cp.wait()

    def gam(self, account_type, wanted_ou, awk_file):
        self.account_type = account_type
        self.wanted_ou = str(wanted_ou)
        self.awk_file = awk_file

        if str(self.account_type) == "student":
            self.awk_line = '{print "gam create user "$1" firstname "$2" lastname "$3" password "$4" gal off org \'"$5"\' && sleep 2"}'
        elif str(self.account_type) == "staff":
            self.awk_line = '{print "gam create user "$1" firstname "$2" lastname "$3" password "$4" gal on org \'"$5"\' && sleep 2"}'

        self.dry_run = subprocess.Popen(
            ["awk", "-F:", self.awk_line, self.awk_file], stdout=subprocess.PIPE
        )
        self.gam_command = str(self.dry_run.stdout.read().decode())
        print(str(self.gam_command))

        while True:
            yn = input("Does the above command look correct? y/n ").lower()
            if not re.search(r"^(y|n)$", yn):
                print("Invalid response please enter 'y' or 'n'")
            else:
                break

        if yn == "n":
            self.__init__(account_type, wanted_ou)
        else:
            try:
                 self.holder = subprocess.Popen(
                    ["awk","-F:", self.awk_line, self.awk_file], stdout=subprocess.PIPE
                 )
                 self.run = subprocess.Popen(
                    ["sh"], stdin=self.holder.stdout, stdout=subprocess.PIPE
                 )
                 #print(self.run.stdout.read().decode())
                 self.run.wait()
            except FileNotFoundError as e:
                raise (e)

def log_file(account_type):
    account_type = str(account_type)
    filepath = (account_type + "/" + account_type + ".txt")
    x = datetime.datetime.now()
    log_file_name = (
        "logs/" + account_type + "-" + str(x.year) + str(x.month) + str(x.day) + str(x.hour) + str(x.minute) + str(x.second)
    )
    create_log = subprocess.Popen(
        ["cp", filepath, log_file_name], stdout=subprocess.PIPE
    )
    create_log.wait()


def dict_print(data):
    print("\n")
    data_list = list(map(int,data))
    data_list = sorted(data_list)
    for i in range(0,len(data)):
         print(str(data_list[i]) + " : " + data.get(str(data_list[i])))
    #[print(key, ":", value) for key, value in data.items()]
    #print(sorted(data.items()))

def main():
    subprocess.Popen(["clear"], stdout=subprocess.PIPE)
    print("Welcome to the MG Create Account Tool\n")
    account_type = new_user_script.Account_type.get()
    Setup(account_type)
    campus_OUs = Campus_OUs().ou_dict(account_type)
    dict_print(campus_OUs)
    OU = Assign_OU(None).get(campus_OUs)
    Create_Account(account_type, OU)
    campus_groups = Campus_groups().groups_dict()
    dict_print(campus_groups)
    Assign_groups.get(campus_groups, account_type)
    log_file(account_type)

    while True:
        restart = input(
            "Account creations and group additions sucessfull. Would you like to create more accounts? y/n "
        ).lower()
        if not re.search(r"^(y|n)$", restart):
            print("Invalid response please enter 'y' or 'n'")
        else:
            break
    if str(restart) == "y":
        main()
    else:
        sys.exit("Thank you!  -Jhart")


if __name__ == "__main__":
    main()
