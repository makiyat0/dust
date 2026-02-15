from datetime import datetime,date
import os
import random
from flask import Flask, render_template

app = Flask(__name__)

BASE_PATH = "kehanet_araclari"

undr_cs = ["üzgünüm buraı bitiremedim daha",
           "yapım aşamasında",
           "erken öten horoz",
           "saskın gelme sözlerim kayıp ayıp ediyoru mkendime",
           "en azından tarihte iz bıraksın bu sayfa"]


print("CALISILAN KLASOR:", os.getcwd())

# --------------------
# DOSYADAN OKUMA
# --------------------
def load_words(filename):
    path = os.path.join(BASE_PATH, filename)
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def yoksayfa(yapim_asamasi):
    bugun = date.today().isoformat()
    random.seed(bugun)
    yapim_asamasi = undr_cs
    return random.choice(yapim_asamasi)



# --------------------
# FİİLİ GENİŞ ZAMANA ÇEK
# --------------------
def genis_zaman(fiil):
    if fiil.endswith("mak") or fiil.endswith("mek"):
        kok = fiil[:-3]
    else:
        return fiil

    kalin = "aıou"
    ince = "eiöü"

    son_unlu = None
    for harf in reversed(kok):
        if harf in kalin + ince:
            son_unlu = harf
            break

    if son_unlu in kalin:
        return kok + "ar"
    else:
        return kok + "er"

# --------------------
# KELİME HAVUZLARI
# --------------------
baglaclar  = load_words("baglac.txt")
nesneler  = load_words("nesne.txt")
ozneler   = load_words("ozne.txt")
sifatlar  = load_words("sifat.txt")
yuklemler = load_words("yuklem.txt")

word_map = {
    "sifat": sifatlar,
    "ozne": ozneler,
    "nesne": nesneler,
    "yuklem": yuklemler,
    "baglac": baglaclar
}

# --------------------
# CÜMLE KALIPLARI
# --------------------
sentence_patterns = [
    ["sifat", "ozne", "nesne", "yuklem"],
    ["ozne", "yuklem"],
    ["sifat", "ozne", "yuklem"],
    ["ozne", "nesne", "yuklem"],
    ["sifat", "ozne", "baglac", "ozne", "yuklem"]
]

# --------------------
# GÜNLÜK KEHANET
# --------------------
def memur_kehanetci():
    bugun = date.today().isoformat()
    random.seed(bugun)  # her güne 1 kehanet

    pattern = random.choice(sentence_patterns)
    words = []

    for item in pattern:
        kelime = random.choice(word_map[item])
        if item == "yuklem":
            kelime = genis_zaman(kelime)
        words.append(kelime)

    return " ".join(words).capitalize() + "."

# --------------------
# ROUTES
# --------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/hakkinda")
def hakkinda():
    return render_template("hakkinda.html")

@app.route("/kehanetci")
def kehanetci():
    kehanet = memur_kehanetci()
    return render_template("kehanetci.html", kehanet=kehanet)

def oguz_cumle(filename):
    now = datetime.now()

    # Saat bazlı seed (yıl, ay, gün, saat)
    seed = now.year * 1000000 + now.month * 10000 + now.day * 100 + now.hour
    path = filename
    random.seed(seed)
    with open(path, "r", encoding="utf-8") as f:
        cumle = f.read().splitlines()


    return random.choice(cumle)


@app.route("/oguz")
def oguz():
    cümlemiz = oguz_cumle("oyunlu_tehlike.txt")
    return render_template("oguz.html",cümlemiz=cümlemiz)

@app.route("/thenullmoon")
def null():
    moon = yoksayfa(undr_cs)
    giselle = "özür dilerim, kedni kafamda halletmem gereken şeyler var sesninle konuşmalarımız bazı arkaya attığım gerçekleri tekrar değerlendirmek zorunda bıraktı iyi oldu aslında ama içinden çıktığımda hayatımın neleri değişecek ve neleri aynı kalacak bilmiyorum (bu cümle 14 02 2026 tarihinde yazılmıştır) "
    syf = "79. sayfadayım"

    return render_template("thenullmoon.html", moon=moon, giselle=giselle, syf=syf)




# --------------------
# RUN
# --------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)