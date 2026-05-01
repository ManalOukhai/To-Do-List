import os
import time
import json
from datetime import datetime

# ── Couleurs ANSI
RESET   = "\033[0m"
BOLD    = "\033[1m"
DIM     = "\033[2m"
GREEN   = "\033[92m"
RED     = "\033[91m"
YELLOW  = "\033[93m"
CYAN    = "\033[96m"
MAGENTA = "\033[95m"
BLUE    = "\033[94m"
WHITE   = "\033[97m"
BG_GREEN  = "\033[42m"
BG_RED    = "\033[41m"
BG_YELLOW = "\033[43m"

# ── Fichier de sauvegarde
FICHIER = "taches.json"

# ── Priorités
PRIORITES = {
    "1": ("🔴 Urgente",  RED),
    "2": ("🟡 Normale",  YELLOW),
    "3": ("🟢 Faible",   GREEN),
}


#   FONCTIONS DE SAUVEGARDE


def charger_taches():
    """Charge les tâches depuis le fichier JSON."""
    if os.path.exists(FICHIER):
        with open(FICHIER, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def sauvegarder_taches(taches):
    """Sauvegarde les tâches dans le fichier JSON."""
    with open(FICHIER, "w", encoding="utf-8") as f:
        json.dump(taches, f, ensure_ascii=False, indent=2)


#   AFFICHAGE

def effacer_ecran():
    os.system("cls" if os.name == "nt" else "clear")

def afficher_banniere():
    print(f"\n{CYAN}╔══════════════════════════════════════════════╗{RESET}")
    print(f"{CYAN}║{RESET}  {BOLD}{MAGENTA}  ✅  TO-DO LIST — Manal Oukhai{RESET}              {CYAN}║{RESET}")
    print(f"{CYAN}║{RESET}  {DIM}Gestionnaire de tâches personnel{RESET}            {CYAN}║{RESET}")
    print(f"{CYAN}╚══════════════════════════════════════════════╝{RESET}")
    now = datetime.now().strftime("%d/%m/%Y  %H:%M")
    print(f"  {DIM}📅 {now}{RESET}\n")

def afficher_taches(taches):
    if not taches:
        print(f"  {DIM}(Aucune tâche pour l'instant — ajoutez-en une !){RESET}\n")
        return

    print(f"  {BOLD}{WHITE}{'N°':<4} {'STATUT':<12} {'PRIORITÉ':<16} {'TÂCHE'}{RESET}")
    print(f"  {DIM}{'─'*56}{RESET}")

    for i, t in enumerate(taches, 1):
        # Statut
        if t["fait"]:
            statut   = f"{GREEN}✅ Faite{RESET}"
            texte    = f"{DIM}{t['texte']}{RESET}"
        else:
            statut   = f"{YELLOW}⏳ En cours{RESET}"
            texte    = t["texte"]

        # Priorité
        prio_label, prio_color = PRIORITES.get(t.get("priorite", "2"), PRIORITES["2"])
        priorite = f"{prio_color}{prio_label}{RESET}"

        print(f"  {BOLD}{CYAN}{i:<4}{RESET} {statut:<22} {priorite:<26} {texte}")

    total  = len(taches)
    faites = sum(1 for t in taches if t["fait"])
    reste  = total - faites
    print(f"\n  {DIM}{'─'*56}{RESET}")
    print(f"  {GREEN}✅ {faites} faite(s){RESET}  •  {YELLOW}⏳ {reste} restante(s){RESET}  •  Total : {total}\n")

def afficher_menu():
    print(f"  {BOLD}Que voulez-vous faire ?{RESET}\n")
    print(f"  {CYAN}[1]{RESET}  Ajouter une tâche")
    print(f"  {GREEN}[2]{RESET}  Marquer une tâche comme faite")
    print(f"  {YELLOW}[3]{RESET}  Modifier une tâche")
    print(f"  {RED}[4]{RESET}  Supprimer une tâche")
    print(f"  {MAGENTA}[5]{RESET}  Supprimer toutes les tâches faites")
    print(f"  {BLUE}[6]{RESET}  Trier par priorité")
    print(f"  {DIM}[0]{RESET}  Quitter\n")

#   ACTIONS

def ajouter_tache(taches):
    print(f"\n{CYAN}── Nouvelle tâche ──────────────────────────{RESET}")
    texte = input(f"  {BOLD}Description :{RESET} ").strip()
    if not texte:
        print(f"  {RED}⚠ Description vide, annulé.{RESET}")
        return

    print(f"\n  Choisissez une priorité :")
    for k, (label, color) in PRIORITES.items():
        print(f"  {color}[{k}]{RESET}  {label}")

    prio = input(f"\n  Priorité (1/2/3) [{YELLOW}2{RESET} par défaut] : ").strip()
    if prio not in PRIORITES:
        prio = "2"

    tache = {
        "texte":    texte,
        "fait":     False,
        "priorite": prio,
        "date":     datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    taches.append(tache)
    sauvegarder_taches(taches)
    print(f"\n  {GREEN}✅ Tâche ajoutée avec succès !{RESET}")

def marquer_faite(taches):
    if not taches:
        print(f"  {RED}⚠ Aucune tâche à marquer.{RESET}")
        return
    try:
        n = int(input(f"  Numéro de la tâche à cocher : "))
        if 1 <= n <= len(taches):
            t = taches[n - 1]
            if t["fait"]:
                t["fait"] = False
                print(f"  {YELLOW}↩ Tâche remise en 'En cours'.{RESET}")
            else:
                t["fait"] = True
                print(f"  {GREEN}🎉 Bravo ! Tâche marquée comme faite !{RESET}")
            sauvegarder_taches(taches)
        else:
            print(f"  {RED}⚠ Numéro invalide.{RESET}")
    except ValueError:
        print(f"  {RED}⚠ Entrez un nombre valide.{RESET}")

def modifier_tache(taches):
    if not taches:
        print(f"  {RED}⚠ Aucune tâche à modifier.{RESET}")
        return
    try:
        n = int(input(f"  Numéro de la tâche à modifier : "))
        if 1 <= n <= len(taches):
            t = taches[n - 1]
            print(f"  Texte actuel : {CYAN}{t['texte']}{RESET}")
            nouveau = input(f"  Nouveau texte (Entrée pour garder) : ").strip()
            if nouveau:
                t["texte"] = nouveau
            print(f"  Nouvelle priorité (1/2/3, Entrée pour garder) : ", end="")
            prio = input().strip()
            if prio in PRIORITES:
                t["priorite"] = prio
            sauvegarder_taches(taches)
            print(f"  {GREEN}✅ Tâche modifiée.{RESET}")
        else:
            print(f"  {RED}⚠ Numéro invalide.{RESET}")
    except ValueError:
        print(f"  {RED}⚠ Entrez un nombre valide.{RESET}")

def supprimer_tache(taches):
    if not taches:
        print(f"  {RED}⚠ Aucune tâche à supprimer.{RESET}")
        return
    try:
        n = int(input(f"  Numéro de la tâche à supprimer : "))
        if 1 <= n <= len(taches):
            supprimee = taches.pop(n - 1)
            sauvegarder_taches(taches)
            print(f"  {RED}🗑 Tâche '{supprimee['texte']}' supprimée.{RESET}")
        else:
            print(f"  {RED}⚠ Numéro invalide.{RESET}")
    except ValueError:
        print(f"  {RED}⚠ Entrez un nombre valide.{RESET}")

def supprimer_faites(taches):
    avant = len(taches)
    taches[:] = [t for t in taches if not t["fait"]]
    apres = len(taches)
    sauvegarder_taches(taches)
    print(f"  {GREEN}✅ {avant - apres} tâche(s) supprimée(s).{RESET}")

def trier_priorite(taches):
    taches.sort(key=lambda t: t.get("priorite", "2"))
    sauvegarder_taches(taches)
    print(f"  {BLUE}🔃 Tâches triées par priorité.{RESET}")

#   PROGRAMME PRINCIPAL

def main():
    taches = charger_taches()

    while True:
        effacer_ecran()
        afficher_banniere()
        afficher_taches(taches)
        afficher_menu()

        choix = input(f"  {BOLD}Votre choix :{RESET} ").strip()

        print()

        if choix == "1":
            ajouter_tache(taches)
        elif choix == "2":
            marquer_faite(taches)
        elif choix == "3":
            modifier_tache(taches)
        elif choix == "4":
            supprimer_tache(taches)
        elif choix == "5":
            supprimer_faites(taches)
        elif choix == "6":
            trier_priorite(taches)
        elif choix == "0":
            print(f"  {MAGENTA}👋 À bientôt, Manal !{RESET}\n")
            break
        else:
            print(f"  {RED}⚠ Option invalide, choisissez entre 0 et 6.{RESET}")

        time.sleep(1.2)

if __name__ == "__main__":
    main()
