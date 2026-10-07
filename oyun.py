# Elma Yakala — PyGame Zero ile yazılmış küçük bir oyun
import random

WIDTH = 600
HEIGHT = 500
HIZ = 6  # sepetin her karede kaç piksel kaydığı
DUSME_HIZI = 3  # elmanın her karede kaç piksel düştüğü

sepet = Rect(250, 450, 100, 20)  # x, y, genişlik, yükseklik
elma = Rect(300, 0, 20, 20)

def draw():
    screen.fill((135, 206, 235))  # gökyüzü mavisi
    screen.draw.filled_rect(sepet, (139, 69, 19))  # kahverengi sepet
    screen.draw.filled_circle(elma.center, 10, (220, 20, 60))  # kırmızı elma


def update():
    # Ok tuşlarına basılıysa sepeti kaydır
    if keyboard.left:
        sepet.x -= HIZ
    if keyboard.right:
        sepet.x += HIZ

    # Sepet pencereden taşmasın
    if sepet.left < 0:
        sepet.left = 0
    if sepet.right > WIDTH:
        sepet.right = WIDTH

    # Elma aşağı düşsün (y aşağı doğru büyür)
    elma.y += DUSME_HIZI

    # Elma yere düşünce yukarıdan, rastgele bir yerden yeniden başlasın
    if elma.top > HEIGHT:
        elma.x = random.randint(0, WIDTH - elma.width)
        elma.bottom = 0