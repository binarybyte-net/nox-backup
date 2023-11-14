import os
import subprocess

def choose_directory(prompt):
    while True:
        path = input(prompt)
        if os.path.isdir(path):
            return path
        else:
            print("Invalid directory. Please try again.")

def list_directories(path):
    try:
        dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
        for i, d in enumerate(dirs, start=1):
            print(f"{i}) {d}")
        return dirs
    except FileNotFoundError:
        print("Directory not found.")
        return []

def select_directories():
    base_path = choose_directory("Enter the base path to list directories: ")
    dirs = list_directories(base_path)
    if not dirs:
        return []
    selected = input("Enter the numbers of the directories to back up (comma-separated): ")
    selected_indices = [int(i.strip()) - 1 for i in selected.split(',') if i.strip().isdigit()]
    return [os.path.join(base_path, dirs[i]) for i in selected_indices if 0 <= i < len(dirs)]

def local_backup():
    dirs = select_directories()
    if not dirs:
        print("No directories selected for backup.")
        return
    dest = choose_directory("Enter the destination directory: ")
    print("Starting local backup...")
    subprocess.run(["rsync", "-avh", "--progress"] + dirs + [dest])
    print("Local backup completed.")

def ssh_backup():
    dirs = select_directories()
    if not dirs:
        print("No directories selected for backup.")
        return
    ssh_dest = input("Enter SSH destination (user@host): ")
    dest = choose_directory("Enter the destination directory on the remote host: ")
    ssh_key = input("Enter the path to your private SSH key (e.g., ~/.ssh/id_rsa): ")
    print("Starting backup over SSH...")
    subprocess.run(["rsync", "-avh", "--progress", "-e", f"ssh -i {ssh_key}"] + dirs + [f"{ssh_dest}:{dest}"])
    print("SSH backup completed.")
