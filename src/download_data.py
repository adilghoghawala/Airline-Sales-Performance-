# src/download_data.py
import kagglehub
from pathlib import Path
import shutil

# Download latest version of the dataset from Kaggle
print("Downloading dataset from Kaggle...")
path = kagglehub.dataset_download("bhavikjikadara/us-airline-flight-routes-and-fares-1993-2024")
print("Path to dataset files:", path)

# Make sure data/ exists in your project
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

# The dataset folder may contain one or more CSVs.
# We'll just copy them into data/ so the rest of your code can use them.
src_path = Path(path)
for p in src_path.glob("*.csv"):
    dest = data_dir / p.name
    print(f"Copying {p.name} -> {dest}")
    shutil.copy2(p, dest)

print("Done. Check the data/ folder for the CSVs.")
