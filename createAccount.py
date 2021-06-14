import os
import subprocess
import time

responseList = ['y','n']

def main():
    os.system("clear")
    print("Welcome to MG Create Account Tool\n")
    chosenAccountType = choseTool()
    rerun = True
    try:
        while chosenAccountType != 'Exit':
            setup(chosenAccountType)
            if chosenAccountType == 'Staff':
                organization = staffOU()
                if organization[3] != 'Exit':
                    staffTool(organization)
                else:
                    exit(1)
            elif chosenAccountType == 'Student':
                while rerun == True:
                    organization = studentOU()
                    if organization[0] != 'Exit':
                        rerun = studentTool(organization)
                    else:
                        exit(1)
            elif chosenAccountType == 'Exit':
                exit(1)
    except:
        print("An error has occured or you have chosen to Exit, sealing blast doors now!!")
        exit(1)

def setup(argument):
    if argument == "Student":
        os.system("touch student.txt")
    elif argument == "Staff":
        os.system("touch staff.txt")


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
    while selectedOrgUnit not in list(orgUnitDict.keys()) and correctOU != 'y':
        [print(key,':',value) for key, value in orgUnitDict.items()]
        selectedOrgUnit = int(input("Please select the desired Org Unit: "))
        orgUnit = orgUnitDict.get(selectedOrgUnit)
        if orgUnit == 'Exit':
            exit(1)
        while correctOU not in responseList:
            correctOU = input("\nYou chose " + orgUnit + ", is this correct? (y/n): ").lower()
    while staffPrint not in responseList:
        staffPrint = input("\nDoes the employee need to cloud print? (y/n): ").lower()
    while allStaff not in responseList:
        allStaff = input("\nDoes the employee need to be on all staff email list? (y/n)").lower()
    while classroom not in responseList:
        classroom = input("\nDoes the employee need to have their own Google Classroom? (y/n)").lower()
    return[staffPrint, allStaff, classroom, orgUnit]

def staffTool(argument):
    desiredOU = argument[3]
    staffPrint = argument[0]
    allStaff = argument[1]
    classroom = argument[2]
    ADDTOPRINT = """awk -F: '{print "gam update group staffprint@mg.k12.mo.us add user "$1}' staff.txt | sh"""
    ADDTOALLSTAFF = """awk -F: '{print "gam update group allstaff@mg.k12.mo.us add user "$1}' staff.txt | sh"""
    ADDTOCLASSROOM = """awk -F: '{print "gam update group classroom_teachers@mg.k12.mo.us add user "$1}' staff.txt | sh"""
    staffFile = 'tempStaff.txt'
    os.system("vim " + staffFile)
    if desiredOU == "Exit":
        exit(1)
    elif desiredOU == "Employees":
        os.system("mv tempStaff.txt staff.txt")
        DRYCOMMAND = """awk -F: '{print "gam create user "$1" firstname "$2" lastname "$3" password "$4" gal on org Employees && sleep 2"}' staff.txt"""
        print("\n")
        subprocess.call(DRYCOMMAND, shell=True)
        valid = False
        dryRunGood = None
        while not valid:
            while dryRunGood not in responseList:
                dryRunGood = input("\nDoes the DRYCOMMAND above look correct? (y/n): ").lower()
            if dryRunGood != 'y':
                rerun = True
                return(rerun)
            else:
                valid = True
                RUN = (DRYCOMMAND + " | sh")
                print(RUN)
                subprocess.call(RUN, shell=True)
    else:
        os.system("rm staff.txt")
        INJECT = "sed -e 's/$/:" + desiredOU +"/' tempStaff.txt >> staff.txt"
        DRYCOMMAND = """awk -F: '{print "gam create user "$1" firstname "$2" lastname "$3" password "$4" gal on org Employees/"$5" && sleep 2"}' staff.txt"""
        subprocess.call(INJECT, shell= True)
        os.system("rm tempStaff.txt")
        print("\n")
        subprocess.call(DRYCOMMAND, shell=True)
        valid = False
        dryRunGood = None
        while not valid:
            while dryRunGood not in responseList:
                dryRunGood = input("\nDoes the DRYCOMMAND above look correct? (y/n): ").lower()
            if dryRunGood != 'y':
                rerun = True
                return(rerun)
            else:
                valid = True
                RUN = (DRYCOMMAND + " | sh")
                subprocess.call(RUN, shell=True)
    for x in range(0,len(argument)):
        if argument[x] == 'y':
            switch = {
            0: ADDTOPRINT,
            1: ADDTOALLSTAFF,
            2: ADDTOCLASSROOM
            }
            whichGroup = switch.get(x, "ERROR!!!")
            subprocess.call(whichGroup, shell=True)

def studentOU():
    stuOrgDict = {
    1: "MGHS",
    2: "MGMS",
    3: "MGES",
    4: "JDC",
    5: "OMTC",
    6: "ALC",
    7: "Exit"
    }
    orgUnit = None
    correctOU = None
    selectedOrgUnit = None
    while selectedOrgUnit not in list(stuOrgDict.keys()) and correctOU != 'y':
        [print(key,':',value) for key, value in stuOrgDict.items()]
        selectedOrgUnit = int(input("Please select the desired Org Unit: "))
        orgUnit = stuOrgDict.get(selectedOrgUnit)
        while correctOU not in responseList:
            correctOU = input("\nYou chose " + orgUnit + ", is this correct? (y/n): ").lower()
    return [orgUnit, selectedOrgUnit]

def studentTool(argument):
    desiredOU = argument[0]
    studentFile = 'tempStudent.txt'
    os.system("vim " + studentFile)
    if desiredOU == 'ALC':
        os.system("mv tempStudent.txt student.txt")
        DRYCOMMANDALC = """awk -F: '{print "gam create user "$1" firstname "$2" lastname "$3" password "$4" gal off org Students/MGHS/"$5" && sleep 2"}' student.txt"""
        print("\n")
        subprocess.call(DRYCOMMANDALC, shell=True)
        valid = False
        dryRunGood = None
        while not valid:
            while dryRunGood not in responseList:
                dryRunGood = input("\nDoes the dry run command above look correct? (y/n): ").lower()
            if dryRunGood != 'y':
                return(rerun)
            else:
                valid = True
                RUN = (DRYCOMMANDALC + " | sh")
                print(RUN)
                subprocess.call(RUN, shell=True)
    else:
        os.system('rm student.txt')
        INJECT = "sed -e 's/$/:" + desiredOU + "/' tempStudent.txt >> student.txt"
        DRYCOMMAND = """awk -F: '{print "gam create user "$1" firstname "$2" lastname "$3" password "$4" gal off org Students/"$5" && sleep 2"}' student.txt"""
        subprocess.call(INJECT, shell=True)
        os.system("rm tempStudent.txt")
        print("\n")
        subprocess.call(DRYCOMMAND, shell=True)
        valid = False
        dryRunGood = None
        while not valid:
            while dryRunGood not in responseList:
                dryRunGood = input("\nDoes the dry run command above look correct? (y/n): ").lower()
                if dryRunGood != 'y':
                    rerun = True
                    return(rerun)
                else:
                    try:
                        RUN = (DRYCOMMAND + " | sh")
                        subprocess.call(RUN, shell=True)
                        valid = True
                    except:
                        print("The above error occured! Pulling ejection pin now!")

main()
