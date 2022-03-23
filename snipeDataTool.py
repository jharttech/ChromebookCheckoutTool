#!/usr/bin/env python3
from sys import argv, exit
import csv
import os
import subprocess
import time

sanityCheck = ['y','n']

# input
def main():
    #clear screen
    os.system("clear")
    #set initial value for while loop to run
    quit = False
    print("Welcome to MG snipeIT data tool\n")
    #Run setup function
    setup()
    #Run script based on what user wants to do
    while quit == False:
        #Set variable for debug sake, otherwise run function
        chosenData = choseDataType()
        #print(chosenData) UNCOMMENT FOR DEGUB INFO
        if chosenData == 1:
            #Set variable for debug sake, otherwise run function
            chosenTool = studentDataType()
            #print(chosenTool) UNCOMMENT FOR DEGUB INFO
            studentDataTool(chosenTool)
        elif chosenData == 2:
            #Set variable for debug sake, otherwise run function
            print("Now going to collect all cart data from GAM to ensure newest devices are listed.")
            time.sleep(3)
            with open("needed_file/full.csv", 'w') as file:
                COMMAND = subprocess.Popen(["gam","print","cros","full","query","status:provisioned"], stdout=file)
                COMMAND.wait()
            chosenTool = cartDataType()
            #print(chosenTool) UNCOMMENT FOR DEGUB INFO
            cartDataTool(chosenTool)
        elif chosenData == 3:
            hotspotDataTool()
        elif chosenData == 4:
            staffDataTool()
        elif chosenData == 5:
            findByUUIDTool()
        else:
            print("Unknown error, bailing out!")
            time.sleep(3)
            #End while loop
            quit = True
        leave = None
        while leave not in sanityCheck:
            leave = input("\nOperation Complete. You are now ready to transfer data to your SnipeIT server.\nDo you want to perform any other tasks? (y/n) ").lower()
        #Take user input
            if leave == 'n':
                quit = True
    print("Have a great day! ~Jhart")
    exit()

def setup():
    #Array of file names
    directories = ["students", "carts", "hotspots", "staff"]
    #Set FNULL varialbe to dev null
    FNULL = open(os.devnull, 'w')
    #start while loop for number of directories
    while len(directories):
        #Make each directory
        subprocess.Popen(["mkdir",directories.pop(0)],stdout=FNULL, stderr=subprocess.STDOUT)


def choseDataType():
    #Set default values for loops to run
    valid = False
    while valid == False:
        #Take user input
        dataType = int(input("\nPlease type the number of the desired data type: \n1) Student Data\n2) Cart Data\n3) Hotspot Data\n4) Staff Data\n5) Find Device by UUID\n6) EXIT\n"))
        #Return value from dataSwitch function
        firstResponse = dataSwitch(dataType)
        correct = input(str(firstResponse) + "\nIs this correct: (y/n) ").lower()
        #Take user input
        if correct == 'y':
            valid = True
    return(dataType)

def studentDataType():
    #Set default values for loops
    valid = False
    while valid == False:
        selectedTool = int(input("\nPlease type the number of the desired tool: \n1) Create all student data csv file\n2) Sort student data into individual building\n3) Escalate class to new building\n"))
        #Assign returned data from studentToolSwitch function to a variable
        tool = studentToolSwitch(selectedTool)
        correct = input(str(tool) + "\nIs this correct: (y/n) ").lower()
        #Take user input
        if correct == 'y':
            #Set tool value back to Invalid option so that loop restarts
            valid = True
    return(selectedTool)

