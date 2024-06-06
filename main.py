import os

def clear_screen():
    # Cette fonction nettoie l'écran (fonctionne pour Windows et Unix)
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    print("\n")
    print("1. Deploy new infras")
    print("2. Stop & delete all running infras")
    print("3. Update kali")
    print("4. Quitter")

#def deploy_pentester():
    # Call command to run the playbook


#def deploy_attacker(studentNbr):
    # Call command to run the playbook


def deploy_infras():
    clear_screen()
    nbrStudent = int(input("Nombre de labos : "))

    for i in range(1, nbrStudent + 1):
        # Generate new vmid based on studentNbr
        # modify vars.yml file with student number and new vmid
        #deploy_attacker(i)
        #deploy_pentester(i)
        print(i)


#def stop_all():


#def update_kali():
    #Start playbook

    
def update_inventory():
    os.system("bash updateInventory")



def main():
    while True:
        clear_screen()
        display_menu()
        choice = input("Veuillez choisir une option (1-4) : ")
        update_inventory()

        if choice == '1':
            deploy_infras()
        elif choice == '2':
            #stop_all()
        elif choice == '3':
            #update_kali()
        elif choice == '4':
            print("Quitter le programme.")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

        input("\nAppuyez sur Entrée pour continuer...")


if __name__ == "__main__":
    main()
