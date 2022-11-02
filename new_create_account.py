import sys
import subprocess
from scripts import new_user_script


class Setup():
    def __init__(self,account_type):
        self.account_type = account_type
        n_file = f"{account_type}/{account_type}.txt"
        subprocess.Popen(["touch",n_file], stdout=subprocess.PIPE)


class Campus_OUs:
    def __init__(self):
        all_ou = subprocess.Popen(["gam","print","orgs"], stdout=subprocess.DEVNULL)
        print(all_ou)


class Staff_OU:
    def __init__(self):
        self.org_unit_dict = {
            
        }


def main():
    subprocess.Popen(["clear"], stdout=subprocess.PIPE)
    print("Welcome to the MG Create Account Tool\n")
    account_type = new_user_script.Account_type.get()
    Setup(account_type)
    Campus_OUs()
    if str(account_type) == "staff":
        Staff_OU


if __name__=="__main__":
    main()