import os

def rename_files(folder_path):
    # Get a list of all files in the specified folder
    files = os.listdir(folder_path)
    
    # Sort files to ensure consistent ordering
    files.sort()
    
    for index, filename in enumerate(files):
        # Create new filename
        new_filename = f"{index}.png"
        
        # Build full file paths
        old_file = os.path.join(folder_path, filename)
        new_file = os.path.join(folder_path, new_filename)
        
        # Rename the file
        os.rename(old_file, new_file)

# Specify the folder path
folder_path = './data/train/0/0'
rename_files(folder_path)
