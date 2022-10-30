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
        self.temp_row = []
        self.num = None

        stage(self.g_headers,self.header_to_num,account_type
        ,self.lines)

    def stage(self,g_headers,header_to_num,account_type,lines):
        if account_type == "staff":
            this.i_filename = "full_staff.csv"
            this.o_filename = "fullStaff.csv"
        elif account_type == "student":
            this.i_filename = "full_student.csv"
            this.o_filename = "fullStudent.csv"
        else:
            raise ValueError

        with open(f"needed_file/{this.i_filename}") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            n_col = len(next(csv_reader))
            csv_file.seek(0)
            line_count = 0
            header_row = ['Email','First Name','Last Name','Location','Notes','Username']
            notes = 'EMPLOYEE'

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
                with open(f'needed_file/{this.o_filename}.csv', mode = 'w') as csv_file:
                    for i in range(0,len(lines)):
                        full = csv.writer(csv_file,delimiter=',')
                        full.writerow(lines[i])
            else:
                sys.exit(f"Error: no {account_type} data to add.  Now going to exit...")

                    






             




def main():
    account_type = Account_type()
    if account_type == "exit":
        sys.exit("You have chosen to exit.")
    else:
        staged = Stage_csv(account_type)


if __name__ == "__main__":
    main()