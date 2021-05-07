import os
import subprocess
import time

responseList = ['y','n']

def main():
    os.system("clear")
    leave = False
    print("Welcome to MG Create Account Tool\n")
    while not leave:
        chosenAccountType = choseTool()
        if chosenAccountType == 'Staff':
            organization = staffOU()
            staffTool(organization)
        elif chosenAccountType == 'Student':
             organization = studentOU()


def choseTool():
    toolDict = {
    1: "Staff",
    2: "Student",
    3: "Exit"
    }
    valid = False
    accountType = None
    while not valid:
        while accountType not in [1,2,3]:
            [print(key,':',value) for key, value in toolDict.items()]
            accountType = int(input("\nPlease select the desired account type: "))
        response = toolDict.get(accountType)
        correct = input("You chose " + response + " is this correct? (y/n): ").lower()
        if correct == 'y':
            valid = True
    return(response)

def staffOU():
    orgUnitDict = {
    1: "Employees",
    2: "Admins",
    3: "Discovery",
    4: "LTSubs",
    5: "SecurityStrong",
    6: "Technology",
    7: "BoardMembers",
    8: "Exit"
    }
    orgUnit = None
    correctOU = None
    staffPrint = None
    allStaff = None
    classroom = None
    selectedOrgUnit = None
    while selectedOrgUnit not in list(orgUnitDict.keys()):
        [print(key,':',value) for key, value in orgUnitDict.items()]
        selectedOrgUnit = int(input("Please select the desired Org Unit: "))
        orgUnit = orgUnitDict.get(selectedOrgUnit)
    while correctOU not in responseList:
        correctOU = input("\nYou chose " + orgUnit + ", is this correct? (y/n): ").lower()
    while staffPrint not in responseList:
        staffPrint = input("\nDoes the employee need to cloud print? (y/n): ").lower()
    while allStaff not in responseList:
        allStaff = input("\nDoes the employee need to be on all staff email list? (y/n)").lower()
    while classroom not in responseList:
        classroom = input("\nDoes the employee need to have their own Google Classroom? (y/n)").lower()
    return[orgUnit, staffPrint, allStaff, classroom]

def staffTool(argument):
    desiredOU = argument[0]
    staffPrint = argument[1]
    allStaff = argument[2]
    classroom = argument[3]
    ADDTOPRINT = """awk -F: '{print "gam update group staffprint@mg.k12.mo.us add user "$1}' staff.txt | sh"""
    ADDTOALLSTAFF = """awk -F: '{print "gam update group allstaff@mg.k12.mo.us add user "$1}' staff.txt | sh"""
    ADDTOCLASSROOM = """awk -F: '{print "gam update group classroom@mg.k12.mo.us add user" $1}' staff.txt | sh"""
    staffFile = 'tempStaff.txt'
    os.system("vim " + staffFile)
    if desiredOU == "Employees":
        os.system("mv tempStaff.txt staff.txt")
        COMMAND = """awk -F: '{print "gam create user "$1" firstname "$2" lastname "$3" password "$4" gal on org Employees && sleep 2"}' staff.txt"""
        print("\n")
        subprocess.call(COMMAND, shell=True)
        valid = False
        dryRunGood = None
        while not valid:
            while dryRunGood not in responseList:
                dryRunGood = input("\nDoes the command above look correct? (y/n): ").lower()
            if dryRunGood != 'y':
                break
            else:
                valid = True
                RUN = (COMMAND + " | sh")
                print(RUN)
                subprocess.call(RUN, shell=True)
    elif desiredOU == "Exit":
        exit(1)
    else:
        os.system("rm staff.txt")
        INJECT = "sed -e 's/$/:" + desiredOU +"/' tempStaff.txt >> staff.txt"
        COMMAND = """awk -F: '{print "gam create user "$1" firstname "$2" lastname "$3" password "$4" gal on org Employees/"$5" && sleep 2"}' staff.txt"""
        subprocess.call(INJECT)
        os.system("rm tempStaff.txt")
        print("/n")
        subprocess.call(COMMAND, shell=True)
        valid = False
        dryRunGood = None
        while not valid:
            while dryRunGood not in responseList:
                dryRunGood = input("\nDoes the command above look correct? (y/n): ").lower()
            if dryRunGood != 'y':
                break
            else:
                valid = True
                RUN = (COMMAND + " | sh")
                subprocess.call(RUN, shell=True)
    for x in range(len(argument)):
        if argument[x] == 'y':
            switch = {
            0: ADDTOPRINT,
            1: ADDTOALLSTAFF,
            2: ADDTOCLASSROOM
            }
            whichGroup = switch.get(x, "ERROR!!!")
            subprocess.call(whichGroup, shell=True)

def studentOU():


main()
