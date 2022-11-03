import sys
import subprocess
import re
from scripts import new_user_script


class Setup():
    def __init__(self,account_type):
        self.account_type = account_type
        n_file = f"{account_type}/{account_type}.txt"
        subprocess.Popen(["touch",n_file], stdout=subprocess.PIPE)


class Campus_OUs:
    def __init__(self):
        ...


    def ou_dict(self):
    #ADD on campus and logic to build the dictionary for staff or student
        #all_ou = subprocess.Popen(["gam","print","orgs"], stdout=subprocess.DEVNULL)
        #print(all_ou)
        # GETOU = "gam print orgs"
        # listOU = list(subprocess.call(GETOU, shell=True))
        # for x in range(0,len(listOU)):
        #     orgUnitDict.update({x + 1 : listOU[x]})
        # orgUnitDict.update({int(len(listOU)) : "Exit"})
        #Above code needs implimented once on campus
        self.org_unit_dict = {
            "1": "Employees",
            "2": "Admins",
            "3": "Discovery",
            "4": "LTSubs",
            "5": "SecurityStrong",
            "6": "Technology",
            "7": "BoardMembers",
            "8": "Exit"
            }

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

    
class Assign_groups:
    def __init__(self, staff_print, all_staff, classroom):
        self.staff_print = staff_print
        self.all_staff = all_staff
        self.classroom = classroom
        
    @classmethod
    def get(cls,):
        assigned_groups = []
        
        def response(answer):
            if not re.search(r"^(y|n)$", answer):
                print("Invalid response, please answer 'y' or 'n'.")
            else:
                return True
                
        while True:
            staff_print = input(f"\nDoes the employee need to cloud print? (y/n): ").lower()
            if response(staff_print):
                break
            if staff_print == 'y':
                assigned_groups.append('staff_print')
        
        return assigned_groups
            
def dict_print(data):
    print("\n")
    [print(key,':',value) for key, value in data.items()]


def main():
    subprocess.Popen(["clear"], stdout=subprocess.PIPE)
    print("Welcome to the MG Create Account Tool\n")
    account_type = new_user_script.Account_type.get()
    Setup(account_type)
    campus_OUs = Campus_OUs().ou_dict()
    dict_print(campus_OUs)
    OU = Assign_OU(None).get(campus_OUs)
    print(account_type)
    if str(account_type) == "staff":
        groups = Assign_groups(None,None,None).get()
    print(OU)


if __name__=="__main__":
    main()