import shutil
from pathlib import Path

# Read the source file path from .html-source
with open('.html-source', 'r') as f:
    source_path = f.read().strip()

source = Path(source_path)

if not source.is_file():
    raise FileNotFoundError(f"Source file not found: {source}")

destination = Path.cwd() / "grass_latte" / "webpage" / (source.name.split(".")[0] + ".py")


with open(source, "r") as f:
    contents = f.read()

contents = contents.replace("\\", "\\\\")
contents = contents.replace('"""', r'\"\"\"')

with open(destination, "w+") as f:
    f.write(f'HTML_SOURCE = """{contents}"""')

print(f"Wrote {source} to {destination}")