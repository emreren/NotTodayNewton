# Elma Yakala — PyGame Zero ile yazılmış küçük bir oyun
WIDTH = 600
HEIGHT = 500

sepet = Rect(250, 450, 100, 20)  # x, y, genişlik, yükseklik


def draw():
    screen.fill((135, 206, 235))  # gökyüzü mavisi
    screen.draw.filled_rect(sepet, (139, 69, 19))  # kahverengi sepet