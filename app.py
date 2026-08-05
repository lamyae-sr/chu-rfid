from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import check_password_hash

from database import (
    afficher_utilisateurs,
    ajouter_utilisateur,
    modifier_utilisateur,
    supprimer_utilisateur,
    chercher_utilisateur,
    chercher_admin,
    chercher_carte,
    enregistrer_acces
)

app = Flask(__name__)
app.secret_key = "chu_rfid_2026"

# =====================================================
# LOGIN
# =====================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        admin = chercher_admin(username)

        if admin:

            if check_password_hash(admin["password"], password):
                session["admin"] = admin["username"]
                return redirect(url_for("index"))

        return render_template(
            "login.html",
            erreur="Nom d'utilisateur ou mot de passe incorrect."
        )

    return render_template("login.html")


# =====================================================
# LOGOUT
# =====================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# =====================================================
# ACCUEIL
# =====================================================

@app.route("/")
def index():

    if "admin" not in session:
        return redirect(url_for("login"))

    return render_template("index.html")


# =====================================================
# DASHBOARD
# =====================================================
@app.route("/ping", methods=["GET", "POST"])
def ping():
    return jsonify({
        "message": "pong"
    })

@app.route("/dashboard")
def dashboard():

    if "admin" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html")


# =====================================================
# HISTORIQUE
# =====================================================

@app.route("/historique")
def historique():

    if "admin" not in session:
        return redirect(url_for("login"))

    return render_template("historique.html")


# =====================================================
# EXPORT
# =====================================================

@app.route("/export")
def export():

    if "admin" not in session:
        return redirect(url_for("login"))

    return "<h2>Export Excel à développer</h2>"


# =====================================================
# UTILISATEURS
# =====================================================

@app.route("/utilisateurs")
def utilisateurs():

    if "admin" not in session:
        return redirect(url_for("login"))

    liste = afficher_utilisateurs()

    return render_template(
        "utilisateurs.html",
        utilisateurs=liste
    )


# =====================================================
# AJOUTER
# =====================================================

@app.route("/ajouter", methods=["POST"])
def ajouter():

    if "admin" not in session:
        return redirect(url_for("login"))

    uid = request.form["uid"]
    nom = request.form["nom"]
    service = request.form["service"]
    fonction = request.form["fonction"]
    email = request.form["email"]
    telephone = request.form["telephone"]

    actif = 1 if request.form.get("actif") else 0

    ajouter_utilisateur(
        uid,
        nom,
        service,
        fonction,
        email,
        telephone,
        actif
    )

    return redirect(url_for("utilisateurs"))


# =====================================================
# MODIFIER
# =====================================================

@app.route("/modifier/<int:id>", methods=["GET", "POST"])
def modifier(id):

    if "admin" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        modifier_utilisateur(
            id,
            request.form["uid"],
            request.form["nom"],
            request.form["service"],
            request.form["fonction"],
            request.form["email"],
            request.form["telephone"],
            1 if request.form.get("actif") else 0
        )

        return redirect(url_for("utilisateurs"))

    utilisateur = chercher_utilisateur(id)

    return render_template(
        "modifier_utilisateur.html",
        utilisateur=utilisateur
    )


# =====================================================
# SUPPRIMER
# =====================================================

@app.route("/supprimer/<int:id>")
def supprimer(id):

    if "admin" not in session:
        return redirect(url_for("login"))

    supprimer_utilisateur(id)

    return redirect(url_for("utilisateurs"))


# =====================================================
# TEST
# =====================================================

@app.route("/test")
def test():
    return "Serveur Flask fonctionne !"


# =====================================================
# API RFID
# =====================================================

@app.route("/api/rfid", methods=["POST"])
def api_rfid():

    print("\n==============================")
    print("REQUETE RECUE")

    data = request.get_json(silent=True)

    print("JSON :", data)

    if data is None:

        print("Aucun JSON reçu")

        return jsonify({
            "resultat": "ERREUR",
            "message": "JSON invalide"
        }), 400

    uid = data.get("uid", "").strip().upper()

    print("UID =", uid)

    utilisateur = chercher_carte(uid)

    print("Utilisateur =", utilisateur)

    if utilisateur is not None and utilisateur["actif"] == 1:

        enregistrer_acces(
            uid,
            utilisateur["nom"],
            "AUTORISE"
        )

        print("AUTORISE")

        return jsonify({
            "resultat": "AUTORISE",
            "nom": utilisateur["nom"]
        })

    enregistrer_acces(
        uid,
        "Inconnu",
        "REFUSE"
    )

    print("REFUSE")

    return jsonify({
        "resultat": "REFUSE"
    })


# =====================================================
# LANCEMENT
# =====================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )