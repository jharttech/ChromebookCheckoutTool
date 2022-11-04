import sys
import subprocess
import re
import csv
from scripts import new_user_script


class Setup():
    def __init__(self,account_type):
        self.account_type = account_type
        n_file = f"{account_type}/{account_type}.txt"
        subprocess.Popen(["touch",n_file], stdout=subprocess.PIPE)


class Campus_OUs:
    def __init__(self):
        ...


    def ou_dict(self, account_type):
    #ADD on campus and logic to build the dictionary for staff or student
        self.account_type = account_type
        
        if str(self.account_type) == "staff":
            self.ou_type = "Employees"
        else:
            self.ou_type = "Students"
        
        self.org_unit_dict = {}
        #self.all_ou = subprocess.Popen(["gam","print","orgs"], stdout=subprocess.PIPE)
        #self.result = all_ou.stdout.read().decode()
        #self.all_ou.wait()
        #with open(f"needed_file/result.csv", mode='w') as self.temp_file:
            #self.temp_file.write(result)

        with open(f"needed_file/result.csv", mode='r') as self.csv_file_read:
            self.read_file = csv.reader(self.csv_file_read, delimiter=',')
            self.n_col = len(next(self.read_file))
            self.csv_file_read.seek(0)
            self.line_count = 0
            self.dict_key_count = 0
            for row in self.read_file:
                print(f"row is {row}")
                if self.line_count == 0:
                    for x in range(0, self.n_col):
                        self.col_name = str(row[x])
                        if str(self.col_name) == "orgUnitPath":
                            self.num = x
                            self.line_count += 1
                else:
                    self.line_count+=1
                    print(str(self.ou_type))
                    if str(self.ou_type) in row[self.num]:
                        self.dict_key_count += 1
                        self.org_unit_dict.update({str(self.dict_key_count):row[self.num]})
        # listOU = list(subprocess.call(GETOU, shell=True))
        # for x in range(0,len(listOU)):
        #     orgUnitDict.update({x + 1 : listOU[x]})
        # orgUnitDict.update({int(len(listOU)) : "Exit"})
        #Above code needs implimented once on campus
        #self.org_unit_dict = {
            #"1": "Employees",
            #"2": "Admins",
            #"3": "Discovery",
            #"4": "LTSubs",
            #"5": "SecurityStrong",
            #"6": "Technology",
            #"7": "BoardMembers",
            #"8": "Exit"
            #}

        return self.org_unit_dict

    
class Assign_OU:
    def __init__(self, ou):
        self.ou = ou
        
    def __str__(self):
        return self.ou

    @classmethod
    def get(cls, ou_dict):
        #DEBUG print(ou_dict)
        while True:
            choice = input("Please select the desired Org Unit: ")
            if str(choice) not in ou_dict:
                print(f"Invalid entry, please try again! (Enter 1-{len(ou_dict)})")
            else:  
                ou = ou_dict.get(choice)
                return cls(ou)
    
    
class Campus_groups:
    def __init__(self):
        ...
    #Create logic to poll GAM for groups, drop them in a list,
    #then ask the user to input what groups they want the user to
    #be a member of
    #gam print groups

    
    def groups_dict(self):
        self.group_dict = {}
        with open(f"needed_file/group_data.csv", mode='r') as self.csv_file_read:
            self.read_file = csv.reader(self.csv_file_read, delimiter=',')
            self.n_col = len(next(self.read_file))
            self.csv_file_read.seek(0)
            self.line_count = 0
            self.dict_key_count = 0
            for row in self.read_file:
                print(f"row is {row}")
                if self.line_count == 0:
                    for x in range(0, self.n_col):
                        self.col_name = str(row[x])
                        if str(self.col_name) == "Email":
                            self.num = x
                            self.line_count += 1
                else:
                    self.line_count+=1
                    self.dict_key_count += 1
                    self.group_dict.update({str(self.dict_key_count):row[self.num]})
        #self.group_dict = {
         #   "1":"staff_print",
          #  "2":"all_staff",
           # "3":"classroom"
        #}
        return self.group_dict

    
class Assign_groups:
    #Finish this class, may use getter setter 
    def __init__(self, groups):
        self.group_list(groups)

    
    def group_list(self,groups):
        self.groups = groups
        return self.groups
        
        
    @classmethod
    def get(cls,campus_groups):
        assigned_groups = []
        
        group_wanted = input(f"""\nPlease enter the numbers of the groups
the user will need be a member of: (Comma seperated: ex. 1,2,3)\n""")
        group_wanted = group_wanted.split(",")
        for i in range(0,len(group_wanted)):
            assigned_groups.append(campus_groups.get(group_wanted[i]))
        
        return cls(assigned_groups)
            
def dict_print(data):
    print("\n")
    [print(key,':',value) for key, value in data.items()]


class Create_Account:
    def __init__(self,account_type,wanted_ou,groups):
        self.account_type = account_type
        self.sed_params = f"s|$|:{wanted_ou}|"
        self.temp_file = f"{account_type}/temp_{account_type}.txt"

        subprocess.Popen(["touch",self.temp_file], stdout=subprocess.PIPE)
        self.edit_file = subprocess.Popen(["vim",self.temp_file])
        self.edit_file.wait()

        self.copy_file(self.temp_file,self.account_type)

        with open(self.temp_file, mode='w') as file:
            inject_org = subprocess.Popen(["sed","-e",self.sed_params,self.temp_file], stdout=file)
            inject_org.wait()

        self.gam(self.account_type,wanted_ou,groups)

    def copy_file(self,temp_file,account_type):
        cp = subprocess.Popen(["cp",temp_file,f"{account_type}/{account_type}.txt"], stdout=subprocess.PIPE)
        cp.wait()

    def gam(self,account_type,wanted_ou,groups):
        self.account_type = account_type
        self.awk_file = f"{self.account_type}/{self.account_type}.txt"

        if str(self.account_type) == "student":
            self.awk_line = '{print "gam create user "$1" firstname "$2" lastname "$3" password "$4" gal off org "$5" && sleep 2"}'
        elif str(self.account_type) == "staff":
            self.awk_line = '{print "gam create user "$1" firstname "$2" lastname "$3" password "$4" gal on org "$5" && sleep2"}'
        
        self.dry_run = subprocess.Popen(["awk","-F:",self.awk_line,self.awk_file], stdout=subprocess.PIPE)
        self.dry_run.communicate()
        print(f"{self.dry_run}")



def main():
    subprocess.Popen(["clear"], stdout=subprocess.PIPE)
    print("Welcome to the MG Create Account Tool\n")
    account_type = new_user_script.Account_type.get()
    Setup(account_type)
    campus_OUs = Campus_OUs().ou_dict(account_type)
    print(campus_OUs)
    dict_print(campus_OUs)
    OU = Assign_OU(None).get(campus_OUs)
    if str(account_type) == "staff":
        campus_groups = Campus_groups().groups_dict()
        dict_print(campus_groups)
        groups = Assign_groups(None).get(campus_groups)
        Create_Account(account_type,OU,groups)
    else:
        Create_Account(account_type,OU,None)
    print(OU)


if __name__=="__main__":
    main()