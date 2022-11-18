import subprocess
import csv


class Stage_CSV:
    def __init__():
        self.g_headers = [
            "deviceId",
            "diskVolumeReports.0.volumeInfo.0.storageFree",
            "diskVolumeReports.0.volumeInfo.0.storageTotal",
            "orgUnitPath",
            "serialNumber"
        ]

        self.header_to_num = {}
        self.lines = []
        self.i_filename = "full_devices.csv"

    def stage(self):
        with open(f"needed_file/{self.i_filename}", mode="r") as self.csv_file_read:
            self.csv_reader = csv.reader(self.csv_file_read, delimiter=",")
            self.n_col = len(next(self.csv_reader))
            self.csv_file_read.seek(0)
            self.line_count = 0
            

def main():
    ... 


if __name__ == "__main__":
    main()