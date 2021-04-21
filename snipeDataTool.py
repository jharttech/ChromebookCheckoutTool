#!/usr/bin/env python3
from sys import argv, exit
import csv
import os
import subprocess
import time

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
            chosenTool = cartDataType()
            #print(chosenTool) UNCOMMENT FOR DEGUB INFO
            cartDataTool(chosenTool)
        elif chosenData == 3:
            hotspotDataTool()
        else:
            print("Unknown error, bailing out!")
            time.sleep(3)
            #End while loop
            quit = True
        leave = input("\nOperation Complete. You are now ready to transfer data to your SnipeIT server.\nDo you want to perform any other tasks? (y/n) ").lower()
        #Take user input
        if leave == 'n':
            quit = True
    print("Have a great day! ~Jhart")
    exit()

def setup():
    #Array of file names
    directories = ["students", "carts", "hotspots"]
    #Set FNULL varialbe to dev null
    FNULL = open(os.devnull, 'w')
    #start while loop for number of directories
    while len(directories):
        #Make each directory
        subprocess.call(['mkdir',directories.pop(0)], stdout=FNULL, stderr=subprocess.STDOUT)


def choseDataType():
    #Set default values for loops to run
    valid = False
    while valid == False:
        #Take user input
        dataType = int(input("\nPlease type the number of the desired data type: \n1) Student Data\n2) Cart Data\n3) Hotspot Data\n4) EXIT\n"))
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
        selectedTool = int(input("\nPlease type the number of the desired tool: \n1) Create all student data csv file\n2) Sort student data into individual building\n"))
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
        os.system("gam print users allfields query orgUnitPath=/Students > needed_file/full_student.csv")
    elif argument == 2:
        #set user_script.sh to executable
        os.system('python3 scripts/user_script.py')
    else:
        print("Unknown Error! Sealing Blast Doors!")
        time.sleep(3)
        exit()

def studentToolSwitch(argument):
    #Create python switch
    switch = {
    1: "Create all student data csv file",
    2: "Sort student data into individual building"
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
        os.system("gam print cros full query 'status:provisioned' > needed_file/full.csv")
        os.system('python3 scripts/cart_script.py')
    elif argument == 2:
        #Query GAM for deprovisioned devices
        os.system("gam print cros full query 'status:deprovisioned' > needed_file/deprovisioned_full.csv")
        os.system('python3 scripts/deprovisioned_unit.py')
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
    #Change hotspot_script.sh script to executable
    os.system('python3 scripts/hotspot_script.py')
    #Revert permission of hotspot_script.sh script

def dataSwitch(argument):
    #Create python switch
    switch = {
    1: "Student Data",
    2: "Cart Data",
    3: "Hotspot Data"
    }
    #Set option 4 as exit command
    if argument == 4:
        exit()
    response = switch.get(argument, "Invalid option!")
    if response == "Invalid option!":
        return(response)
    else:
        return("\nYou Chose: " + response)

#Run main function of program
main()
