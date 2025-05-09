import shutil
from pathlib import Path

# Read the source file path from .html-source
with open('.html-source', 'r') as f:
    source_path = f.read().strip()

source = Path(source_path)

if not source.is_file():
    raise FileNotFoundError(f"Source file not found: {source}")

destination = Path.cwd() / source.name

shutil.copy2(source, destination)

print(f"Copied {source} to {destination}")