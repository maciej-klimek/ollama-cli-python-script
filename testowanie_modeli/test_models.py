import subprocess
import time

openai_script_path = "./openai_script.py"
ollama_script_path = "./ollama_script.py"

command_file = "commands.txt"
openai_result_file = "openai_result.txt"
ollama_result_file = "ollama_result.txt"



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

with open(openai_result_file, "w") as openai_out, open(ollama_result_file, "w") as ollama_out:
    for i, line in enumerate(commands):
        if i % 2 != 0:
            command = line.strip()

            file_flag = None
            if command.endswith("small_test.txt"):
                file_flag = "small_test.txt"
            elif command.endswith("large_test.txt"):
                file_flag = "large_test.txt"

            print(f"Running openai_script.py for command {i // 2 + 1}")
            openai_output, openai_time = run_script(
                openai_script_path, command, file_flag)
            openai_out.write(
                f"Command: {command}\nTime: {openai_time:.2f}s\nOutput:\n{openai_output}\n\n")

            print(f"Running ollama_script.py for command {i // 2 + 1}")
            ollama_output, ollama_time = run_script(
                ollama_script_path, command, file_flag)
            ollama_out.write(
                f"Command: {command}\nTime: {ollama_time:.2f}s\nOutput:\n{ollama_output}\n\n")
