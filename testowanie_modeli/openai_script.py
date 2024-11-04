import os
import argparse
import sys
import threading
import time
import itertools
import subprocess
from openai import OpenAI

client = OpenAI(api_key="oho")


def run_openai(command, execute_flag=False, filename=None):
    if filename:
        full_command = f"File: {filename}\nCommand: {command.strip()}"
    else:
        full_command = f"Command: {command.strip()}"

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a Linux terminal assistant. Your responses should be concise one-liners that can be directly pasted into the terminal, without any comments or additional text."},
            {"role": "user", "content": full_command},
        ]
    )

    model_output = completion.choices[0].message.content.strip()

    if model_output.startswith('`') and model_output.endswith('`'):
        model_output = model_output[1:-1].strip()

    print(model_output)

    dangerous_commands = ['rm', 'rmdir', 'sudo rm']
    contains_dangerous = any(cmd in model_output for cmd in dangerous_commands)

    if execute_flag:
        if contains_dangerous:
            confirmation = input(
                "The command contains a potentially dangerous operation ('rm'). Are you sure you want to execute it? (y/n): ").strip().lower()
            if confirmation != "y":
                print("Command execution aborted.")
                return

        subprocess.run(model_output, shell=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run commands with OpenAI and optionally execute output.")
    parser.add_argument("command", help="Command to pass to the model.")
    parser.add_argument("-e", "--execute", action="store_true",
                        help="Automatically execute the command given by the model.")
    parser.add_argument("-f", "--file", help="Specify the input filename.")

    args = parser.parse_args()

    run_openai(args.command, args.execute, filename=args.file)
