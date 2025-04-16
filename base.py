import os
from concurrent.futures import ThreadPoolExecutor

def rename_folder(old_folder_path, new_folder_path):
    try:
        os.rename(old_folder_path, new_folder_path)
        print(f"Renamed '{os.path.basename(old_folder_path)}' to '{os.path.basename(new_folder_path)}'")
    except OSError as e:
        print(f"Error renaming folder '{old_folder_path}': {e}")

def rename_all_folders(directory, base_name):
    try:
        # Use os.scandir for more efficient directory listing
        folders = [(entry.path, entry.name) for entry in os.scandir(directory) if entry.is_dir()]
        
        tasks = []
        count = 1
        
        # Prepare the tasks with paths to be renamed
        for old_folder_path, folder in folders:
            new_folder_name = f"{base_name}{count}"
            new_folder_path = os.path.join(directory, new_folder_name)
            tasks.append((old_folder_path, new_folder_path))
            count += 1

        # Use ThreadPoolExecutor for I/O-bound operations
        with ThreadPoolExecutor() as executor:
            executor.map(lambda args: rename_folder(*args), tasks)

    except Exception as e:
        print(f"Error accessing directory '{directory}': {e}")

def main():
    directory = '/storage/emulated/0/logs'
    base_name = input("Enter the base name for renaming folders: ")
    rename_all_folders(directory, base_name)

if __name__ == "__main__":
    main()
