import os
import subprocess
import time
import shutil

responseList = ['y','n']

def main():
    os.system("clear")
    print("Welcome to MG Create Account Tool\n")
    chosenAccountType = choseTool()
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
                organization = studentOU()
                if organization[0] != 'Exit':
                    studentTool(organization)
                else:
                    exit(1)
            elif chosenAccountType == 'Exit':
                exit(1)
    except:
        print("An error has occured or you have chosen to Exit, sealing blast doors now!!")
        exit(1)

def setup(argument):
    if argument == "Student":
        touchStuFile = subprocess.Popen(["touch","student.txt"])
        touchStuFile.communicate()
    elif argument == "Staff":
        touchStaffFile = subprocess.Popen(["touch","staff.txt"])
        touchStaffFile.communicate()


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
    # GETOU = "gam print orgs"
    # listOU = list(subprocess.call(GETOU, shell=True))
    # for x in range(0,len(listOU)):
    #     orgUnitDict.update({x + 1 : listOU[x]})
    # orgUnitDict.update({int(len(listOU)) : "Exit"})
    #Above code needs implimented once on campus
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
    awkFile = "staff.txt"
    staffFile = 'tempStaff.txt'
    editStaffFile = subprocess.Popen(["vim",staffFile])
    editStaffFile.communicate()
    if desiredOU == "Exit":
        exit(1)
    elif desiredOU == "Employees":
        moveTempToStaff = subprocess.Popen(["mv","tempStaff.txt","staff.txt"])
        moveTempToStaff.communicate()
        DRYCOMMAND = '{print "gam create user "$1" firstname "$2" lastname "$3" password "$4" gal on org Employees && sleep 2"}'
        print("\n")
        dryRun = subprocess.Popen(["awk","-F:",DRYCOMMAND,awkFile])
        dryRun.communicate()
        valid = False
        dryRunGood = None
        while not valid:
            while dryRunGood not in responseList:
                dryRunGood = input("\nDoes the DRYCOMMAND above look correct? (y/n): ").lower()
            if dryRunGood != 'y':
                return()
            else:
                valid = True
                awkPrint = '{print "gam create user "$1" firstname "$2" lastname "$3" password "$4" gal on org Employees && sleep 2"}'
                RUN1 = subprocess.Popen(["awk","-F:",awkPrint,awkFile], stdout=subprocess.PIPE)
                RUN2 = subprocess.Popen(["sh"], stdin=RUN1.stdout)
                RUN2.communicate()
    else:
        removeStaffFile = subprocess.Popen(["rm","staff.txt"])
        removeStaffFile.communicate()
        SEDPARAMETERS = "s/$/:" + desiredOU + "/"
        with open("staff.txt", 'w') as file:
            subprocess.Popen(["sed","-e",SEDPARAMETERS,"tempStaff.txt"], stdout=file)
        awkPrint = '{print "gam create user "$1" firstname "$2" lastname "$3" password "$4" gal on org Employees/"$5" && sleep 2"}'
        dryRun = subprocess.Popen(["awk","-F:",awkPrint,awkFile])
        removeTempStaff = subprocess.Popen(["rm","tempStaff.txt"])
        removeTempStaff.communicate()
        print("\n")
        dryRun.communicate()
        valid = False
        dryRunGood = None
        while not valid:
            while dryRunGood not in responseList:
                dryRunGood = input("\nDoes the DRYCOMMAND above look correct? (y/n): ").lower()
            if dryRunGood != 'y':
                return()
            else:
                valid = True
                RUN1 = subprocess.Popen(["awk","-F:",awkPrint,awkFile], stdout=subprocess.PIPE)
                RUN2 = subprocess.Popen(["sh"], stdin=RUN1.stdout)
                RUN2.communicate()
    for x in range(0,len(argument)):
        if argument[x] == 'y':
            switch = {
            0: 'staffprint',
            1: 'allstaff',
            2: 'classroom_teachers'
            }
            whichGroup = switch.get(x, "ERROR!!!")
            ADDGROUPCOMMAND = '{print "gam update group '+whichGroup+'@mg.k12.mo.us add user "$1}'
            ADDGROUP1 = subprocess.Popen(["awk","-F:",ADDGROUPCOMMAND,awkFile], stdout=subprocess.PIPE)
            ADDGROUP2 = subprocess.Popen(["sh"], stdin=ADDGROUP1.stdout)
            ADDGROUP2.communicate()

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
    editStuFile = subprocess.Popen(["vim",studentFile])
    editStuFile.communicate()
    if desiredOU == 'ALC':
        mvTempToStu = subprocess.Popen(["mv",studentFile,"student.txt"])
        mvTempToStu.communicate()
        awkPrintALC = '{print "gam create user "$1" firstname "$2" lastname "$3" password "$4" gal off org Students/MGHS/"$5" && sleep 2"}'
        awkFile = "student.txt"
        print("\n")
        dryRun  = subprocess.Popen(["awk","-F:",awkPrintALC,awkFile])
        dryRun.communicate()
        valid = False
        dryRunGood = None
        while not valid:
            while dryRunGood not in responseList:
                dryRunGood = input("\nDoes the dry run command above look correct? (y/n): ").lower()
            if dryRunGood != 'y':
                rerun = True
                return(rerun)
            else:
                valid = True
                RUN = subprocess.Popen(["awl","-F:",awkPrint,awkFile],stdout=subprocess.PIPE)
                RUN2 = subprocess.Popen(["sh"],stdin=RUN.stdout)
                RUN2.communicate()
    else:
        removeStuFile = subprocess.Popen(["rm","student.txt"])
        removeStuFile.communicate()
        SEDPARAMETERS = "s/$/:" + desiredOU + "/"
        with open("student.txt", 'w') as file:
            INJECT = subprocess.Popen(["sed","-e",SEDPARAMETERS,"tempStudent.txt"], stdout=file)
        awkPrint = '{print "gam create user "$1" firstname "$2" lastname "$3" password "$4" gal off org Students/"$5" && sleep 2"}'
        awkFile = "student.txt"
        dryRun = subprocess.Popen(["awk","-F:",awkPrint,awkFile])
        removeStuTempFile = subprocess.Popen(["rm","tempStudent.txt"])
        removeStuTempFile.communicate()
        print("\n")
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
                        RUN = subprocess.Popen(["awk","-F:", awkPrint,awkFile],stdout=subprocess.PIPE)
                        RUN2 = subprocess.Popen(["sh"],stdin=RUN.stdout)
                        RUN2.communicate()
                        valid = True
                    except:
                        print("The above error occured! Pulling ejection pin now!")

main()
