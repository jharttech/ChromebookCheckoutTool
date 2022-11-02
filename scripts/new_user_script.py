import sys
import csv
import re
import subprocess


class Account_type:
    def __init__(self, account):
        self.dict = {"1": "student", "2": "staff", "3": "exit"}

        self.a_type = self.dict.get(account)
        # input(f"account is {self.a_type}")

    def __str__(self):
        return self.a_type

    @classmethod
    def get(cls):
        while True:
            account = input(
                "Would you like to work with: \n1) student \nor \n2) staff\n"
            )
            if not re.search(r"^([1-3])$", account):
                print(f"Please enter 1, 2, or 3")
            else:
                return cls(account)


class Stage_csv:
    def __init__(self, account_type):
        self.g_headers = [
            "primaryEmail",
            "name.givenName",
            "name.familyName",
            "orgUnitPath",
        ]
        self.header_to_num = {}
        self.lines = []
        self.account_type = str(account_type)
        self.result = []
        # input(f"account type is {self.account_type}")

        if self.account_type == "staff":
            print(f"made it to staff account type")
            self.i_filename = "full_staff.csv"
            self.o_filename = "fullStaff.csv"
            self.notes = "EMPLOYEE"
        elif self.account_type == "student":
            print(f"Made it to student account type")
            self.i_filename = "full_student.csv"
            self.o_filename = "fullStudent.csv"
            self.notes = "Initial Import"
        else:
            raise ValueError("Invalid account type!")

        # self.stage()#self.g_headers,self.header_to_num,self.account_type,self.lines,self.i_filename,self.o_filename,self.notes)

    def stage(
        self,
    ):  # ,g_headers,header_to_num,account_type,lines,i_filename,o_filename,notes):
        with open(f"needed_file/{self.i_filename}") as self.csv_file:
            self.csv_reader = csv.reader(self.csv_file, delimiter=",")
            self.n_col = len(next(self.csv_reader))
            self.csv_file.seek(0)
            self.line_count = 0
            self.header_row = [
                "Email",
                "First Name",
                "Last Name",
                "Location",
                "Notes",
                "Username",
            ]

            self.lines.append(self.header_row)

            for row in self.csv_reader:
                if self.line_count == 0:
                    for x in range(0, self.n_col):
                        self.col_name = str(row[x])
                        if self.col_name in self.g_headers:
                            self.header_to_num.update({self.col_name: x})
                    self.line_count += 1
                else:
                    try:
                        self.username = row[
                            self.header_to_num.get(
                                "primaryEmail",
                                "Error getting header number for primaryEmail",
                            )
                        ].split("@")
                        self.username = self.username[0]
                    except:
                        sys.exit(
                            f"Error with primaryEmail field, please check the 'needed_file/{self.i_filename}'"
                        )
                    # DEBUGprint(self.header_to_num)
                    try:
                        self.temp_row = [
                            row[
                                self.header_to_num.get(
                                    "primaryEmail",
                                    "Error getting header number for primaryEmail",
                                )
                            ],
                            row[
                                self.header_to_num.get(
                                    "name.givenName",
                                    "Error getting header number for givenName",
                                )
                            ],
                            row[
                                self.header_to_num.get(
                                    "name.familyName",
                                    "Error getting header number for familyName",
                                )
                            ],
                            row[
                                self.header_to_num.get(
                                    "orgUnitPath",
                                    "Error getting header number for orgUnitPath",
                                )
                            ],
                            self.notes,
                            self.username,
                        ]
                        # DEBUGinput(f"temp row is {self.temp_row}")
                        # DEBUGinput(f"self.lines is {self.lines}")
                        self.lines.append(self.temp_row)
                    except:
                        sys.exit(f"Error getting needed fields for csv row")

            if self.temp_row != []:
                return [self.lines, self.o_filename, self.account_type]
            else:
                sys.exit(f"Error: no {self.account_type} data to add. Exiting now...")


class Compose:
    def __init__(self, staged_data):
        self.o_filename = staged_data[1]
        self.lines = staged_data[0]
        with open(f"needed_file/{self.o_filename}", mode="w") as self.csv_file:
            for i in range(0, len(self.lines)):
                self.full = csv.writer(self.csv_file, delimiter=",")
                self.full.writerow(self.lines[i])


