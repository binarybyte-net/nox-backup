import os
import shutil
import subprocess
import compression  # Importing the compression module

def choose_directory(prompt):
    while True:
        path = input(prompt)
        if os.path.isdir(path) or path.endswith(".tar.gz"):
            return path
        else:
            print("Invalid directory or compressed file. Please try again.")

def list_directories(path):
    try:
        items = [os.path.join(path, item) for item in os.listdir(path)]
        dirs = [item for item in items if os.path.isdir(item)]
        tarballs = [item for item in items if item.endswith(".tar.gz")]
        
        for i, d in enumerate(dirs, start=1):
            print(f"{i}) {os.path.basename(d)} (Directory)")
        
        for i, t in enumerate(tarballs, start=len(dirs) + 1):
            print(f"{i}) {os.path.basename(t)} (Compressed File)")
        
        return dirs, tarballs
    except FileNotFoundError:
        print("Directory not found.")
        return [], []

def select_directories():
    base_path = choose_directory("Enter the base path to list directories: ")
    dirs, tarballs = list_directories(base_path)
    if not dirs and not tarballs:
        print("No valid directories or compressed files found.")
        return []
    selected = input("Enter the numbers of the directories or compressed files to back up (comma-separated): ")
    selected_indices = [int(i.strip()) - 1 for i in selected.split(',') if i.strip().isdigit()]
    selected_items = [os.path.join(base_path, dirs[i]) for i in selected_indices if 0 <= i < len(dirs)] + \
                    [os.path.join(base_path, tarballs[i]) for i in selected_indices if 0 <= i < len(tarballs)]
    return selected_items

def local_backup():
    dirs = select_directories()
    if not dirs:
        print("No directories selected for backup.")
        return
    dest = choose_directory("Enter the destination directory: ")

    # Ask if the user wants to compress the directories
    should_compress = input("Do you want to compress the directories before backup? (yes/no): ")
    compressed_files = []
    if should_compress.lower() == 'yes':
        for dir_path in dirs:
            dir_name = os.path.basename(dir_path)  # Extract the directory name
            output_file = os.path.join(dest, f"{dir_name}.tar.gz")
            if compression.compress_directory(dir_path, output_file):
                compressed_files.append(output_file)
    else:
        compressed_files = dirs

    # Ask if the user wants to decompress the directories
    should_decompress = input("Do you want to decompress the directories before backup? (yes/no): ")
    decompressed_items = []
    if should_decompress.lower() == 'yes':
        for item_path in compressed_files:
            if item_path.endswith(".tar.gz"):
                # Create a target directory preserving only the directory name
                dir_name = os.path.splitext(os.path.basename(item_path))[0]
                target_dir = os.path.join(dest, dir_name)
                os.makedirs(target_dir, exist_ok=True)
                if compression.decompress_directory(item_path, target_dir):
                    decompressed_items.append(target_dir)
    else:
        decompressed_items = compressed_files

    print("Starting local backup...")
    subprocess.run(["rsync", "-avh", "--progress"] + decompressed_items + [dest])
    print("Local backup completed.")


def ssh_backup():
    dirs = select_directories()
    if not dirs:
        print("No directories selected for backup.")
        return
    ssh_dest = input("Enter SSH destination (user@host): ")
    dest = choose_directory("Enter the destination directory on the remote host: ")
    ssh_key = input("Enter the path to your private SSH key (e.g., ~/.ssh/id_rsa): ")

    # Compression for SSH backup
    should_compress = input("Do you want to compress the directories before backup? (yes/no): ")
    compressed_files = []
    if should_compress.lower() == 'yes':
        temp_dir = "/tmp/backup_temp"  # Temporary directory for compression
        os.makedirs(temp_dir, exist_ok=True)
        for dir_path in dirs:
            dir_name = os.path.basename(dir_path)  # Extract the directory name
            output_file = os.path.join(temp_dir, f"{dir_name}.tar.gz")
            if compression.compress_directory(dir_path, output_file):
                compressed_files.append(output_file)
    else:
        compressed_files = dirs

    # Ask if the user wants to decompress the directories
    should_decompress = input("Do you want to decompress the directories before backup? (yes/no): ")
    decompressed_items = []
    if should_decompress.lower() == 'yes':
        for item_path in compressed_files:
            if item_path.endswith(".tar.gz"):
                # Create a target directory on the remote host preserving only the directory name
                dir_name = os.path.splitext(os.path.basename(item_path))[0]
                remote_target_dir = os.path.join(dest, dir_name)
                remote_decompressed_cmd = f"mkdir -p {remote_target_dir} && " \
                                          f"tar -xzvf {item_path} -C {remote_target_dir}"
                ssh_command = f"ssh -i {ssh_key} {ssh_dest} '{remote_decompressed_cmd}'"
                subprocess.run(ssh_command, shell=True)
                decompressed_items.append(remote_target_dir)
    else:
        decompressed_items = compressed_files

    print("Starting backup over SSH...")
    subprocess.run(["rsync", "-avh", "--progress", "-e", f"ssh -i {ssh_key}"] + decompressed_items + [f"{ssh_dest}:{dest}"])
    print("SSH backup completed.")
