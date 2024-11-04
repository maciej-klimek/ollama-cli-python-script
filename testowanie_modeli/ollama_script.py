import ollama
import argparse
import sys
import threading
import time
import itertools
import subprocess


def run_ollama(model_name, command, execute_flag=False, filename=None):

    if filename:
        full_command = f"File: {filename}\nCommand: {command.strip()}"
    else:
        full_command = f"Command: {command.strip()}"

    response = ollama.chat(model=model_name, messages=[
        {'role': 'user', 'content': full_command}
    ])

    model_output = response['message']['content'].strip()

    if model_output.startswith('`') and model_output.endswith('`'):
        model_output = model_output[1:-1].strip()

    print(model_output)

    dangerous_commands = ['rm', 'rmdir', 'sudo rm']
    contains_dangerous = any(cmd in model_output for cmd in dangerous_commands)

    if execute_flag:
        if contains_dangerous:
            confirmation = input(
                f"The command contains a potentially dangerous operation ('rm'). Are you sure you want to execute it? (y/n): ").strip().lower()
            if confirmation != "y":
                print("Command execution aborted.")
                return

        subprocess.run(model_output, shell=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run commands with Ollama and optionally execute output.")
    parser.add_argument("command", help="Command to pass to the model.")
    parser.add_argument("-e", "--execute", action="store_true",
                        help="Automatically execute the command given by the model.")
    parser.add_argument("-m", "--model", default="LlamaCLI",
                        help="The model to use (default: LlamaCLI).")
    parser.add_argument("-f", "--file", help="Specify the input filename.")

    args = parser.parse_args()

    run_ollama(args.model, args.command, args.execute, filename=args.file)
