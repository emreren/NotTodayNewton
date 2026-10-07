# NOT TODAY, NEWTON (Bugün olmaz, Newton!)
# Newton bir elma ağacının altında oturuyor. Kafasına elma düşerse yerçekimini keşfedecek!
# Ok tuşlarıyla sepeti bir kare sola ya da sağa götür ve elmaları yakala.
# 3 elma kaçırırsan oyun biter.
# Çalıştırmak için:  pgzrun oyun.py  ya da  python3 oyun.py

import pgzrun  # PyGame Zero: Actor, screen gibi hazır adlar buradan gelir
import random  # rastgele sayı seçmek için

# ---------- AYARLAR ----------
TITLE = "Not Today, Newton"
WIDTH = 600          # pencerenin genişliği: 12 kare
HEIGHT = 500         # pencerenin yüksekliği: 10 kare
KARE = 50            # bir karenin boyu
BEKLEME = 30         # elmalar kaç adımda bir kare iner (saniyede 60 adım var)
ELMA_ARALIGI = 180   # kaç adımda bir yeni elma gelir (180 adım = 3 saniye)

# ---------- OYUNDAKİ ŞEYLER ----------
# Actor resimli bir nesnedir; resmini images klasöründen alır (images/sepet.png).
# Dikkat: ekranda aşağı indikçe y büyür. En üst 0, en alt 500.
sepet = Actor("sepet", midbottom=(275, HEIGHT))  # en alt satırda, 6. sütunda
elmalar = []       # ekrandaki bütün elmalar
puan = 0
canlar = 3
oyun_bitti = False
sayac = 0          # elmaları indirmek için adım sayacı
elma_sayaci = 0    # yeni elma için adım sayacı


def yeni_elma():
    # Rastgele bir sütun seç ve elmayı o sütunun ortasına, ekranın hemen üstüne koy
    sutun = random.randint(0, 11)
    elma = Actor("elma", (sutun * KARE + 25, -25))
    elmalar.append(elma)


def izgara_ciz():
    # Arka plana numaralı kareler çiz. Satır numarası da y gibi aşağı doğru büyür.
    for sutun in range(12):
        x = sutun * KARE
        screen.draw.line((x, 0), (x, HEIGHT), (205, 235, 250))
        screen.draw.text(str(sutun + 1), center=(x + 25, HEIGHT - 12), fontsize=20)
    for satir in range(10):
        y = satir * KARE
        screen.draw.line((0, y), (WIDTH, y), (205, 235, 250))
        screen.draw.text(str(satir + 1), center=(12, y + 12), fontsize=20)


def draw():
    # PyGame Zero bu fonksiyonu saniyede 60 kez kendisi çağırır ve ekranı baştan çizer
    screen.fill((135, 206, 235))  # gökyüzü mavisi

    if oyun_bitti:
        screen.blit("newton", (240, 45))
        screen.draw.text("OYUN BİTTİ", center=(300, 205), fontsize=72)
        screen.draw.text("BONK! Newton yerçekimini keşfetti.", center=(300, 255), fontsize=30)
        screen.draw.text(f"Puan: {puan}", center=(300, 300), fontsize=36)
        return

    izgara_ciz()
    sepet.draw()
    for elma in elmalar:
        elma.draw()
    screen.draw.text(f"Puan: {puan}", topleft=(35, 10), fontsize=32)
    screen.draw.text(f"Can: {canlar}", topright=(590, 10), fontsize=32)


def update():
    # PyGame Zero bunu da saniyede 60 kez çağırır. Her çağrıya bir "adım" diyelim.
    global puan, canlar, oyun_bitti, sayac, elma_sayaci
    if oyun_bitti:
        return

    # Her ELMA_ARALIGI adımda bir yeni elma yap
    elma_sayaci += 1
    if elma_sayaci == ELMA_ARALIGI:
        elma_sayaci = 0
        yeni_elma()

    # Elmalar her adımda değil, birkaç adımda bir iner.
    # Her 5 puanda 5 adım daha az bekleriz, yani elmalar hızlanır (ama en az 15 adım).
    bekleme = BEKLEME - (puan // 5) * 5
    if bekleme < 15:
        bekleme = 15
    sayac += 1
    if sayac < bekleme:
        return
    sayac = 0

    # Her elmayı bir kare indir. elmalar[:] listenin kopyası, çünkü döngüde elma sileceğiz.
    for elma in elmalar[:]:
        elma.y += KARE

        if sepet.colliderect(elma):
            # EĞER elma sepete değdiyse: 1 puan kazan
            puan += 1
            elmalar.remove(elma)
        elif elma.top > HEIGHT:
            # DEĞİLSE, EĞER elma yere düştüyse: 1 can kaybet
            canlar -= 1
            elmalar.remove(elma)

    if canlar == 0:
        oyun_bitti = True


def on_key_down(key):
    # Ok tuşuna her basışta sepet bir kare kayar (ekrandan çıkmadan)
    if key == keys.LEFT and sepet.left > 0:
        sepet.x -= KARE
    if key == keys.RIGHT and sepet.right < WIDTH:
        sepet.x += KARE


pgzrun.go()  # oyunu başlat
