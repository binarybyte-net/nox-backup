import menu
import backup
import image

def main():
    while True:
        choice = menu.show_menu()
        if choice == "1":
            backup.local_backup()
        elif choice == "2":
            backup.ssh_backup()
        elif choice == "3":
            backup.ssh_restore()  # Add this line
        elif choice == "4":
            image.create_os_image()
        elif choice == "5":
            image.restore_from_image()
        elif choice == "6":
            print("Exiting the utility.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
