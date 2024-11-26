import os
import pyzipper
from tqdm import tqdm 


def zip_folder_with_password(folder_path, output_name=None, password=None):
    try:
        # Check if the folder exists and is valid
        if not os.path.exists(folder_path):
            print(f"Error: The folder '{folder_path}' does not exist.")
            return

        if not os.path.isdir(folder_path):
            print(f"Error: The path '{folder_path}' is not a valid folder.")
            return

        # Use the folder name for the zip file if no custom name is provided
        folder_name = os.path.basename(os.path.normpath(folder_path))
        zip_file_name = output_name if output_name else f"{folder_name}.zip"
        zip_file_path = os.path.join(os.path.dirname(folder_path), zip_file_name)

        # Initialize the zip file
        print("Initializing ZIP file...")
        if password:
            print("Password protection enabled.")
            zip_file = pyzipper.AESZipFile(
                zip_file_path,
                'w',
                compression=pyzipper.ZIP_DEFLATED,
                encryption=pyzipper.WZ_AES,
            )
            zip_file.setpassword(password.encode('utf-8'))
        else:
            print("Creating an unencrypted ZIP file.")
            zip_file = pyzipper.ZipFile(zip_file_path, 'w', compression=pyzipper.ZIP_DEFLATED)

        # Collect all files and subdirectories
        file_paths = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, folder_path)
                file_paths.append((full_path, rel_path))

        # Add files to zip with a progress bar
        print("Zipping files...")
        for full_path, rel_path in tqdm(file_paths, desc="Compressing", unit="file"):
            zip_file.write(full_path, arcname=rel_path)

        # Close the ZIP file
        zip_file.close()
        print(f"Zipping completed. Archive saved at: {zip_file_path}")

    except PermissionError:
        print("Error: Permission denied. Please check your file or folder permissions.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    folder_path = input("Please enter the path to the folder you want to zip: ").strip()
    custom_name = input("Enter a custom name for the zip file as .zip (leave blank to use the folder name): ").strip()
    password_option = input("Do you want to password-protect the zip file? (yes/no): ").strip().lower() == "yes"

    password = None
    if password_option:
        password = input("Enter a password for the zip file: ").strip()

    zip_folder_with_password(folder_path, output_name=custom_name if custom_name else None, password=password)
