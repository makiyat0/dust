const sutunlar = ["a", "b", "c", "d", "e", "f", "g", "h"];
const KARE_BOYUTU = 90;

for (let satir = 8; satir >= 1; satir--) {
    for (let i = 0; i < 8; i++) {
        const kareDiv = document.createElement("div");
        kareDiv.classList.add("kare");
        const kareAdi = `${sutunlar[i]}${satir}`;
        kareDiv.dataset.kare = kareAdi;

        const left = i * KARE_BOYUTU;
        const top = (8 - satir) * KARE_BOYUTU;
        kareDiv.style.left = left + "px";
        kareDiv.style.top = top + "px";

        kareDiv.addEventListener("click", () => kareyeTiklandi(kareAdi));

        document.getElementById("tahta").appendChild(kareDiv);
    }
}

for (let satir = 8; satir >= 1; satir--) {
    const etiket = document.createElement("div");
    etiket.textContent = satir;
    document.getElementById("satir-etiketleri").appendChild(etiket);
}

for (let i = 0; i < 8; i++) {
    const etiket = document.createElement("div");
    etiket.textContent = sutunlar[i];
    document.getElementById("sutun-etiketleri").appendChild(etiket);
}

const TAS_RESIM_YOLU = "/static/images/pieces/";

async function tahtayiCiz() {
    const cevap = await fetch("/api/board");
    const veri = await cevap.json();
    const board = veri.masa;

    document.querySelectorAll(".kare").forEach((kareDiv) => {
        kareDiv.innerHTML = "";
    });

    for (const kareAdi in board) {
        const tasKodu = board[kareAdi];
        const kareDiv = document.querySelector(`[data-kare="${kareAdi}"]`);

        const img = document.createElement("img");
        img.src = TAS_RESIM_YOLU + tasKodu + ".png";
        img.classList.add("tas-resmi");

        kareDiv.appendChild(img);
    }
}

function kareyeTiklandi(kareAdi) {
    const hedefKare = prompt(`${kareAdi} karesindeki taş nereye gitsin?`);

    if (hedefKare) {
        hamleGonder(kareAdi, hedefKare.trim().toLowerCase());
    }
}

async function hamleGonder(nereden, nereye) {
    const cevap = await fetch("/api/move", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ from: nereden, to: nereye }),
    });

    const veri = await cevap.json();

    if (!veri.basarili) {
        alert(veri.hata);
        return;
    }

    tahtayiCiz();
}

tahtayiCiz();

setInterval(tahtayiCiz, 2000);
