import ollama
import argparse
import sys
import threading
import time
import itertools
import subprocess

def loading_spinner():
    spinner = itertools.cycle(['-', '/', '|', '\\'])
    while not stop_spinner_event.is_set():
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write('\b')

def run_ollama(model_name, command, execute_flag=False, filename=None, file_content=None):
    global stop_spinner_event
    stop_spinner_event = threading.Event()

    spinner_thread = threading.Thread(target=loading_spinner)
    spinner_thread.start()

    if filename and file_content:
        full_command = f"File: {filename}\nContent:\n{file_content}\n\nCommand: {command.strip()}"
    else:
        full_command = f"Command: {command.strip()}"

    response = ollama.chat(model=model_name, messages=[
        {'role': 'user', 'content': full_command}
    ])

    stop_spinner_event.set()
    spinner_thread.join()

    model_output = response['message']['content'].strip()

    if model_output.startswith('`') and model_output.endswith('`'):
        model_output = model_output[1:-1].strip()

    print(model_output)

    if execute_flag:
        subprocess.run(model_output, shell=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run commands with Ollama and optionally execute output.")
    parser.add_argument("command", help="Command to pass to the model.")
    parser.add_argument("-e", "--execute", action="store_true", help="Automatically execute the command given by the model.")
    parser.add_argument("-m", "--model", default="LlamaCLI", help="The model to use (default: LlamaCLI).")
    parser.add_argument("-f", "--file", help="Specify the input filename.")

    args = parser.parse_args()

    file_content = None
    if args.file:
        try:
            with open(args.file, 'r') as f:
                file_content = f.read()
        except FileNotFoundError:
            print(f"Error: The file '{args.file}' does not exist.")
            sys.exit(1)

    run_ollama(args.model, args.command, args.execute, filename=args.file, file_content=file_content)