from datetime import date
import os,random
from flask import Flask, render_template

app = Flask(__name__)



print("CALISILAN KLASOR:", os.getcwd())

def dosyadan_okuyucu(dosya_adi):
    yol = os.path.join("kehanet_araclari", dosya_adi)
    with open(yol, encoding="utf-8") as f:
        return [satir.strip() for satir in f if satir.strip()]


def memur_kehanetci():
    bugun = date.today().isoformat()
    random.seed(bugun)
    baslangic = dosyadan_okuyucu("baslangic.txt")
    ozne = dosyadan_okuyucu("ozne.txt")
    yuklem = dosyadan_okuyucu("yuklem.txt")

    return f"{random.choice(baslangic)} {random.choice(ozne)} {random.choice(yuklem)}"
    


@app.route("/")
def home():
    return render_template("index.html")
@app.route("/hakkinda")
def hakkinda():
    return render_template("hakkinda.html")
@app.route("/kehanetci")
def kehanteci():
    kehanet = memur_kehanetci()
    return render_template("kehanetci.html", kehanet=kehanet)

if __name__ == "__main__":
    app.run()