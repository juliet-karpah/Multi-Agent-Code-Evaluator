import tempfile
import subprocess
import os
import signal

TIME_LIMIT = 2


def write_to_temp_file(agent_code, tests, function_name):
    """
    Writes code and test cases to a temporary file

    Args:
        agent_code: String containing the agent's solution to algorithm.

    Returns:
        A file_name string
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        file_path = f.name
        f.write(agent_code)
        f.write("\n\nimport json\n\n")
        # add tests
        f.write("test_results = []\n")
        for i, test in enumerate(tests):
            test_input = test["input"]
            f.write(
                f"""
try:
    result_{i} = {function_name}({repr(test_input)})
    test_results.append({{"index": {i}, "output": repr(result_{i}), "error": None}})
except Exception as e:
    test_results.append({{"index": {i}, "output": None, "error": str(e)}})
""")
        f.write("\nprint(json.dumps(test_results))\n")

        return file_path


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
    file_path = write_to_temp_file(agent_code, tests, function_name)
    process = subprocess.Popen(
        ["python3", file_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        preexec_fn=os.setsid,
    )
    try:
        stdout, stderr = process.communicate(timeout=TIME_LIMIT)
        return stdout, stderr
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL)
        return {"error": "Execution Timeout"}
    finally:
        os.remove(file_path)

    
