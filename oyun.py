# ==================================================
#  NOT TODAY, NEWTON  (Bugün olmaz, Newton!)
#  Newton bir elma ağacının altında oturuyor. Elmalardan biri
#  kafasına düşerse yerçekimini keşfedecek. Bugün olmaz!
#  Ok tuşlarına her basışta sepetin bir kare sola ya da sağa gider.
#  Elmaları yakala! 3 elma kaçırırsan Newton yerçekimini keşfeder ve oyun biter.
#
#  Çalıştırmak için terminalde:  pgzrun oyun.py  ya da  python3 oyun.py  ( ▶ tuşu da olur)
#
#  draw, update ve on_key_down fonksiyonlarını biz çağırmıyoruz.
#  PyGame Zero bu isimleri arar ve onları kendisi çağırır.
#  Bu yüzden adları İngilizce ve tam olarak böyle yazılmalı.
# ==================================================

import pgzrun  # PyGame Zero'yu hazırlar: Actor, screen, keyboard gibi adlar bununla gelir
import random  # rastgele sayı seçmemizi sağlayan hazır bir araç


# ---------- AYARLAR ----------
# Bu sayıları değiştirerek oyunu kolaylaştırabilir ya da zorlaştırabilirsin.

TITLE = "Not Today, Newton"  # pencerenin üstünde yazan isim
WIDTH = 600            # pencerenin genişliği: 12 kare
HEIGHT = 500           # pencerenin yüksekliği: 10 kare
KARE = 50              # ızgaradaki her kare kaç nokta (elmalar ve sepet kare kare gider)
BEKLEME = 30           # elmalar kaç adımda bir kare iner (saniyede 60 adım: 30 = yarım saniye)
ELMA_ARALIGI = 3       # kaç saniyede bir yeni elma düşsün
IZGARA = True          # numaralı ızgarayı göster (False yaparsan gizlenir)


# ---------- OYUNDAKİ ŞEYLER ----------
# Actor, oyundaki resimli bir nesne demek. Resmini "images" klasöründe
# kendi adıyla arar: Actor("sepet") → images/sepet.png
# Actor'ün x ve y'si resmin ORTASIDIR. Kenarları da var: left, right, top, bottom.
# Dikkat: ekranda aşağı indikçe sayılar BÜYÜR. En üst 0, en alt 500.

sepet = Actor("sepet", midbottom=(275, HEIGHT))  # en altta, 6. sütunun ortasında (5 × 50 + 25)
elmalar = []         # ekrandaki bütün elmaları tutan liste (başta boş)
puan = 0             # kaç elma yakaladın
canlar = 3           # kaç elma daha kaçırabilirsin
en_yuksek = 0        # şimdiye kadarki en iyi puanın
oyun_bitti = False   # oyun bitti mi? Başta "hayır" (False)
sayac = 0            # elmaları indirmeden önce kaç adım beklediğimizi sayar


# ---------- YENİ ELMA ----------

