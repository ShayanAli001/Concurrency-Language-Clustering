# Concurrency Language Clustering

Clustering programming languages based on their concurrency models using machine learning and AST-based feature engineering.

## Languages Analyzed
- Java, C++, C#, Rust (shared-memory dominant)
- Go, Erlang, Scala (message-passing / actor-based)
- Python, JavaScript (async / event-loop hybrids)

## Features Extracted
- Thread/process spawning density
- Lock/mutex usage
- Channel/actor message passing
- async/await constructs
- Composite concurrency score

## How to Run
```bash
pip3 install -r requirements.txt
jupyter notebook

**.gitignore**
```bash
cat > .gitignore << 'EOL'
# Python & Jupyter
__pycache__/
*.py[cod]
.ipynb_checkpoints/

# Virtual environments
venv/
env/
.venv/

# macOS
.DS_Store

# Large data files
data/*.csv
data/*.parquet
raw_samples/

# IDE
.vscode/
.idea/
