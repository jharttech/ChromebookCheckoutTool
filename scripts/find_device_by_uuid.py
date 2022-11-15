import subprocess
import re
from create_account import dict_print


class Wanted_Data:
    def __init__(self,deviceId):
        self.deviceId = deviceId

    @classmethod
    def get(cls):
        while True:
            deviceId = input(f"\nPlease enter the UUID (Directory API ID): ")

            if re.search(r"^(\w{8})\-(\w{4})\-(\w{4})\-(\w{4})\-(\w{12})$", deviceId, flags=re.IGNORECASE | re.ASCII):
                return cls(deviceId)
            else:
                print("Invalid UUID!")


def main():
    info_dict = {
            "1":"serialNumber",
            "2":"orgUnitPath",
            "3":"osVersion",
            "4":"macAddress",
            "5":"autoUpdateExpiration",
            "6":"email",
            "7":"EXIT"
        }
    dict_print(info_dict)
    Wanted_Data.get()


if __name__ == "__main__":
    main()