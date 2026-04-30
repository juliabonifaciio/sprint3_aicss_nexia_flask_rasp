from flask import Flask, render_template, request, redirect, session, url_for
import time
import os
import logging
from dotenv import load_dotenv
from functools import wraps

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

ADMIN_USER = os.getenv("ADMIN_USER")
ADMIN_PASS = os.getenv("ADMIN_PASS")

led_status = False
last_detection = 0
TIMEOUT = 10

logging.basicConfig(filename="app.log", level=logging.INFO)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logado" not in session:
            app.logger.warning("Acesso negado à área admin")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrap

@app.route("/")
def index():
    global last_detection
    ativo = False

    if last_detection:
        if time.time() - last_detection < TIMEOUT:
            ativo = True
        else:
            session.clear()
            app.logger.info("Sessão encerrada por inatividade")

    return render_template("index.html", ativo=ativo)

@app.route("/detectar")
def detectar():
    global last_detection
    last_detection = time.time()
    session["ativo"] = True
    app.logger.info("Presença detectada")
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("user", "").strip()
        senha = request.form.get("senha", "").strip()

        if not user or not senha:
            return "Preencha os campos"

        if user == ADMIN_USER and senha == ADMIN_PASS:
            session["logado"] = True
            app.logger.info("Login realizado com sucesso")
            return redirect("/admin")
        else:
            app.logger.warning("Tentativa de login inválida")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/admin")
@login_required
def admin():
    return render_template("admin.html", led=led_status)

@app.route("/led/on")
@login_required
def led_on():
    global led_status
    led_status = True
    app.logger.info("LED ligado")
    return redirect("/admin")

@app.route("/led/off")
@login_required
def led_off():
    global led_status
    led_status = False
    app.logger.info("LED desligado")
    return redirect("/admin")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
