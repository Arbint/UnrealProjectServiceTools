import subprocess

def RunCommand(command):
    print("-----------------------------------")
    print("running command line: ")
    print(command)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(f"Command finished with return code: {result.returncode}\n Output: {result.stdout} \n")
    if result.stderr:
        print(f"Error: {result.stderr}")
    print("-----------------------------------")