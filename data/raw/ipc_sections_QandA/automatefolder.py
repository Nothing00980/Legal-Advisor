import os

# Specify the directory where you want to create the files
folder_path = "."  # Replace with your target folder path

# Ensure the directory exists
os.makedirs(folder_path, exist_ok=True)

# Create files from ipc1.jsonl to ipc500.jsonl
for i in range(71, 501):
    file_name = f"ipc{i}.jsonl"
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'w') as file:
        # Optionally, write something in the file
        file.write("")  # Creates an empty file
    print(f"Created: {file_name}")

print("500 files created successfully.")
