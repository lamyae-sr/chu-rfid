import mysql.connector
from datetime import datetime
from config import HOST, USER, PASSWORD, DATABASE, PORT

# =====================================================
# CONNEXION MYSQL
# =====================================================

def connecter():
    
    try:

        print("Connexion à MySQL...")

        connexion = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE,
            port=PORT,
            connection_timeout=5
        )

        print("Connexion MySQL réussie !")

        return connexion

    except mysql.connector.Error as erreur:

        print("Erreur MySQL :", erreur)

        return None


# =====================================================
# AFFICHER TOUS LES UTILISATEURS
# =====================================================

def afficher_utilisateurs():

    connexion = connecter()

    if connexion is None:
        return []

    curseur = connexion.cursor(dictionary=True)

    curseur.execute("SELECT * FROM users ORDER BY nom")

    resultat = curseur.fetchall()

    curseur.close()
    connexion.close()

    return resultat


# =====================================================
# CHERCHER UTILISATEUR PAR ID
# =====================================================

def chercher_utilisateur(id):

    connexion = connecter()

    if connexion is None:
        return None

    curseur = connexion.cursor(dictionary=True)

    curseur.execute(
        "SELECT * FROM users WHERE id=%s",
        (id,)
    )

    resultat = curseur.fetchone()

    curseur.close()
    connexion.close()

    return resultat


# =====================================================
# CHERCHER PAR UID RFID
# =====================================================

def chercher_carte(uid):

    connexion = connecter()

    if connexion is None:
        return None

    uid = uid.strip().upper()

    curseur = connexion.cursor(dictionary=True)

    sql = """
    SELECT *
    FROM users
    WHERE UPPER(TRIM(uid))=%s
    """

    curseur.execute(sql, (uid,))

    resultat = curseur.fetchone()

    curseur.close()
    connexion.close()

    return resultat


# =====================================================
# CHERCHER ADMIN
# =====================================================

def chercher_admin(username):

    connexion = connecter()

    if connexion is None:
        return None

    curseur = connexion.cursor(dictionary=True)

    curseur.execute(
        "SELECT * FROM admins WHERE username=%s",
        (username,)
    )

    resultat = curseur.fetchone()

    curseur.close()
    connexion.close()

    return resultat


# =====================================================
# AJOUTER UTILISATEUR
# =====================================================

def ajouter_utilisateur(uid,
                         nom,
                         service,
                         fonction,
                         email,
                         telephone,
                         actif):

    connexion = connecter()

    if connexion is None:
        return

    curseur = connexion.cursor()

    sql = """
    INSERT INTO users
    (
        uid,
        nom,
        service,
        fonction,
        email,
        telephone,
        actif
    )
    VALUES
    (
        %s,%s,%s,%s,%s,%s,%s
    )
    """

    valeurs = (
        uid.strip().upper(),
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


# =====================================================
# MODIFIER
# =====================================================

def modifier_utilisateur(id,
                          uid,
                          nom,
                          service,
                          fonction,
                          email,
                          telephone,
                          actif):

    connexion = connecter()

    if connexion is None:
        return

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
        uid.strip().upper(),
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


# =====================================================
# SUPPRIMER
# =====================================================

def supprimer_utilisateur(id):

    connexion = connecter()

    if connexion is None:
        return

    curseur = connexion.cursor()

    curseur.execute(
        "DELETE FROM users WHERE id=%s",
        (id,)
    )

    connexion.commit()

    curseur.close()
    connexion.close()


# =====================================================
# ENREGISTRER ACCES
# =====================================================

def enregistrer_acces(uid,
                       nom,
                       resultat):

    connexion = connecter()

    if connexion is None:
        return

    curseur = connexion.cursor()

    maintenant = datetime.now()

    date = maintenant.date()

    heure = maintenant.strftime("%H:%M:%S")

    sql = """
    INSERT INTO logs
    (
        uid,
        nom,
        date_acces,
        heure_acces,
        resultat
    )
    VALUES
    (
        %s,%s,%s,%s,%s
    )
    """

    valeurs = (
        uid,
        nom,
        date,
        heure,
        resultat
    )

    curseur.execute(sql, valeurs)

    connexion.commit()

    curseur.close()
    connexion.close()

    # =====================================================
# STATISTIQUES DASHBOARD
# =====================================================

def nombre_utilisateurs():

    connexion = connecter()

    if connexion is None:
        return 0

    curseur = connexion.cursor()

    curseur.execute("SELECT COUNT(*) FROM users")

    resultat = curseur.fetchone()[0]

    curseur.close()
    connexion.close()

    return resultat


def nombre_cartes_actives():

    connexion = connecter()

    if connexion is None:
        return 0

    curseur = connexion.cursor()

    curseur.execute("SELECT COUNT(*) FROM users WHERE actif=1")

    resultat = curseur.fetchone()[0]

    curseur.close()
    connexion.close()

    return resultat


def nombre_cartes_inactives():

    connexion = connecter()

    if connexion is None:
        return 0

    curseur = connexion.cursor()

    curseur.execute("SELECT COUNT(*) FROM users WHERE actif=0")

    resultat = curseur.fetchone()[0]

    curseur.close()
    connexion.close()

    return resultat


def nombre_acces():

    connexion = connecter()

    if connexion is None:
        return 0

    curseur = connexion.cursor()

    curseur.execute("SELECT COUNT(*) FROM logs")

    resultat = curseur.fetchone()[0]

    curseur.close()
    connexion.close()

    return resultat


def nombre_autorises():

    connexion = connecter()

    if connexion is None:
        return 0

    curseur = connexion.cursor()

    curseur.execute(
        "SELECT COUNT(*) FROM logs WHERE resultat='AUTORISE'"
    )

    resultat = curseur.fetchone()[0]

    curseur.close()
    connexion.close()

    return resultat

# =====================================================
# AFFICHER HISTORIQUE
# =====================================================

def afficher_historique():

    connexion = connecter()

    if connexion is None:
        return []

    curseur = connexion.cursor(dictionary=True)

    curseur.execute("""
        SELECT *
        FROM logs
        ORDER BY id DESC
    """)

    resultat = curseur.fetchall()

    curseur.close()
    connexion.close()

    return resultat


def nombre_refuses():

    connexion = connecter()

    if connexion is None:
        return 0

    curseur = connexion.cursor()

    curseur.execute(
        "SELECT COUNT(*) FROM logs WHERE resultat='REFUSE'"
    )

    resultat = curseur.fetchone()[0]

    curseur.close()
    connexion.close()

    return resultat