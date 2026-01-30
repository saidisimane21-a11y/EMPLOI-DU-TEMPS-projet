from datetime import time
from core.salle import Salle
from core.groupe import GroupeEtudiant
from core.matiere import Matiere
from core.enseignant import Enseignant
from core.creneau import Creneau

def generer_salles():
    return [
        Salle(1, "Amphi 6", 200, "amphi", ["projecteur", "systeme_son"]),
        Salle(2, "Amphi 5", 150, "amphi", ["projecteur"]),
        Salle(3, "Labo Machine Learning", 30, "tp", ["pc", "projecteur"]),
        Salle(4, "Labo Analyse des fouielles des données", 25, "tp", ["pc"]),
        Salle(5, "Salle TD F12", 40, "td", ["tableau_blanc"]),
        Salle(6, "Salle TD E15", 35, "td", ["tableau_blanc"]),
        Salle(7, "Salle TD B18", 30, "td", ["projecteur"]),
    ]

def generer_groupes():
    return [
        GroupeEtudiant(1, "G1", "Informatique", 50, "L1"),
        GroupeEtudiant(2, "G2", "Informatique", 45, "L1"),
        GroupeEtudiant(3, "G3", "Biologie", 40, "L2"),
        GroupeEtudiant(4, "L3-AD", "Informatique", 35, "L3"),
        GroupeEtudiant(5, "M1-DS", "Data Science", 25, "M1"),
        GroupeEtudiant(6, "M2-IA", "IA", 20, "M2"),
    ]

def generer_matieres():
    return [
        Matiere("MATH1", "Analyse", "cours", 3, ["projecteur"]),
        Matiere("MATH1-TD", "Analyse (TD)", "td", 2),
        Matiere("PROG1", "Python", "cours", 2, ["projecteur"]),
        Matiere("PROG1-TP", "Python (TP)", "tp", 3, ["pc"]),
        Matiere("BDD", "Bases de Données", "cours", 2, ["projecteur"]),
        Matiere("BDD-TP", "Bases de Données (TP)", "tp", 2, ["pc"]),
        Matiere("IA", "Intelligence Artificielle", "cours", 3, ["projecteur"]),
    ]

def generer_enseignants(matieres):
    # Dictionnaire pour accès facile par code
    m = {matiere.code: matiere for matiere in matieres}
    
    # Créneaux génériques (ex: Lundi-Vendredi, 8h-18h)
    jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]

    return [
        Enseignant(1, "M. Ait KBIR", [m["MATH1"], m["MATH1-TD"]], 
                  [Creneau(j, time(8, 0), time(18, 0)) for j in jours]),
        Enseignant(2, "Mme. Wafae BAIDA", [m["PROG1"], m["PROG1-TP"]], 
                  [Creneau(j, time(8, 0), time(12, 0)) for j in jours]),
        Enseignant(3, "M. JBARI", [m["BDD"], m["BDD-TP"]], 
                  [Creneau(j, time(14, 0), time(18, 0)) for j in jours]),
        Enseignant(4, "M. KOUNAIDI", [m["IA"]], 
                  [Creneau("Lundi", time(8, 0), time(18, 0)), Creneau("Mardi", time(8, 0), time(18, 0))]),
    ]

def obtenir_tout_le_jeu_de_donnees():
    salles = generer_salles()
    groupes = generer_groupes()
    matieres = generer_matieres()
    enseignants = generer_enseignants(matieres)
    
    return {
        "salles": salles,
        "groupes": groupes,
        "matieres": matieres,
        "enseignants": enseignants
    }

if __name__ == "__main__":
    data = obtenir_tout_le_jeu_de_donnees()
    print(f"Généré {len(data['salles'])} salles")
    print(f"Généré {len(data['groupes'])} groupes")
    print(f"Généré {len(data['matieres'])} matières")
    print(f"Généré {len(data['enseignants'])} enseignants")
