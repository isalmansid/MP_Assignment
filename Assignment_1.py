import os

def rename_files_in_folder(folder_path, reverse=False, preview=False, recursive=False):
    try:
        # Check if the folder exists
        if not os.path.exists(folder_path):
            print(f"Error: The folder '{folder_path}' does not exist.")
            return

        # Collect all files (and optionally subdirectories if recursive)
        files = []
        if recursive:
            for root, _, filenames in os.walk(folder_path):
                for filename in filenames:
                    files.append(os.path.join(root, filename))
        else:
            all_items = os.listdir(folder_path)
            files = [
                os.path.join(folder_path, f)
                for f in all_items
                if os.path.isfile(os.path.join(folder_path, f))
            ]

        # Check if the folder (or recursive subdirectories) is empty
        if not files:
            print("The folder is empty. No files to rename.")
            return

        # Sort files alphabetically (or reverse order if specified)
        files.sort(reverse=reverse)

        # Preview file names if requested
        if preview:
            print("Preview of file renaming:")
            for idx, file_path in enumerate(files, start=1):
                file_name = os.path.basename(file_path)
                file_extension = os.path.splitext(file_name)[1]
                new_name = f"{idx}{file_extension}"
                print(f"{file_name} -> {new_name}")
            confirm = input("Proceed with renaming? (yes/no): ").strip().lower()
            if confirm != "yes":
                print("Renaming cancelled.")
                return

        # Perform renaming
        print("Renaming files...")
        for idx, file_path in enumerate(files, start=1):
            directory = os.path.dirname(file_path)
            file_name = os.path.basename(file_path)
            file_extension = os.path.splitext(file_name)[1]
            new_name = f"{idx}{file_extension}"
            new_path = os.path.join(directory, new_name)

            try:
                os.rename(file_path, new_path)
                print(f"File '{file_name}' renamed to '{new_name}'")
            except PermissionError:
                print(f"Error: Unable to rename file '{file_name}' due to permission issues.")

        print("Renaming completed.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    folder_path = input("Please enter the path to the folder: ").strip()
    reverse_option = input("Rename in reverse order? (yes/no): ").strip().lower() == "yes"
    preview_option = input("Preview file renaming before proceeding? (yes/no): ").strip().lower() == "yes"
    recursive_option = input("Rename files in subdirectories as well? (yes/no): ").strip().lower() == "yes"

    rename_files_in_folder(
        folder_path, reverse=reverse_option, preview=preview_option, recursive=recursive_option
    )