def studentDataTool(argument):
    #Run command or script based on user response passed as argument
    if argument == 1:
        #query GAM for needed information and write it to full_student.csv file in needed_file directory
        with open("needed_file/full_student.csv", 'w') as fileNeeded:
            COMMAND = subprocess.Popen(["gam","print","users","allfields","query","orgUnitPath=/Students"], stdout=fileNeeded)
            COMMAND.wait()
        os.system('python3 scripts/user_script.py')
    elif argument == 2:
        #set user_script.sh to executable
        os.system('python3 scripts/user_script.py')
    elif argument == 3:
        subprocess.Popen(["python3","scripts/user_script.py"])
        whichToEscalate = int(input("Do you want to escalate\n1) MS to HS\n2) ES to MS\n"))
        year = input("Please enter the graduation year desired to escalate: ")
        awkCommand = '{print $1}'
        if whichToEscalate == 1:
            buildingOld = 'MGMS'
            buildingNew = 'MGHS'
            file = 'students/MGMS.csv'
            createFile1 = subprocess.Popen(["cat",file], stdout=subprocess.PIPE)
            createFile2 = subprocess.Popen(["grep","-e","^",year], stdin=createFile1.stdout, stdout=subprocess.PIPE)
            with open("students/EscalateMS_To_HS.csv", 'w') as fileNeeded:
                createFile3 = subprocess.Popen(["awk","-F,",awkCommand], stdin=createFile2.stdout, stdout=fileNeeded)
                createFile3.communicate()
                createFile.wait()
        elif whichToEscalate == 2:
            buildingOld = 'MGES'
            buildingNew = 'MGMS'
            file = 'students/MGES.csv'
            createFile1 = subprocess.Popen(["cat",file], stdout=subprocess.PIPE)
            createFile2 = subprocess.Popen(["grep","-e","^",year], stdin=createFile1.stdout, stdout=subprocess.PIPE)
            with open("students/EscalateES_To_MS.csv", 'w') as fileNeeded:
                createFile3 = subprocess.Popen(["awk","-F,",awkCommand], stdin=createFile2.stdout, stdout=fileNeeded)
                createFile3.communicate()
                createFile3.wait()
    else:
        print("Unknown Error! Sealing Blast Doors!")
        time.sleep(3)
        exit()

def studentToolSwitch(argument):
    #Create python switch
    switch = {
    1: "Create all student data csv file",
    2: "Sort student data into individual building",
    3: "Move Students to new building"
    }
    #Set default value so any option other than 1 and 2 returns Invalid options!
    desiredStudentTool = switch.get(argument, "Invalid option!")
    if desiredStudentTool == "Invalid option!":
        return(desiredStudentTool)
    else:
        #Return users choice
        return("\nYou Chose: " + desiredStudentTool)

def cartDataType():
    #Set default values for while loops
    valid = False
    correct = 2
    #Create loop
    while valid == False:
        selectedTool = int(input("\nPlease type the number of the desired tool: \n1) Compile cart/OU device data csv file\n2) Compile deprovisioned Units csv file\n"))
        tool = cartToolSwitch(selectedTool)
        correct = input(str(tool) + "\nIs this correct: (y/n) ").lower()
        #Take user input
        if correct == 'y':
            #Set tool value back to Invalid option so that loop restarts
            valid = True
    #Return tool user chose
    return(selectedTool)

def cartDataTool(argument):
    #Run script depending on user choices passed as argument
    if argument == 1:
        #Change cart_script.sh to executable
        COMMAND = subprocess.Popen(["python3","scripts/cart_script.py"])
        COMMAND.wait()
    elif argument == 2:
        #Query GAM for deprovisioned devices
        with open("needed_file/deprovisioned_full.csv", 'w') as fileNeeded:
            COMMAND = subprocess.Popen(["gam","print","cros","full","query","status:deprovisioned"], stdout=fileNeeded)
            COMMAND.wait()
        LAUNCHSCRIPT = subprocess.Popen(["python3","scripts/deprovisioned_unit.py"])
        LAUNCHSCRIPT.wait()

    else:
        print("Unknown Error! Pulling the plug!")
        time.sleep(3)
        exit()

def cartToolSwitch(argument):
    #Create python switch
    switch = {
    1: "Compile cart/OU device data csv file",
    2: "Compile deprovisioned units csv file"
    }
    desiredCartTool = switch.get(argument, "Invalid option!")
    if desiredCartTool == "Invalid option!":
        return(desiredCartTool)
    else:
        return("\nYou Chose: " + desiredCartTool)

def hotspotDataTool():
    COMMAND = subprocess.Popen(["python3","scripts/hotspot_script.py"])
    COMMAND.wait()

def staffDataTool():
    with open("needed_file/full_staff.csv", 'w') as fileNeeded:
        COMMAND = subprocess.Popen(["gam","print","users","allfields","query","orgUnitPath=/Employees"], stdout=fileNeeded)
        COMMAND.wait()
    LAUNCHSCRIPT = subprocess.Popen(["python3","scripts/user_script.py"])
    LAUNCHSCRIPT.wait()

def findByUUIDTool():
    LAUNCHSCRIPT = subprocess.Popen(["python3", "scripts/findDeviceByUUID.py"])
    LAUNCHSCRIPT.wait()


def dataSwitch(argument):
    #Create python switch
    switch = {
    1: "Student Data",
    2: "Cart Data",
    3: "Hotspot Data",
    4: "Staff Data",
    5: "Find Device By UUID"
    }
    #Set option 6 as exit command
    if argument == 6:
        exit()
    response = switch.get(argument, "Invalid option!")
    if response == "Invalid option!":
        return(response)
    else:
        return("\nYou Chose: " + response)

#Run main function of program
main()
