import sys
import csv
import re
import subprocess


class Account_type:
    def __init__(self,account):
        self.dict = {
            "1": "student",
            "2": "staff",
            "3": "exit"
        }

        a_type = dict.get(account)
        return a_type


    @classmethod
    def get(cls):
        while True:
            account = input("Would you like to work with: \n1) student \nor \n2) staff\n")
            if not re.search(r"^([1-3])$", account):
                print(f"Please enter 1, 2, or 3")
            else:
                return account


class Compose_csv:
    def __init__(self,account_type):
        self.header = [
            'primaryEmail',
            'name.givenName',
            'name.familyName',
            'orgUnitPath'
        ]
        self.header_to_num = {}
        lines = []
        temp_row = []
        num = None

        compose(account_type)

    def compose(self.account_type):
        if account_type == "staff":
            this.filename = "full_staff.csv"
        elif account_type == "student":
            this.filename = "full_student.csv"
        else:
            raise ValueError

        with open(f"needed_file/{this.filename}") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            n_col = len(next(csv_reader))
            csv_file.seek(0)
            line_count = 0 
             




def main():
    account_type = Account_type()
    if account_type == "exit":
        sys.exit("You have chosen to exit.")
    else:
        Compose_csv(account_type)


if __name__ == "__main__":
    main()