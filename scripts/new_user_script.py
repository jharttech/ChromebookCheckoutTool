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

        a_type = self.dict.get(account)
        return a_type


    @classmethod
    def get(cls):
        while True:
            account = input("Would you like to work with: \n1) student \nor \n2) staff\n")
            if not re.search(r"^([1-3])$", account):
                print(f"Please enter 1, 2, or 3")
            else:
                return account


class Stage_csv:
    def __init__(self,account_type):
        self.g_headers = [
            'primaryEmail',
            'name.givenName',
            'name.familyName',
            'orgUnitPath'
        ]
        self.header_to_num = {}
        self.lines = []

        if account_type == "staff":
            self.i_filename = "full_staff.csv"
            self.o_filename = "fullStaff.csv"
            self.notes = "EMPLOYEE"
        elif account_type == "student":
            self.i_filename = "full_student.csv"
            self.o_filename = "fullStudent.csv"
            self.notes = "Initial Import"
        else:
            raise ValueError("Invalid account type!")

        stage(self.g_headers,self.header_to_num,account_type
        ,self.lines,self.i_filename,self.o_filename,self.notes)

    def stage(self,g_headers,header_to_num,account_type,lines,i_filename,o_filename,notes):
        with open(f"needed_file/{i_filename}") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            n_col = len(next(csv_reader))
            csv_file.seek(0)
            line_count = 0
            header_row = ['Email','First Name','Last Name','Location','Notes','Username']

            lines.append(header_row)

            for row in csv_reader:
                while line_count == 0:
                    for x in range(0,n_col):
                        col_name = str(row[x])
                        if col_name in header:
                            header_to_num.update({col_name:x})
                    line_count += 1
                
                try:
                    username = row[header_to_num.get('primaryEmail',"Error getting header number for primaryEmail")].split('@')
                    username = username[0]
                except:
                    sys.exit(f"Error with primaryEmail field, please check the 'needed_file/{this.filename}'")

                try:
                    temp_row = [
                        row[header_to_num.get('primaryEmail',"Error getting header number for primaryEmail")],
                        row[header_to_num.get('name.givenName',"Error getting header number for givenName")],
                        row[header_to_num.get('name.familyName',"Error getting header number for familyName")],
                        row[header_to_num.get('orgUnitPath',"Error getting header number for orgUnitPath")],
                        notes,
                        username
                    ]
                    lines.append(temp_row)
                except:
                    sys.exit(f"Error getting needed fields for csv row")

            if temp_row != []:
                return lines,this.o_filename
            else:
                sys.exit(f"Error: no {account_type} data to add. Exiting now...")


class Compose:
    def __init__(self,staged_data):
        self.o_filename = staged_data[1]
        self.lines = staged_data[0]
        with open(f'needed_file/{self.o_filename}.csv', mode = 'w') as csv_file:
            for i in range(0,len(self.lines)):
                full = csv.writer(csv_file,delimiter=',')
                full.writerow(lines[i])
                    

def main():
    account_type = Account_type()
    if account_type == "exit":
        sys.exit("You have chosen to exit.")
    else:
        staged = Stage_csv(account_type)
    Compose(staged)


if __name__ == "__main__":
    main()