import json
import os
import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL")


def _baglanti_ac():
    return psycopg2.connect(DATABASE_URL)


def inception():
    dizilim = ["R", "N", "B", "Q", "K", "B", "N", "R"]
    board = {}

    for i, sutun in enumerate("abcdefgh"):
        board[f"{sutun}1"] = f"w{dizilim[i]}"
        board[f"{sutun}8"] = f"b{dizilim[i]}"
        board[f"{sutun}2"] = "wP"
        board[f"{sutun}7"] = "bP"

    return board


def veritabanini_hazirla():
    """Uygulama açılırken bir kere çağrılır - tablo yoksa oluşturur."""
    conn = _baglanti_ac()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS durum (
            id INTEGER PRIMARY KEY,
            masa TEXT,
            yenenler TEXT
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


def veriyi_yukle():
    conn = _baglanti_ac()
    cur = conn.cursor()
    cur.execute("SELECT masa, yenenler FROM durum WHERE id = 1")
    satir = cur.fetchone()

    if satir is None:
        # İlk açılış - başlangıç tahtasını veritabanına yaz
        baslangic = inception()
        cur.execute(
            "INSERT INTO durum (id, masa, yenenler) VALUES (1, %s, %s)",
            (json.dumps(baslangic), json.dumps([]))
        )
        conn.commit()
        cur.close()
        conn.close()
        return baslangic, []

    cur.close()
    conn.close()
    return json.loads(satir[0]), json.loads(satir[1])


def veriyi_kaydet():
    conn = _baglanti_ac()
    cur = conn.cursor()
    cur.execute(
        "UPDATE durum SET masa = %s, yenenler = %s WHERE id = 1",
        (json.dumps(masa), json.dumps(yenenler))
    )
    conn.commit()
    cur.close()
    conn.close()


veritabanini_hazirla()
masa, yenenler = veriyi_yukle()


def bozmaz_mi(gelen):
    return len(gelen) == 2 and gelen[0] in "abcdefgh" and gelen[1] in "12345678"


def oynatici(nereden, nereye, board=masa, captured=yenenler):
    if not (bozmaz_mi(nereye) and bozmaz_mi(nereden)):
        return False, "yassah gardaşım"

    if nereden not in board:
        return False, "orada taş yok"

    if nereye in board:
        captured.append(board[nereye])

    board[nereye] = board[nereden]
    board.pop(nereden)

    veriyi_kaydet()

    return True, None