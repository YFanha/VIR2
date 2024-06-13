#!/usr/bin/env python3

import os
import yaml
import subprocess


def clear_screen():
    # Cette fonction nettoie l'écran (fonctionne pour Windows et Unix)
    os.system('cls' if os.name == 'nt' else 'clear')


def display_menu():
    print("\n")
    print("1. Deploy new infras")
    print("2. Stop & delete all running infras")
    print("3. Update kali")
    print("4. Quitter")


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
    with open('deploy_infra/vars.yml', 'r') as file:
        vars_data = yaml.safe_load(file)

    vars_data['student'] = student
    vars_data['kali_student_vmid'] = kali_vmid
    vars_data['pentest_student_vmid'] = pentest_vmid

    # Save modified data back to vars.yml
    with open('deploy_infra/vars.yml', 'w') as file:
        yaml.dump(vars_data, file)


def create_network():
    subprocess.run(
    ["/usr/bin/env", "ansible-playbook", "-i", "inventory/inventory", "deploy_infra/create_network.yml"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL)


def deploy_pentester():
    subprocess.run(
    ["/usr/bin/env", "ansible-playbook", "-i", "inventory/inventory", "deploy_infra/deploy_pentest.yml"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL)


def deploy_attacker():
    subprocess.run(
    ["/usr/bin/env", "ansible-playbook", "-i", "inventory/inventory", "deploy_infra/deploy_attacker.yml"],
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


def stop_all():
    while True:
        clear_screen()
        confirm = input("Are you sure you want to stop and delete all student's infrastructure? (yes/no): ").lower()
        if confirm == 'yes':
            print("Stopping and deleting all student's infrastructure")
            subprocess.run(["/usr/bin/env", "ansible-playbook", "-i", "inventory/inventory", "stop_infra/stop_infras.yml"],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
            print("Infrastructure has been stopped and deleted.")
            break  # Exit the loop if user confirms
        elif confirm == 'no':
            print("Operation cancelled.")
            break  # Exit the loop if user cancels
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def update_kali():
    subprocess.run(
    ["/usr/bin/env", "ansible-playbook", "-i", "inventory/inventory", "deploy_infra/update-template-kali.yml"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL)


    
def update_inventory():
    print("Updating inventory...")
    os.system("/bin/bash updateInventory")


def main():
    while True:
        update_inventory()
        clear_screen()
        display_menu()
        choice = input("What do you want to do ? (1-4) : ")

        if choice == '1':
            deploy_infras()
        elif choice == '2':
            stop_all()
        elif choice == '3':
            update_kali()
        elif choice == '4':
            print("Quit.")
            break
        else:
            print("Invalid choice.")

        input("\nPress any key to continue...")


if __name__ == "__main__":
    main()
