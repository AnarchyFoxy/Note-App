import os
import sys
from fastapi import FastAPI

app = FastAPI()

# Function to display the ASCII text logo
def display_logo():
    return (
        "    __    _  _    __    ____   ___  _   _  _  _    ____  _____  _  _  _  _ \n"
        "   /__\\  ( \\( )  /__\\  (  _ \\ / __)( )_( )( \\/ )  ( ___)(  _  )( \\/ )( \\/ )\n"
        "  /(__)\\  )  (  /(__)\\  )   /( (__  ) _ (  \\  /    )__)  )(_)(  )  (  \\  / \n"
        " (__)(__)(_)\\_)(__)(__)(_)\\_) \\___)(_) (_) (__)   (__)  (_____)(_/\\_) (__)  \n"
        "   ___  _   _  ____  __    __   \n"
        " / __)( )_( )( ___)(  )  (  )  \n"
        " \\__ \\ ) _ (  )__)  )(__  )(__ \n"
        " (___/(_) (_)(____)(____)(____)"
    )

# Function to parse the input command and arguments
def parse_command(input_str):
    args = input_str.split()
    command = args[0]
    arguments = args[1:]
    return command, arguments

# Function to execute a command with arguments
def execute_command(command, arguments):
    if command == "exit":
        return "Anarchy Foxy Says Goodbye!"
    try:
        pid = os.fork()

        if pid < 0:
            raise Exception("Fork error")
        elif pid == 0:
            # Child process executes the command
            os.execvp(command, [command] + arguments)
            raise Exception("Command execution error")
        else:
            # Parent process waits for the child to complete
            os.waitpid(pid, 0)
    except Exception as e:
        return str(e)

@app.get("/")
def read_root():
    return display_logo()

@app.post("/execute/")
def execute_endpoint(command_str: str):
    command, arguments = parse_command(command_str)
    return execute_command(command, arguments)
