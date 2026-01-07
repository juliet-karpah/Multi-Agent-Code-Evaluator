MAX_RUNTIME_MS = 1500.0 # For MVP
def normalize(x):
    """
    TODO Will be updated to z-score when there is alot of data
    """
    return max(0.0, min(1.0, x))

def normalize_runtime(runtime_ms):
    return normalize(1 - (runtime_ms / MAX_RUNTIME_MS))

def calculate_score(norm_metrics, weights):
    return sum(norm_metrics[k] * weights[k] for k in weights)