import tempfile
import subprocess
import os
import signal
import time

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
        start = time.perf_counter()
        stdout, stderr = process.communicate(timeout=TIME_LIMIT)
        end = time.perf_counter()
        runtime_ms = (end - start) * 1000

        exit_code = process.returncode
        timed_out = 0
        crashed = int(exit_code != 0)
        execution_success = int(exit_code == 0 and stderr == "")

        return {
            "stdout": stdout,
            "stderr": stderr,
            "runtime_ms": runtime_ms,
            "exit_code": exit_code,
            "timed_out": timed_out,
            "crashed": crashed,
            "execution_success": execution_success,
        }
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL)
        return {
            "stdout": "",
            "stderr": "Execution Timeout",
            "runtime_ms": TIME_LIMIT * 1000,
            "exit_code": None,
            "timed_out": 1,
            "crashed": 0,          
            "execution_success": 0,
        }

    finally:
        os.remove(file_path)