class Building_names:
    def __init__(self, staged_data):
        self.building_list = []
        self.temp_building = []
        self.o_filename = staged_data[1]
        self.num = None

        # self.buildings(self,staged_data[2],staged_data[1])

    def buildings(self):
        with open(f"needed_file/{self.o_filename}", mode="r") as self.csv_file:
            self.csv_reader = csv.reader(self.csv_file, delimiter=",")
            self.line_count = 0
            self.n_col = len(next(self.csv_reader))
            self.csv_file.seek(0)
            for row in self.csv_reader:
                if self.line_count == 0:
                    for x in range(0, self.n_col):
                        if (column_name := str(row[x])) == "Location":
                            self.num = x
                            self.line_count += 1
                else:
                    self.temp_building = row[self.num].split("/")
                    # DEBUGprint(f"temp building list is {self.temp_building}")
                    if (
                        self.temp_building[len(self.temp_building) - 1]
                        not in self.building_list
                    ):
                        self.building_list.append(
                            self.temp_building[len(self.temp_building) - 1]
                        )
        return self.building_list


class Building:
    def __init__(self, building):
        self.building = building

    def __str__(self):
        return self.building

    @classmethod
    def get(cls, building_list):
        buildings = building_list
        buildings.append("ALL")
        while True:
            building = input(
                f"Please enter the building of data wanted:\n {buildings}\n"
            )
            if building not in buildings:
                print("Invalid Building")
            else:
                return cls(building)


class Sort_students:
    def __init__(self, building, i_filename):
        self.building = building
        self.i_filename = i_filename

    def sort(self):
        with open(f"{self.i_filename}", mode="r") as self.csv_file_read:
            self.csv_reader = csv.reader(self.csv_file_read, delimiter=",")
            self.line_count = 0
            self.lines = []
            self.n_cols = len(next(self.csv_reader))
            self.csv_file_read.seek(0)
            for row in self.csv_reader:
                if self.line_count == 0:
                    for x in range(0, self.n_cols):
                        if (column_name := str(row[x])) == "Location":
                            self.num = x
                    self.lines.append(row)
                    self.line_count += 1
                elif (self.line_count != 0) and (row[self.num].__contains__("ALC")):
                    # DEBUGprint(f"full building is {row[self.num]}")
                    self.temp_building = row[self.num].split("/")
                    self.temp_building = self.temp_building[len(self.temp_building) - 1]
                    # DEBUGinput(f"temp buildings are {self.temp_building}")
                    # DEBUGinput(f"Self building is {self.building}")
                    if str(self.temp_building) == str(self.building):
                        self.lines.append(row)
                        # DEBUGprint(row)
                else:
                    continue
        with open(f"student/{self.building}.csv", mode="w") as self.csv_file_write:
            for i in range(0, len(self.lines)):
                self.o_file = csv.writer(self.csv_file_write, delimiter=",")
                self.o_file.writerow(self.lines[i])


def move_file(staged_data):
    filename = f"needed_file/{staged_data[1]}"
    destination = f"{staged_data[2]}/{staged_data[1]}"

    def moved():
        subprocess.Popen(["mv", filename, destination], stdout=subprocess.PIPE)
        return f"All {staged_data[2]} has been compiled into ..ChromebookCheckoutTool/{destination}"

    if staged_data[2] == "staff":
        print(moved())
    elif staged_data[2] == "student":
        building_names = Building_names(staged_data).buildings()
        input(f"building_names are {building_names}")
        building = Building.get(building_names)
        input(building)
        if str(building) != "ALL":
            Sort_students(building, filename).sort()
            print(
                f"All {staged_data[2]} in {building} has been compiled into ..ChromebookCheckoutTool/{staged_data[2]}/{building}.csv"
            )
        else:
            print(moved())
    else:
        sys.exit(
            f"No Data to work with or move, please check original data source needed_file/{staged_data[1]}"
        )


def main():
    account_type = Account_type.get()
    # print(f"account type is {account_type}")
    if account_type == "exit":
        sys.exit("You have chosen to exit.")
    else:
        staged = Stage_csv(account_type).stage()
        # DEBUGprint(f"staged is {staged}")
    Compose(staged)
    move_file(staged)


if __name__ == "__main__":
    main()
