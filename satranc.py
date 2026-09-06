import json
import os

DOSYA_YOLU = "veri.json"


def inception():
    dizilim = ["R", "N", "B", "Q", "K", "B", "N", "R"]
    board = {}

    for i, sutun in enumerate("abcdefgh"):
        board[f"{sutun}1"] = f"w{dizilim[i]}"
        board[f"{sutun}8"] = f"b{dizilim[i]}"
        board[f"{sutun}2"] = "wP"
        board[f"{sutun}7"] = "bP"

    return board


def veriyi_yukle():
    if os.path.exists(DOSYA_YOLU):
        with open(DOSYA_YOLU, "r") as f:
            veri = json.load(f)
            return veri["masa"], veri["yenenler"]
    return inception(), []


def veriyi_kaydet():
    with open(DOSYA_YOLU, "w") as f:
        json.dump({"masa": masa, "yenenler": yenenler}, f)


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