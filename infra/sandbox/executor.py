import sys
import json

payload = json.load(sys.stdin)

agent_code = payload["code"]
tests = payload["tests"]
function_name = payload["function_name"]

namespace = {}

exec(agent_code, namespace)

function = namespace[function_name]

results = []
for i, test in enumerate(tests):
    try:
        argument = test["input"]
        if isinstance(argument, (list, tuple)):
            output = function(*argument)
        else:
            output = function(argument)
        
        results.append({
            "index": i,
            "output": repr(output),
            "error": None
        })
    except Exception as e:
        results.append({
            "index":i,
            "output": None,
            "error": str(e)
        })

print("SANDBOX_RESULT_START")
print(json.dumps(results))
print("SANDBOX_RESULT_END")
