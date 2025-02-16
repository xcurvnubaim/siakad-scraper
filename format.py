import json
import os

# Directory containing JSON files
scrapped_result_dir = "scraped_results"
formatted_dir = os.path.join(scrapped_result_dir)

# Create the formatted directory if it doesn't exist
os.makedirs(formatted_dir, exist_ok=True)

# Iterate over all JSON files in the directory
for filename in os.listdir(scrapped_result_dir):
    file_path = os.path.join(scrapped_result_dir, filename)

    # Skip directories and the formatted output folder
    if not filename.endswith(".json") or os.path.isdir(file_path):
        continue

    # Read JSON file
    with open(file_path, "r") as f:
        json_data = json.load(f)

    # Convert to JSON with one object per line
    formatted_path = os.path.join(formatted_dir, filename)
    with open(formatted_path, "w") as f:
        f.write("[\n")
        f.write(",\n".join(json.dumps(obj, separators=(',', ':')) for obj in json_data))
        f.write("\n]")

    print(f"Formatted JSON saved to {formatted_path}")
