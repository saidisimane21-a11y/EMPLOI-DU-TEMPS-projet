import sqlite3
from core.salle import Salle
from core.enseignant import Enseignant
from core.seance import Seance
from core.creneau import Creneau
from datetime import datetime

DB_FILE = "database.sqlite"

# --------------------
# Connexion et initialisation
# --------------------
def connexion():
    return sqlite3.connect(DB_FILE)


def initialiser_base():
    with connexion() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Salle (
                id INTEGER PRIMARY KEY,
                nom TEXT NOT NULL,
                capacite INTEGER NOT NULL,
                type_salle TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Salle_Disponibilite (
                salle_id INTEGER,
                jour TEXT,
                heure_debut TEXT,
                heure_fin TEXT,
                FOREIGN KEY(salle_id) REFERENCES Salle(id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Enseignant (
                id INTEGER PRIMARY KEY,
                nom TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Enseignant_Disponibilite (
                enseignant_id INTEGER,
                jour TEXT,
                heure_debut TEXT,
                heure_fin TEXT,
                FOREIGN KEY(enseignant_id) REFERENCES Enseignant(id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Groupe (
                id INTEGER PRIMARY KEY,
                nom TEXT NOT NULL,
                filiere TEXT NOT NULL,
                effectif INTEGER NOT NULL,
                niveau TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Matiere (
                code TEXT PRIMARY KEY,
                nom TEXT NOT NULL,
                type_seance TEXT NOT NULL,
                volume_horaire INTEGER NOT NULL,
                equipements_requis TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Seance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                salle_id INTEGER,
                enseignant_id INTEGER,
                groupe_id INTEGER,
                matiere_code TEXT,
                jour TEXT,
                heure_debut TEXT,
                heure_fin TEXT,
                FOREIGN KEY(salle_id) REFERENCES Salle(id),
                FOREIGN KEY(enseignant_id) REFERENCES Enseignant(id),
                FOREIGN KEY(groupe_id) REFERENCES Groupe(id),
                FOREIGN KEY(matiere_code) REFERENCES Matiere(code)
            )
        """)
        conn.commit()


# --------------------
# Fonctions utilitaires pour heures
# --------------------
def time_to_str(t):
    return t.strftime("%H:%M")

def str_to_time(s):
    return datetime.strptime(s, "%H:%M").time()


# --------------------
# CRUD pour Salle
# --------------------
def sauvegarder_salle(salle: Salle):
    with connexion() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO Salle (id, nom, capacite, type_salle) VALUES (?, ?, ?, ?)",
            (salle.id, salle.nom, salle.capacite, salle.type)
        )
        # Supprimer les anciennes disponibilités
        cursor.execute("DELETE FROM Salle_Disponibilite WHERE salle_id = ?", (salle.id,))
        for dispo in salle.disponibilites:
            cursor.execute(
                "INSERT INTO Salle_Disponibilite (salle_id, jour, heure_debut, heure_fin) VALUES (?, ?, ?, ?)",
                (salle.id, dispo.jour, time_to_str(dispo.heure_debut), time_to_str(dispo.heure_fin))
            )
        conn.commit()


def charger_salles():
    salles = []
    with connexion() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nom, capacite, type_salle FROM Salle")
        for row in cursor.fetchall():
            s = Salle(row[0], row[1], row[2], row[3])
            # Charger les disponibilités
            cursor.execute("SELECT jour, heure_debut, heure_fin FROM Salle_Disponibilite WHERE salle_id = ?", (s.id,))
            for d in cursor.fetchall():
                c = Creneau(d[0], str_to_time(d[1]), str_to_time(d[2]))
                s.ajouter_disponibilite(c)
            salles.append(s)
    return salles


# --------------------
# CRUD pour Enseignant
# --------------------
def sauvegarder_enseignant(e: Enseignant):
    with connexion() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO Enseignant (id, nom) VALUES (?, ?)",
            (e.id, e.nom)
        )
        cursor.execute("DELETE FROM Enseignant_Disponibilite WHERE enseignant_id = ?", (e.id,))
        for dispo in e.disponibilites:
            cursor.execute(
                "INSERT INTO Enseignant_Disponibilite (enseignant_id, jour, heure_debut, heure_fin) VALUES (?, ?, ?, ?)",
                (e.id, dispo.jour, time_to_str(dispo.heure_debut), time_to_str(dispo.heure_fin))
            )
        conn.commit()


def charger_enseignants():
    enseignants = []
    with connexion() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nom FROM Enseignant")
        for row in cursor.fetchall():
            e = Enseignant(row[0], row[1])
            cursor.execute("SELECT jour, heure_debut, heure_fin FROM Enseignant_Disponibilite WHERE enseignant_id = ?", (e.id,))
            for d in cursor.fetchall():
                c = Creneau(d[0], str_to_time(d[1]), str_to_time(d[2]))
                e._disponibilites.append(c)  # accès direct car propriété lecture seule
            enseignants.append(e)
    return enseignants


# --------------------
# CRUD pour Groupe
# --------------------
def sauvegarder_groupe(g: GroupeEtudiant):
    with connexion() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO Groupe (id, nom, filiere, effectif, niveau) VALUES (?, ?, ?, ?, ?)",
            (g.id, g.nom, g.filiere, g.effectif, g.niveau)
        )
        conn.commit()

def charger_groupes():
    groupes = []
    with connexion() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nom, filiere, effectif, niveau FROM Groupe")
        for row in cursor.fetchall():
            groupes.append(GroupeEtudiant(row[0], row[1], row[2], row[3], row[4]))
    return groupes

# --------------------
# CRUD pour Matiere
# --------------------
def sauvegarder_matiere(m: Matiere):
    with connexion() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO Matiere (code, nom, type_seance, volume_horaire, equipements_requis) VALUES (?, ?, ?, ?, ?)",
            (m.code, m.nom, m.type_seance, m.volume_horaire, ",".join(m.equipements_requis))
        )
        conn.commit()

def charger_matieres():
    matieres = []
    with connexion() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT code, nom, type_seance, volume_horaire, equipements_requis FROM Matiere")
        for row in cursor.fetchall():
            equipements = row[4].split(",") if row[4] else []
            matieres.append(Matiere(row[0], row[1], row[2], row[3], equipements))
    return matieres

# --------------------
# CRUD pour Seance
# --------------------
def sauvegarder_seance(seance: Seance):
    from core.matiere import Matiere as M # Eviter import circulaire si possible
    with connexion() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Seance (salle_id, enseignant_id, groupe_id, matiere_code, jour, heure_debut, heure_fin) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                seance.salle.id,
                seance.enseignant.id,
                seance.groupe.id if seance.groupe else None,
                seance.matiere.code if seance.matiere else None,
                seance.creneau.jour,
                time_to_str(seance.creneau.heure_debut),
                time_to_str(seance.creneau.heure_fin)
            )
        )
        conn.commit()


def charger_seances(salles: list, enseignants: list, groupes: list, matieres: list):
    seances = []
    with connexion() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT salle_id, enseignant_id, groupe_id, matiere_code, jour, heure_debut, heure_fin FROM Seance")
        for row in cursor.fetchall():
            salle = next((s for s in salles if s.id == row[0]), None)
            enseignant = next((e for e in enseignants if e.id == row[1]), None)
            groupe = next((g for g in groupes if g.id == row[2]), None)
            matiere = next((m for m in matieres if m.code == row[3]), None)
            
            if salle and enseignant:
                creneau = Creneau(row[4], str_to_time(row[5]), str_to_time(row[6]))
                seances.append(Seance(salle, enseignant, groupe, creneau, matiere))
    return seances
