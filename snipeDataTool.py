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
    leave = 1
    print("Welcome to MG snipeIT data tool\n")
    #Run setup function
    setup()
    #Run script based on what user wants to do
    while True:
        if leave != 1:
            break
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
            leave = 2
        print("\nOperation Complete. You are now ready to transfer data to your SnipeIT server.\nDo you want to perform any other tasks?\n1) Yes\n2) No")
        #Take user input
        leave = int(input())
    print("Have a great day! ~Jhart")
    exit()

def setup():
    #Array of file names
    directories = ["students", "carts"]
    #Set FNULL varialbe to dev null
    FNULL = open(os.devnull, 'w')
    #start while loop for number of directories
    while len(directories):
        #Make each directory
        subprocess.call(['mkdir',directories.pop(0)], stdout=FNULL, stderr=subprocess.STDOUT)


def choseDataType():
    #Set default values for loops to run
    firstResponse = "Invalid option!"
    correct = 2
    while True:
        if firstResponse != "Invalid option!":
            break
        if correct != 2:
            break
        print("\nPlease type the number of the desired data type: \n1) Student Data\n2) Cart Data\n3) Hotspot Data\n4) EXIT")
        #Take user input
        dataType = int(input())
        #Return value from dataSwitch function
        firstResponse = dataSwitch(dataType)
        print(firstResponse)
        print("\nIs this correct:\n1) Yes\n2) No")
        #Take user input
        correct = int(input())
        if correct == 2:
            #Set firstResponse value back to Invalid option so that loop restarts
            firstResponse = "Invalid option!"
    return(dataType)

def studentDataType():
    #Set default values for loops
    tool = "Invalid option!"
    correct = 2
    while True:
        if tool != "Invalid option!":
            break
        if correct != 2:
            break
        print("\nPlease type the number of the desired tool: \n1) Create all student data csv file\n2) Sort student data into individual building")
        #Take user input
        selectedTool = int(input())
        #Assign returned data from studentToolSwitch function to a variable
        tool = studentToolSwitch(selectedTool)
        print(tool)
        print("\nIs this correct:\n1) Yes\n2) No")
        #Take user input
        correct = int(input())
        if correct == 2:
            #Set tool value back to Invalid option so that loop restarts
            tool = "Invalid option!"
    return(selectedTool)

def studentDataTool(argument):
    #Run command or script based on user response passed as argument
    if argument == 1:
        #query GAM for needed information and write it to full_student.csv file in needed_file directory
        os.system("gam print users allfields query orgUnitPath=/Students > needed_file/full_student.csv")
    elif argument == 2:
        #set user_script.sh to executable
        os.chmod('scripts/user_script.sh', 0o755)
        #Run user_script.sh
        subprocess.call("scripts/user_script.sh")
        #Revert permissions on user_script.sh once done
        os.chmod('scripts/user_script.sh', 0o644)
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
    tool = "Invalid option!"
    correct = 2
    #Create loop
    while True:
        if tool != "Invalid option!":
            break
        if correct != 2:
            break
        print("\nPlease type the number of the desired tool: \n1) Compile cart/OU device data csv file\n2) Compile deprovisioned Units csv file")
        #Take user input
        selectedTool = int(input())
        tool = cartToolSwitch(selectedTool)
        print(tool)
        print("\nIs this correct:\n1) Yes\n2) No")
        #Take user input
        correct = int(input())
        if correct == 2:
            #Set tool value back to Invalid option so that loop restarts
            tool = "Invalid option!"
    #Return tool user chose
    return(selectedTool)

def cartDataTool(argument):
    #Run script depending on user choices passed as argument
    if argument == 1:
        #Change cart_script.sh to executable
        os.chmod('scripts/cart_script.sh', 0o755)
        #Run cart_script.sh
        subprocess.call("scripts/cart_script.sh")
        #Revert permission on cart_script.sh
        os.chmod('scirpts/cart_script.sh', 0o644)
    elif argument == 2:
        #Query GAM for deprovisioned devices
        os.system("gam print cros allfields query 'status:deprovisioned' > needed_file/deprovisioned_full.csv")
        #Change deprovisioned_units.sh to executable
        os.chmod('scripts/deprovisioned_units.sh', 0o755)
        #Run deprovisioned_units.sh script
        subprocess.call("scripts/deprovisioned_units.sh")
        #Revert permission on deprovisioned_units.sh script
        os.chmod('scripts/deprovisioned_units.sh', 0o644)
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
    os.chmod('scripts/hotspot_script.sh', 0o755)
    #Run hotspot_script.sh script
    subprocess.call("scripts/hotspot_script.sh")
    #Revert permission of hotspot_script.sh script
    os.chmod('scripts/hotspot_script.sh', 0o644)

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
