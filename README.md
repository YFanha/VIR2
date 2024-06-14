# VIR2

> **Yann Fanha - SI-T1b
Yann.FANHA@eduvaud.ch**
> 

# Concept

---

![VIR2(2).png](https://github.com/YFanha/VIR2/blob/main/Documentation/VIR2.svg)

!https://raw.githubusercontent.com/YFanha/VIR2/main/Documentation/VIR2.svg

# Utilisations

---

## Playbooks

***Tous les playbooks ont été créer pour une utilisation avec le script `main.py.`*** 

| configure-pentest.yml | Configuration du pentester lab sur une machine existance avec le site et ses failles de sécurité. |
| --- | --- |
| create_network.yml | Création du réseau privé entre la machine kali et la machine pentest (si pas existant) |
| delete_infras.yml | Suppression des LXC arrêtés. (Kali et Pentest) |
| deploy_attacker.yml | Clone le template LXC de Kali pour un nouveau labos |
| deploy_attacker.yml | Clone le template Pentester pour un nouveau labos |
| start_infras.yml | Démarrer les labos arrêtés (par le VMID) |
| start_template.yml | Démarrer le template |
| stop_and_delete_run_infras.yml | Arrêter les labos en cours et les supprimer |
| stop_infras.yml | Arrêter les labos en cours |
| stop_template.yml | Arrêter le template Kali |
| update-template-kali.yml | Vérifier et Installer que tous les softwares spécifiés dans la liste “packages_kali” sont présent dans le template. Si un package est ajoué, il sera installé sur la machine grâce  à ce playbook. |


Malheureusement, je n'ai pas réussi à faire fonctionner entièrement le script d'installation du pentester (configure-pentest.yml). Tout fonctionne, excepté la partie d'import de la base de données.
Pour la configuration de kali, le script est "Update-tempalte-kali.yml" -> il installe simplement les packages renseigné dans le fichiers "vars.yml".
## Files

| playbooks/templates/ipconfig.j2 | Template pour le fichier qui répertorie la configuration d’un labo (user, password, IP, hostname..) |
| --- | --- |
| playbooks/vars.yml | Fichiers des variables. Il peut être mis à jour manuellement pour les packages. Il est également utilisé par le script pour créer les VMID. |
| ansible.cfg | Fichier de configuration de ansible |

## Scripts/commandes

| updateInventory | Commande pour mettre à jour l’inventaire basé sur proxmox. |
| --- | --- |

## Exécution du script

```bash
/app/ansible/main.py
```

# Améliorations

---

- **Utilisation** : Scripts pour le déploiement et la configuration des containers templates afin de faciliter le déploiement de l’infrastructure de base.
- **Sécurité et confidentialité** : Améliorer les playbooks afin de ne faire apparaître aucun mot de passe, ni nom utilisateur.

---

## SSH configuration

```bash
ssh-keygen -t ed25519
```

## Inventory

[*Using the `community.general.proxmox` plugin.*](https://docs.ansible.com/ansible/latest/collections/community/general/proxmox_inventory.html)

The proxmox.yml file is available on [the github repository.](https://github.com/YFanha/VIR2/blob/main/inventory/proxmox.yml) It used update the list of the LXC with the playbook update_dns.yml. It is necessary to get the IP of the containers.
