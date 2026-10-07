# ==================================================
#  ELMA YAKALA
#  Gökyüzünden elmalar düşüyor. Sepetini ok tuşlarıyla
#  sağa sola götür ve elmaları yakala!
#  3 elma kaçırırsan oyun biter.
#
#  Çalıştırmak için aynı dizinde bu komutu çalıştır:  pgzrun oyun.py
#
#  draw, update ve on_key_down fonksiyonlarını biz çağırmıyoruz.
#  PyGame Zero bu isimleri arar ve onları kendisi çağırır.
#  Bu yüzden adları İngilizce ve tam olarak böyle yazılmalı.
# ==================================================

import random  # rastgele sayı seçmemizi sağlayan hazır bir araç


# ---------- AYARLAR ----------
# Bu sayıları değiştirerek oyunu kolaylaştırabilir ya da zorlaştırabilirsin.

TITLE = "Elma Yakala"  # pencerenin üstünde yazan isim
WIDTH = 600            # pencerenin genişliği
HEIGHT = 500           # pencerenin yüksekliği
HIZ = 6                # sepet her adımda kaç nokta kayacak
DUSME_HIZI = 3         # elmalar oyunun başında ne kadar hızlı düşecek


# ---------- OYUNDAKİ ŞEYLER ----------
# Rect bir dikdörtgen demek: Rect(soldan, yukarıdan, genişlik, yükseklik)
# Dikkat: ekranda aşağı indikçe sayılar BÜYÜR. En üst 0, en alt 500.

sepet = Rect(250, 450, 100, 20)  # sepet ekranın altında duruyor
elmalar = []         # ekrandaki bütün elmaları tutan liste (başta boş)
puan = 0             # kaç elma yakaladın
canlar = 3           # kaç elma daha kaçırabilirsin
en_yuksek = 0        # şimdiye kadarki en iyi puanın
oyun_bitti = False   # oyun bitti mi? Başta "hayır" (False)


# ---------- YENİ ELMA ----------

def yeni_elma():
    # Pencerenin hemen üstünde, rastgele bir yerde yeni bir elma yap
    x = random.randint(0, WIDTH - 20)  # 20 çıkarıyoruz ki elma sağdan taşmasın
    elma = Rect(x, -20, 20, 20)        # -20: elma ekranın biraz üstünden gelsin
    elmalar.append(elma)               # yeni elmayı listeye ekle


# ---------- YENİ OYUN ----------

def yeni_oyun():
    # Her şeyi oyunun en başındaki hâline getir
    global puan, canlar, oyun_bitti  # yukarıdaki bu değişkenleri değiştireceğiz
    puan = 0
    canlar = 3
    oyun_bitti = False
    elmalar.clear()  # listedeki bütün elmaları sil
    sepet.x = 250    # sepeti ortaya geri koy


# ---------- EKRANI ÇİZ ----------
# PyGame Zero bu fonksiyonu saniyede 60 kez kendisi çağırır.
# Renkler (kırmızı, yeşil, mavi) karışımıdır; her biri 0 ile 255 arasında.

def draw():
    screen.fill((135, 206, 235))                   # her yeri gökyüzü mavisine boya
    screen.draw.filled_rect(sepet, (139, 69, 19))  # kahverengi sepeti çiz

    for elma in elmalar:  # listedeki her elma için...
        screen.draw.filled_circle(elma.center, 10, (220, 20, 60))  # ...kırmızı bir daire çiz

    # Sol üste puanı, sağ üste kalan canları yaz
    screen.draw.text(f"Puan: {puan}", topleft=(10, 10), fontsize=32, color="white")
    screen.draw.text(f"Can: {canlar}", topright=(WIDTH - 10, 10), fontsize=32, color="white")

    # Oyun bittiyse ekranın ortasına büyük harflerle yaz
    if oyun_bitti:
        orta = WIDTH / 2
        screen.draw.text("OYUN BİTTİ", center=(orta, 190), fontsize=72, color="white")
        screen.draw.text(f"Puan: {puan}    En yüksek: {en_yuksek}",
                         center=(orta, 250), fontsize=36, color="white")
        screen.draw.text("Yeniden başlamak için BOŞLUK tuşuna bas",
                         center=(orta, 300), fontsize=28, color="white")


# ---------- HER ŞEYİ HAREKET ETTİR ----------
# PyGame Zero bu fonksiyonu da saniyede 60 kez çağırır, ekranı çizmeden hemen önce.

def update():
    global puan, canlar, en_yuksek, oyun_bitti  # yukarıdaki bu değişkenleri değiştireceğiz

    # Oyun bittiyse burada dur, hiçbir şeyi hareket ettirme
    if oyun_bitti:
        return

    # Sol oka basıyorsan sepet sola, sağ oka basıyorsan sağa gitsin
    if keyboard.left:
        sepet.x -= HIZ  # x küçülürse sepet sola gider
    if keyboard.right:
        sepet.x += HIZ  # x büyürse sepet sağa gider

    # Sepet pencerenin dışına kaçmasın
    if sepet.left < 0:
        sepet.left = 0
    if sepet.right > WIDTH:
        sepet.right = WIDTH

    # Her 5 puanda elmalar biraz daha hızlı düşsün
    # (// bölmenin tam kısmını verir: 12 // 5 = 2)
    dusme_hizi = DUSME_HIZI + puan // 5

    # Listedeki her elmaya sırayla bak.
    # elmalar[:] listenin bir kopyası. Döngünün içinde elma sileceğimiz için
    # kopyayı geziyoruz; yoksa bazı elmalar atlanırdı.
    for elma in elmalar[:]:
        elma.y += dusme_hizi  # elmayı biraz aşağı indir

        if sepet.colliderect(elma):
            # EĞER elma sepete değdiyse: yakaladın! 1 puan kazan.
            puan += 1
            elmalar.remove(elma)
        elif elma.top > HEIGHT:
            # DEĞİLSE, EĞER elma yere düştüyse: kaçırdın! 1 can kaybet.
            canlar -= 1
            elmalar.remove(elma)

    # Hiç can kalmadıysa oyun biter
    if canlar <= 0:
        oyun_bitti = True
        en_yuksek = max(en_yuksek, puan)  # ikisinden büyük olanı en yüksek puan yap


# ---------- TUŞA BASILINCA ----------
# Bir tuşa bastığında PyGame Zero bu fonksiyonu kendisi çağırır.

def on_key_down(key):
    # Oyun bittiyse ve BOŞLUK tuşuna bastıysan yeni oyun başlasın
    if oyun_bitti and key == keys.SPACE:
        yeni_oyun()


# Her 1 saniyede bir yeni_elma fonksiyonunu çalıştır (alarm kurmak gibi)
clock.schedule_interval(yeni_elma, 1.0)
