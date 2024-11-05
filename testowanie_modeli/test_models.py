import subprocess
import time
import csv

openai_script_path = "./openai_script.py"
ollama_script_path = "./ollama_script.py"

command_file = "commands.txt"
openai_result_file = "openai_result.csv"
ollama_result_file = "ollama_result.csv"


def run_script(script_path, command, file_flag=None):
    args = ["python3", script_path, command]
    if file_flag:
        args.extend(["-f", file_flag])
    start_time = time.time()
    try:
        result = subprocess.run(
            args, capture_output=True, text=True, check=True)
        output = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        output = f"Error: {e.stderr.strip()}"
    end_time = time.time()

    elapsed_time = end_time - start_time
    return output, elapsed_time


with open(command_file, "r") as f:
    commands = f.readlines()

# Write headers and results to CSV files for openai and ollama
with open(openai_result_file, "w", newline="") as openai_out, open(ollama_result_file, "w", newline="") as ollama_out:
    openai_writer = csv.writer(openai_out)
    ollama_writer = csv.writer(ollama_out)

    # Write headers
    openai_writer.writerow(["Command", "Time (s)", "Output"])
    ollama_writer.writerow(["Command", "Time (s)", "Output"])

    # Loop to get every third line for each command
    for i, line in enumerate(commands[::3]):
        command = line.strip()

        file_flag = None
        if command.endswith("small_test.txt"):
            file_flag = "small_test.txt"
        elif command.endswith("large_test.txt"):
            file_flag = "large_test.txt"

        # Run and log openai_script.py
        # print(f"Running openai_script.py for command {i + 1}")
        # openai_output, openai_time = run_script(
        #     openai_script_path, command, file_flag)
        # openai_writer.writerow([command, f"{openai_time:.2f}", openai_output])

        # Run and log ollama_script.py
        print(f"Running ollama_script.py for command {i + 1}")
        ollama_output, ollama_time = run_script(
            ollama_script_path, command, file_flag)
        ollama_writer.writerow([command, f"{ollama_time:.2f}", ollama_output])
