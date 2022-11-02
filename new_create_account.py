import sys
import subprocess
from scripts import new_user_script


class Setup():
    def __init__(self,account_type):
        self.account_type = account_type
        n_file = f"{account_type}.txt"
        subprocess.Popen(["touch",])


def main():
    subprocess.Popen(["clear"], stdout=subprocess.PIPE)
    print("Welcome to the MG Create Account Tool\n")
    account_type = new_user_script.Account_type.get()
    Setup(account_type)


if __name__=="__main__":
    main()