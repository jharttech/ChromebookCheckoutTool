import subprocess
import new_create_account


class Tool:
    def __init__(self, tool):
        self.tool = tool
        
    def __str__(self):
        return f"{self.tool}"
        
    @classmethod
    def get(cls, tool_dict):
        dict_num = input("\nWhat tool would you like to utilize?\n")
        tool = tool_dict.get(dict_num)
        return cls(tool)


def main():
    tool_dict = {
        "1":"create_account",
        "2":"Exit"
    }
    subprocess.Popen(["clear"], stdout=subprocess.PIPE)
    print("Welcome to the MG Create Account Tool\n")
    new_create_account.dict_print(tool_dict)
    tool = Tool.get(tool_dict)
    # Change to case in the future since case switch exists Python >= 3.10
    if str(tool) == "create_account":
        new_create_account.main()


if __name__ == "__main__":
    main()