def yeni_elma():
    # Rastgele bir sütun seç, elmayı o sütunun ortasına, ekranın hemen üstüne koy
    sutun = random.randint(0, WIDTH // KARE - 1)  # 0 ile 11 arası bir sütun
    x = sutun * KARE + KARE / 2                    # sütunun ortası
    elma = Actor("elma", (x, -KARE / 2))           # ekranın bir kare üstünden başlasın
    elmalar.append(elma)                           # yeni elmayı listeye ekle


# ---------- YENİ OYUN ----------

def yeni_oyun():
    # Her şeyi oyunun en başındaki hâline getir
    global puan, canlar, oyun_bitti  # yukarıdaki bu değişkenleri değiştireceğiz
    puan = 0
    canlar = 3
    oyun_bitti = False
    elmalar.clear()  # listedeki bütün elmaları sil
    sepet.x = 275    # sepeti 6. sütuna geri koy


# ---------- NUMARALI IZGARA ----------
# Elmanın ekranda nerede olduğunu görmek için arka plana bir harita çizer.
# Her kare 50 nokta: 3. sütun x'in 100 ile 150 arası, 5. satır y'nin 200 ile 250 arası.
# Satır numaraları solda, sütun numaraları altta (satranç tahtası gibi).

def izgara_ciz():
    cizgi_rengi = (205, 235, 250)  # gökyüzünden açık bir mavi

    for sutun in range(WIDTH // KARE):  # 600 // 50 = 12 sütun: 0, 1, 2, ... 11
        x = sutun * KARE                # bu sütunun sol kenarı
        screen.draw.line((x, 0), (x, HEIGHT), cizgi_rengi)  # dikey çizgi
        # Saymaya 0'dan başladık ama numarayı 1'den yazıyoruz
        screen.draw.text(str(sutun + 1), center=(x + KARE / 2, HEIGHT - 12),
                         fontsize=20, color="white")

    for satir in range(HEIGHT // KARE):  # 500 // 50 = 10 satır: 0, 1, 2, ... 9
        y = satir * KARE                 # bu satırın üst kenarı
        screen.draw.line((0, y), (WIDTH, y), cizgi_rengi)   # yatay çizgi
        screen.draw.text(str(satir + 1), center=(12, y + 12),
                         fontsize=20, color="white")


# ---------- EKRANI ÇİZ ----------
# PyGame Zero bu fonksiyonu saniyede 60 kez kendisi çağırır.
# Renkler (kırmızı, yeşil, mavi) karışımıdır; her biri 0 ile 255 arasında.

def draw():
    screen.fill((135, 206, 235))  # her yeri gökyüzü mavisine boya
    if IZGARA and not oyun_bitti:
        izgara_ciz()              # oyun sürerken arka plana numaralı ızgarayı çiz
    sepet.draw()                  # sepetin resmini çiz

    for elma in elmalar:  # listedeki her elma için...
        elma.draw()       # ...elmanın resmini çiz

    # Sol üste puanı (satır numaralarına değmesin diye biraz sağda), sağ üste canları yaz
    screen.draw.text(f"Puan: {puan}", topleft=(35, 10), fontsize=32, color="white")
    screen.draw.text(f"Can: {canlar}", topright=(WIDTH - 10, 10), fontsize=32, color="white")

    # Oyun bittiyse Newton'u göster ve ekranın ortasına büyük harflerle yaz
    if oyun_bitti:
        orta = WIDTH / 2
        screen.blit("newton", (orta - 60, 45))  # images/newton.png, 120 nokta genişliğinde
        screen.draw.text("OYUN BİTTİ", center=(orta, 205), fontsize=72, color="white")
        screen.draw.text("BONK! Newton yerçekimini keşfetti.",
                         center=(orta, 255), fontsize=30, color="white")
        screen.draw.text(f"Puan: {puan}    En yüksek: {en_yuksek}",
                         center=(orta, 300), fontsize=36, color="white")
        screen.draw.text("Yeniden başlamak için BOŞLUK tuşuna bas",
                         center=(orta, 345), fontsize=28, color="white")


# ---------- ELMALARI İNDİR ----------
# PyGame Zero bu fonksiyonu da saniyede 60 kez çağırır, ekranı çizmeden hemen önce.
# Her çağrılmasına bir "adım" diyelim.

def update():
    global puan, canlar, en_yuksek, oyun_bitti, sayac  # bunları değiştireceğiz

    # Oyun bittiyse burada dur, hiçbir şeyi hareket ettirme
    if oyun_bitti:
        return

    # Elmaları her adımda değil, birkaç adımda bir indiriyoruz; böylece kare kare iniyorlar.
    # Her 5 puanda bekleme kısalır, elmalar daha sık iner.
    # (// bölmenin tam kısmını verir: 12 // 5 = 2)
    bekleme = max(15, BEKLEME - (puan // 5) * 5)
    sayac += 1
    if sayac < bekleme:
        return    # daha zamanı gelmedi
    sayac = 0     # zamanı geldi: sayacı sıfırla ve elmaları indir

    # Listedeki her elmaya sırayla bak.
    # elmalar[:] listenin bir kopyası. Döngünün içinde elma sileceğimiz için
    # kopyayı geziyoruz; yoksa bazı elmalar atlanırdı.
    for elma in elmalar[:]:
        elma.y += KARE  # elmayı bir kare aşağı indir

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
    # Oyun bittiyse: BOŞLUK tuşu yeni oyun başlatır, başka tuşlar bir şey yapmaz
    if oyun_bitti:
        if key == keys.SPACE:
            yeni_oyun()
        return

    # Ok tuşuna her basışta sepet bir kare sola ya da sağa gider (pencereden çıkmadan)
    if key == keys.LEFT and sepet.left > 0:
        sepet.x -= KARE  # x küçülürse sepet sola gider
    if key == keys.RIGHT and sepet.right < WIDTH:
        sepet.x += KARE  # x büyürse sepet sağa gider


# Her ELMA_ARALIGI saniyede bir yeni_elma fonksiyonunu çalıştır (alarm kurmak gibi)
clock.schedule_interval(yeni_elma, ELMA_ARALIGI)

pgzrun.go()  # oyunu başlat
