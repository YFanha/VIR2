#!/usr/bin/env python3

import os
import yaml
import subprocess


def clear_screen():
    # Cette fonction nettoie l'écran (fonctionne pour Windows et Unix)
    os.system('cls' if os.name == 'nt' else 'clear')


def display_menu():
    print("\n=================================")
    print("1. DEPLOY")
    print("2. STOP & DELETE all running infras")
    print("3. STOP running containers")
    print("4. START stopped containers")
    print("5. DELETE all stopped infras")
    print("6. UPDATE kali")
    print("7. Quit")


def kali_generate_vmid(student_nbr):
    if student_nbr < 10:
        return f"30{student_nbr}"
    else:
        return f"3{student_nbr}"

def pentest_generate_vmid(student_nbr):
    if student_nbr < 10:
        return f"20{student_nbr}"
    else:
        return f"2{student_nbr}"


def update_vars(student, kali_vmid, pentest_vmid):
    # Load vars.yml
    with open('playbooks/vars.yml', 'r') as file:
        vars_data = yaml.safe_load(file)

    vars_data['student'] = student
    vars_data['kali_student_vmid'] = kali_vmid
    vars_data['pentest_student_vmid'] = pentest_vmid

    # Save modified data back to vars.yml
    with open('playbooks/vars.yml', 'w') as file:
        yaml.dump(vars_data, file)


def create_network():
    subprocess.run(
    ["/usr/bin/env", "ansible-playbook", "-i", "inventory/inventory", "playbooks/create_network.yml"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL)


def deploy_pentester():
    subprocess.run(
    ["/usr/bin/env", "ansible-playbook", "-i", "inventory/inventory", "playbooks/deploy_pentest.yml"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL)


def deploy_attacker():
    subprocess.run(
    ["/usr/bin/env", "ansible-playbook", "-i", "inventory/inventory", "playbooks/deploy_attacker.yml"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL)


def deploy_infras():
    clear_screen()
    nbrStudent = int(input("Nombre de labos : "))

    for student in range(1, nbrStudent + 1):
        # Generate new VMID by student
        kali_vmid = int(kali_generate_vmid(student))
        pentest_vmid = int(pentest_generate_vmid(student))

        update_vars(student, kali_vmid, pentest_vmid)

        # Create network if not exist
        create_network()

        deploy_attacker()
        deploy_pentester()
        
        print("deployed : " + f"{student}")


def start_infras():
    print("Starting all student's infrastructure")
    subprocess.run(["/usr/bin/env", "ansible-playbook", "-i", "inventory/inventory", "playbooks/start_infras.yml"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL)
    print("Infrastructures has been stopped.")


def stop_running_infras():
    while True:
        clear_screen()
        confirm = input("Are you sure you want to stop all student's infrastructure? (y/n): ").lower()
        if confirm == 'y':
            print("Stopping all student's infrastructure")
            subprocess.run(["/usr/bin/env", "ansible-playbook", "-i", "inventory/inventory", "playbooks/stop_infras.yml"],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
            print("Infrastructures has been stopped.")
            break  # Exit the loop if user confirms
        elif confirm == 'n':
            print("Operation cancelled.")
            break  # Exit the loop if user cancels
        else:
            print("Invalid input. Please enter 'y' or 'n'.")


def delete_all_infras():
    while True:
        clear_screen()
        confirm = input("Are you sure you want to delete all student's infrastructure? (y/n): ").lower()
        if confirm == 'y':
            print("Deleting all stopped student's infrastructure")
            subprocess.run(["/usr/bin/env", "ansible-playbook", "-i", "inventory/inventory", "playbooks/delete_infras.yml"],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
            print("Infrastructures has been deleted.")
            break  # Exit the loop if user confirms
        elif confirm == 'n':
            print("Operation cancelled.")
            break  # Exit the loop if user cancels
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

def stop_and_delete_infras():
    while True:
        clear_screen()
        confirm = input("Are you sure you want to stop & delete all student's infrastructure? (y/n): ").lower()
        if confirm == 'y':
            print("Stopping and deleting all student's infrastructure")
            subprocess.run(["/usr/bin/env", "ansible-playbook", "-i", "inventory/inventory", "playbooks/stop_and_delete_run_infras.yml"],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
            print("Infrastructures has been stopped and deleted.")
            break  # Exit the loop if user confirms
        elif confirm == 'n':
            print("Operation cancelled.")
            break  # Exit the loop if user cancels
        else:
            print("Invalid input. Please enter 'y' or 'n'.")


def update_kali():
    subprocess.run(
    ["/usr/bin/env", "ansible-playbook", "-i", "inventory/inventory", "playbooks/start_template.yml"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL)

    # Update the inventory to get the IP
    update_inventory()

    subprocess.run(
    ["/usr/bin/env", "ansible-playbook", "-i", "inventory/inventory", "playbooks/update-template-kali.yml"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL)
    subprocess.run(
    ["/usr/bin/env", "ansible-playbook", "-i", "inventory/inventory", "playbooks/stop_template.yml"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL)
    
    print("The template has been updated with the packages of the vars.yml file.")


    
def update_inventory():
    print("Updating inventory...")
    os.system("/bin/bash updateInventory")


def main():
    update_inventory()
    while True:
        clear_screen()
        display_menu()
        choice = input("What do you want to do ? (1-6) : ")

        if choice == '1':
            deploy_infras()
        elif choice == '2':
            stop_and_delete_infras()
        elif choice == '3':
            stop_running_infras()
        elif choice == '4':
            start_infras()
        elif choice == '5':
            delete_all_infras()
        elif choice == '6':
            update_kali()
        elif choice == '7':
            print("Quit.")
            break
        else:
            print("Invalid choice.")

        input("Press enter to continue...")


if __name__ == "__main__":
    main()
