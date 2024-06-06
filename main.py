#!/usr/bin/env python3

import os
import yaml


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
    os.system("/usr/bin/env ansible-playbook -i inventory/inventory deploy_infra/create_network.yml >/dev/null")


def deploy_pentester():
    os.system("/usr/bin/env ansible-playbook -i inventory/inventory deploy_infra/deploy_pentest.yml >/dev/null")


def deploy_attacker():
    os.system("/usr/bin/env ansible-playbook -i inventory/inventory deploy_infra/deploy_attacker.yml >/dev/null")


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


#def stop_all():


def update_kali():
    os.system("/usr/bin/env ansible-playbook -i inventory/inventory deploy_infra/update-template-kali.yml >/dev/null")

    
def update_inventory():
    os.system("./updateInventory")


def main():
    while True:
        clear_screen()
        display_menu()
        choice = input("Veuillez choisir une option (1-4) : ")
        update_inventory()

        if choice == '1':
            deploy_infras()
        elif choice == '2':
            print("Stop & delete all running infras")
        elif choice == '3':
            update_kali()
        elif choice == '4':
            print("Quitter le programme.")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

        input("\nAppuyez sur Entrée pour continuer...")


if __name__ == "__main__":
    main()
