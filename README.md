# Not Today, Newton 🍎

*Bugün olmaz, Newton!*

Newton bir elma ağacının altında oturuyor. Elmalardan biri kafasına düşerse yerçekimini keşfedecek.
Senin görevin, düşen elmaları sepetinle yakalayıp bu keşfi bir gün daha ertelemek.
Python ve [PyGame Zero](https://pygame-zero.readthedocs.io/) ile yazılmış küçük bir oyun.

Çocuklara Python'u oyun yaparak öğretmek için hazırladığım örnek bir proje:
kod kısa (tek dosya) ve her bölümü sade Türkçe açıklamalarla anlatılıyor.
İngilizce sürümü de var: [`game.py`](game.py) *(English version: [see below](#english))*.

<p>
  <img src="screenshots/gameplay.png" alt="Oyun ekranı: düşen elmalar ve sepet" width="380">
  <img src="screenshots/game-over.png" alt="Oyun bitti ekranı" width="380">
</p>

## Nasıl oynanır?

- **← →** ok tuşlarına her basışta sepet bir kare sola ya da sağa gider.
- Yakaladığın her elma **1 puan**.
- **3 elma** kaçırırsan *BONK!* Newton yerçekimini keşfeder ve oyun biter. Yeniden oynamak için oyunu tekrar başlat.
- Elmalar yarım saniyede bir, bir kare iner; her 5 puanda daha sık iner. Yerçekimi şakaya gelmez.
- Arka plandaki numaralı ızgara, bir elmanın hangi sütun ve satırda olduğunu gösterir.

## Çalıştırma

Python 3 ve PyGame Zero gerekir:

```bash
pip install pgzero
pgzrun oyun.py    # Türkçe sürüm
pgzrun game.py    # İngilizce sürüm
```

Debian/Ubuntu'da `pip` yerine `sudo apt install python3-pgzero` da olur.

## Kodda neler var?

| Kavram | Oyunda nerede? |
|---|---|
| Değişken | `puan`, `canlar`, `oyun_bitti` oyunun o anki durumunu tutar |
| Liste | `elmalar`: yeni elma `append` ile eklenir, yakalanan ya da düşen `remove` ile çıkarılır |
| Döngü | `for elma in elmalar[:]` ekrandaki her elmayı tek tek bir kare indirir; `izgara_ciz` içindeki iki döngü 12 sütunu ve 10 satırı çizer |
| Koşul | `if sepet.colliderect(elma)` elma sepete değdi mi? `elif elma.top > HEIGHT` yere mi düştü? |
| Fonksiyon | `yeni_elma` 3 saniyede bir yeni elma yapar (`update` içinden çağrılır), `izgara_ciz` numaralı kareleri çizer |
| Actor (resimli nesne) | `Actor("elma")` resmini `images/elma.png` dosyasından alır, `elma.draw()` ile çizilir |

`draw`, `update` ve `on_key_down` fonksiyonlarını kodun içinde hiç çağırmıyoruz:
PyGame Zero bu isimleri bulur ve onları kendisi çağırır (`draw` ile `update` saniyede 60 kez,
`on_key_down` bir tuşa basıldığında). `yeni_elma`'yı ise `update` içinden biz çağırıyoruz.

## Kendin dene

1. `BEKLEME = 60` yap. Elmalar ne sıklıkla iniyor? (60 adım = 1 saniye) Sonra `ELMA_ARALIGI = 60` dene: her saniye yeni elma gelince yetişebiliyor musun?
2. Bir elmanın `y`'si 375 ise kaçıncı satırdadır? İpucu: `375 // 50 + 1`. Oyunda ızgaraya bakıp kontrol et.
3. Elmanın resmini değiştir: kendi çizdiğin bir resmi `images/elma.png` adıyla kaydet ve oyunu yeniden çalıştır.
4. Arka planın rengini değiştir. İpucu: renkler (kırmızı, yeşil, mavi) karışımıdır; gece için `(20, 24, 60)` dene.
5. **Altın elma:** Bazen sarı bir elma düşsün ve yakalayınca 5 puan versin.
   İpucu: `yeni_elma` içinde `random.randint(1, 10) == 1` ise `Actor("altin_elma")` yap ve ayrı bir `altin_elmalar` listesine ekle.

## English

Newton is sitting under an apple tree. If an apple lands on his head, he will discover gravity. Not today!
Catch the falling apples with your basket and keep the discovery waiting one more day.
A tiny game made with Python and Pygame Zero to teach kids coding.

- Each **← →** arrow key press moves the basket one square. Every apple you catch is **1 point**.
- Miss **3 apples** and *BONK!* Newton discovers gravity and the game is over. Start it again to play again.
- Apples fall one square every half second, and more often every 5 points.
- The numbered grid in the background shows which column and row an apple is in.

```bash
pip install pgzero
pgzrun game.py
```

[`game.py`](game.py) is the English version of [`oyun.py`](oyun.py): same game, with English names and
kid-friendly English comments. It uses variables, a list, a `for` loop, `if`/`elif`, functions and Actors.
Code: MIT. Apple and basket images: Twemoji (CC-BY 4.0); Newton portrait: Godfrey Kneller, 1689 (public domain).
Details in the section below.

## Lisans

Kod [MIT](LICENSE) lisanslı: kopyala, değiştir, derste kullan, kendi oyununa dönüştür.

Görseller kendi lisanslarıyla kullanıldı:

- **Elma ve sepet** (`images/elma.png`, `images/sepet.png`, İngilizce sürüm için `apple.png`, `basket.png`): [Twemoji](https://github.com/jdecked/twemoji),
  © Twitter, Inc. ve katkıda bulunanlar, [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/).
  Kırpılıp yeniden boyutlandırıldı.
- **Newton portresi** (`images/newton.png`): Godfrey Kneller, 1689,
  [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:GodfreyKneller-IsaacNewton-1689.jpg), kamu malı.
  Yuvarlak kırpıldı.
