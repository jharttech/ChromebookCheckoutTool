import os
import subprocess
import time

def main():
    os.system("clear")
    leave = False
    print("Welcome to MG Create Account Tool\n")
    while not leave:
        chosenAccountType = choseTool()
        if chosenAccountType == 1:
            organization = staffOU()

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
    return(accountType)

def staffOU():
    orgUnitDict = {
    1: "MGHS",
    2: "MGMS",
    3: "MGES",
    4: "JDC",
    5: "OMTC",
    6: "ALC",
    7: "Exit"
    }
    valid = False
    orgUnit = None
    selectedOrgUnit = None
    while not valid:
        while selectedOrgUnit not in list(orgUnitDict.values()):
            [print(key,':',value) for key, value in orgUnitDict.items()]
            selectedOrgUnit = int(input("Please select the desired Org Unit: "))
            orgUnit = orgUnitDict.get(selectedOrgUnit)
            print(orgUnit)


main()
