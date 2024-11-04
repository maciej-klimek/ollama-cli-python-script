import subprocess
import time

# Define script paths
openai_script_path = "./openai_script.py"
ollama_script_path = "./ollama_script.py"

# Define command files and result files
command_file = "commands.txt"
openai_result_file = "openai_result.txt"
ollama_result_file = "ollama_result.txt"

# Helper function to run each script with a command


def run_script(script_path, command, file_flag=None):
    # Set up arguments based on if the -f flag is required
    args = ["python3", script_path, command]
    if file_flag:
        args.extend(["-f", file_flag])

    # Start timing
    start_time = time.time()
    try:
        result = subprocess.run(
            args, capture_output=True, text=True, check=True)
        output = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        output = f"Error: {e.stderr.strip()}"
    end_time = time.time()

    # Calculate time taken and return output
    elapsed_time = end_time - start_time
    return output, elapsed_time


# Read commands from command file
with open(command_file, "r") as f:
    commands = f.readlines()

# Prepare results
with open(openai_result_file, "w") as openai_out, open(ollama_result_file, "w") as ollama_out:
    # Iterate over commands
    for i, line in enumerate(commands):
        # Ignore description lines and get the actual command
        if i % 2 != 0:
            command = line.strip()

            # Determine if the -f flag should be used
            file_flag = None
            if command.endswith("small_test.txt"):
                file_flag = "small_test.txt"
            elif command.endswith("large_test.txt"):
                file_flag = "large_test.txt"

            # Log progress for openai_script.py
            print(f"Running openai_script.py for command {i // 2 + 1}")
            openai_output, openai_time = run_script(
                openai_script_path, command, file_flag)
            openai_out.write(
                f"Command: {command}\nTime: {openai_time:.2f}s\nOutput:\n{openai_output}\n\n")

            # Log progress for ollama_script.py
            print(f"Running ollama_script.py for command {i // 2 + 1}")
            ollama_output, ollama_time = run_script(
                ollama_script_path, command, file_flag)
            ollama_out.write(
                f"Command: {command}\nTime: {ollama_time:.2f}s\nOutput:\n{ollama_output}\n\n")
