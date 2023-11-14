import subprocess

def local_backup():
    dirs = input("Enter the directory or directories to back up (space-separated): ")
    dest = input("Enter the destination directory: ")
    print("Starting local backup...")
    subprocess.run(["rsync", "-avh", "--progress"] + dirs.split() + [dest])
    print("Local backup completed.")

def ssh_backup():
    dirs = input("Enter the directory or directories to back up (space-separated): ")
    ssh_dest = input("Enter SSH destination (user@host): ")
    dest = input("Enter the destination directory on the remote host: ")
    ssh_key = input("Enter the path to your private SSH key (e.g., ~/.ssh/id_rsa): ")
    print("Starting backup over SSH...")
    subprocess.run(["rsync", "-avh", "--progress", "-e", f"ssh -i {ssh_key}"] + dirs.split() + [f"{ssh_dest}:{dest}"])
    print("SSH backup completed.")
