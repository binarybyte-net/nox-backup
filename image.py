import subprocess

def create_os_image():
    dev = input("Enter the device to create an image of (e.g., /dev/sda): ")
    img_dest = input("Enter the destination path for the OS image: ")
    print("Creating OS image...")
    subprocess.run(["sudo", "dd", "if="+dev, "of="+img_dest, "bs=4M", "status=progress"])
    print(f"OS image created at {img_dest}.")

def restore_from_image():
    img_file = input("Enter the image file to restore: ")
    target_dev = input("Enter the target device (e.g., /dev/sda): ")
    print("Restoring image to " + target_dev + "...")
    subprocess.run(["sudo", "dd", "if="+img_file, "of="+target_dev, "bs=4M", "status=progress"])
    print("Restoration completed.")
