import json
import subprocess
import time
import uuid

TIME_LIMIT = 2

def run_code_in_sandbox(agent_code, tests, function_name):
    """
    Starts up process to run agent code against test cases.

    Args:
        agent_code: String containing the agent's solution to algorithm.
        tests: List of dicts with input and expected keys.
        algo_name: The name of the algorithm the agent solved.

    Returns:
        A dict with the results of the test cases. Or an error message.
    """
    # file_path = write_to_temp_file(agent_code, tests, function_name)
    payload = {
        "code": agent_code,
        "tests": tests,
        "function_name": function_name
    }

    payload_json = json.dumps(payload)

    start = time.perf_counter()

    container_name = f"sandbox-{uuid.uuid4()}"

    try:
        result = subprocess.run(
            [
                "docker",
                "run",
                "--name", container_name,
                "--rm",
                "--network=none",
                "--memory=256m",
                "--cpus=0.5",
                "--pids-limit=64",
                "--tmpfs","/tmp",
                "--read-only",
                "--cap-drop=ALL",
                "--security-opt=no-new-privileges",
                "-i",
                "python-sandbox"
                
            ],
            input=payload_json,
            text=True,
            capture_output=True,
            timeout=TIME_LIMIT
        )
        end = time.perf_counter()
        
        runtime_ms = (end - start) * 1000

        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "runtime_ms": runtime_ms,
            "exit_code": result.returncode,
            "timed_out": 0,
            "crashed": int(result.returncode != 0),
            "execution_success": int(result.returncode == 0 and result.stderr == "")
        }
    except subprocess.TimeoutExpired:
        subprocess.run(["docker", "rm", "-f", container_name])
