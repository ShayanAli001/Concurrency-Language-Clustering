"""
Feature Extraction Pipeline (Phase 2)
Uses Tree-sitter to parse source code and extract concurrency-related AST features.
This is a template showing the real structure — in production, it would process thousands of files.
"""

import os
from tree_sitter import Language, Parser
import pandas as pd

# Note: Tree-sitter languages need to be built/loaded
# In a real setup, you would compile grammars for Java, Go, Python, etc.

# Example concurrency keywords/patterns per language
CONCURRENCY_PATTERNS = {
    'java': ['synchronized', 'Thread', 'Executor', 'Lock', 'await', 'Future'],
    'go': ['go ', 'chan', 'select', 'sync.Mutex', 'WaitGroup'],
    'python': ['async def', 'await', 'threading.', 'asyncio.'],
    'javascript': ['async ', 'await', 'Promise'],
    'rust': ['async ', 'await', 'tokio::', 'Mutex', 'Arc'],
    'erlang': ['spawn', '!', 'receive'],
    'scala': ['Actor', 'Future', 'ExecutionContext'],
    'cpp': ['std::thread', 'std::mutex', 'std::async'],
    'csharp': ['async ', 'await', 'Task', 'lock']
}

def count_concurrency_patterns(code: str, language: str) -> dict:
    """
    Simple keyword-based feature extraction (fallback for demo).
    In full version: Use Tree-sitter queries on AST nodes.
    """
    patterns = CONCURRENCY_PATTERNS.get(language.lower(), [])
    counts = {pat: code.lower().count(pat.lower()) for pat in patterns}
    
    total_lines = len(code.splitlines()) or 1
    densities = {f"{k}_density": v / total_lines for k, v in counts.items()}
    
    # Composite features
    has_threads = int(any(k in code.lower() for k in ['thread', 'spawn', 'go ', 'task']))
    has_locks = int(any(k in code.lower() for k in ['lock', 'mutex', 'synchronized']))
    has_channels = int(any(k in code.lower() for k in ['chan', '!', 'send', 'receive']))
    has_actors = int('actor' in code.lower() or 'spawn' in code.lower())
    has_async = int(any(k in code.lower() for k in ['async', 'await', 'promise', 'future']))
    
    concurrency_score = (
        has_threads * 0.2 +
        has_locks * 0.2 +
        has_channels * 0.25 +
        has_actors * 0.2 +
        has_async * 0.15
    )
    
    return {
        'has_threads': has_threads,
        'lock_density': densities.get('lock_density', 0) + densities.get('mutex_density', 0),
        'channel_density': densities.get('chan_density', 0),
        'actor_density': densities.get('spawn_density', 0) + densities.get('actor_density', 0),
        'async_density': densities.get('async_density', 0) + densities.get('await_density', 0),
        'concurrency_score': round(concurrency_score, 3)
    }

# Example usage (for testing)
if __name__ == "__main__":
    sample_code = """
    public class Example {
        public synchronized void method() {
            new Thread(() -> {
                lock.lock();
            }).start();
        }
    }
    """
    features = count_concurrency_patterns(sample_code, 'java')
    print("Extracted features for Java sample:")
    for k, v in features.items():
        print(f"  {k}: {v}")
