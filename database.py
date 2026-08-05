import mysql.connector
from config import HOST, USER, PASSWORD, DATABASE, PORT


# ==========================================
# Connexion à MySQL
# ==========================================

def connecter():

    try:

        connexion = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE,
            port=PORT
        )

        return connexion

    except mysql.connector.Error as erreur:

        print("Erreur :", erreur)

        return None


# ==========================================
# Afficher tous les utilisateurs
# ==========================================

def afficher_utilisateurs():

    connexion = connecter()

    curseur = connexion.cursor(dictionary=True)

    requete = "SELECT * FROM users ORDER BY nom"

    curseur.execute(requete)

    utilisateurs = curseur.fetchall()

    curseur.close()
    connexion.close()

    return utilisateurs


# ==========================================
# Chercher une carte RFID
# ==========================================

def chercher_carte(uid):

    connexion = connecter()

    curseur = connexion.cursor(dictionary=True)

    sql = "SELECT * FROM users WHERE uid=%s"

    curseur.execute(sql, (uid,))

    utilisateur = curseur.fetchone()

    curseur.close()
    connexion.close()

    return utilisateur


# ==========================================
# Ajouter un utilisateur
# ==========================================

def ajouter_utilisateur(uid,
                         nom,
                         service,
                         fonction,
                         email,
                         telephone,
                         actif):

    connexion = connecter()

    curseur = connexion.cursor()

    sql = """
    INSERT INTO users
    (uid, nom, service, fonction, email, telephone, actif)
    VALUES (%s,%s,%s,%s,%s,%s,%s)
    """

    valeurs = (
        uid,
        nom,
        service,
        fonction,
        email,
        telephone,
        actif
    )

    curseur.execute(sql, valeurs)

    connexion.commit()

    curseur.close()

    connexion.close()


# ==========================================
# Modifier un utilisateur
# ==========================================

def modifier_utilisateur(id,
                          uid,
                          nom,
                          service,
                          fonction,
                          email,
                          telephone,
                          actif):

    connexion = connecter()

    curseur = connexion.cursor()

    sql = """
    UPDATE users
    SET
        uid=%s,
        nom=%s,
        service=%s,
        fonction=%s,
        email=%s,
        telephone=%s,
        actif=%s
    WHERE id=%s
    """

    valeurs = (
        uid,
        nom,
        service,
        fonction,
        email,
        telephone,
        actif,
        id
    )

    curseur.execute(sql, valeurs)

    connexion.commit()

    curseur.close()

    connexion.close()


# ==========================================
# Supprimer un utilisateur
# ==========================================

def supprimer_utilisateur(id):

    connexion = connecter()

    curseur = connexion.cursor()

    sql = "DELETE FROM users WHERE id=%s"

    curseur.execute(sql, (id,))

    connexion.commit()

    curseur.close()

    connexion.close()


# ==========================================
# Chercher un utilisateur par ID
# ==========================================

def chercher_utilisateur(id):

    connexion = connecter()

    curseur = connexion.cursor(dictionary=True)

    sql = "SELECT * FROM users WHERE id=%s"

    curseur.execute(sql, (id,))

    utilisateur = curseur.fetchone()

    curseur.close()

    connexion.close()

    return utilisateur


def chercher_admin(username):

    connexion = connecter()

    curseur = connexion.cursor(dictionary=True)

    sql = "SELECT * FROM admins WHERE username=%s"

    curseur.execute(sql, (username,))

    admin = curseur.fetchone()

    curseur.close()

    connexion.close()

    return admin

from datetime import datetime

def enregistrer_acces(uid, nom, resultat):

    connexion = connecter()

    curseur = connexion.cursor()

    maintenant = datetime.now()

    date = maintenant.date()
    heure = maintenant.strftime("%H:%M:%S")

    sql = """
    INSERT INTO logs(uid, nom, date_acces, heure_acces, resultat)
    VALUES (%s,%s,%s,%s,%s)
    """

    curseur.execute(sql, (uid, nom, date, heure, resultat))

    connexion.commit()

    curseur.close()
    connexion.close()