import subprocess

def main():
    getWanted()
    exit()

def getWanted():
    infoDict = {1:"serialNumber", 2:"orgUnitPath", 3:"osVersion", 4:"macAddress", 5:"autoUpdateExpiration", 6:"email"}
    deviceId = input("Please enter the UUID (Directory API ID): ")
    valid = False
    while valid == False:
        check = input("You have entered " + deviceId + ". Is this correct? (y/n) ").lower()
        if check == 'y':
            valid = True
            dataWanted = int(input("What information about " + deviceId + " would you like: \n1)Serial Number\n2)Org Unit\n3)OS Version\n4)MAC Address\n5)Expiration Date\n6)Recent Users\n7)ALL\n"))
            data = infoDict.get(dataWanted, "Error getting desired option!!!")
            if dataWanted != 7:
                if dataWanted == 6:
                    numValid = False
                    while numValid == False:
                        numOfUsers = int(input("Please enter how many recent users you would like to see: (1-51) "))
                        if (numOfUsers > 0 or numOfUsers <= 51):
                            numValid = True
                            result1 = subprocess.Popen(["gam","info","cros",deviceId], stdout=subprocess.PIPE)
                            result2 = subprocess.Popen(["grep",data], stdin=result1.stdout, stdout=subprocess.PIPE)
                            result3 = subprocess.Popen(["head","-n",str(numOfUsers)], stdin=result2.stdout)
                            result3.communicate()
                            return
                else:
                    result1 = subprocess.Popen(["gam","info","cros",deviceId], stdout=subprocess.PIPE)
                    result2 = subprocess.Popen(["grep",data],stdin=result1.stdout)
                    result2.communicate()
                    return
            else:
                result = subprocess.Popen(["gam","info","cros",deviceId])
                result.communicate()
                return


main()
