import pygame
import sys
import random
import math
from random import randint
from pygame import mixer
from os.path import join

# Pygame'i başlat
pygame.init()

# Ses sistemini başlat
mixer.init()

# Ekran boyutları
GENISLIK = 800
YUKSEKLIK = 600

# Renkler
BEYAZ = (255, 255, 255)
MAVI = (0, 0, 255)
KIRMIZI = (255, 0, 0)
SARI = (255, 255, 0)
YESIL = (0, 255, 0)
SIYAH = (0, 0, 0)
TURKUAZ = (0, 206, 209)
KOYU_TURKUAZ = (0, 166, 169)
ACIK_TURKUAZ = (64, 224, 208)
PEMBE = (255, 192, 203)
MOR = (147, 112, 219)

# Ses dosyaları için sabitler
SES_KLASORU = "sesler"  # sesler klasörü oluşturun
MUZIK_SES = 0.5        # müzik ses seviyesi (0.0 - 1.0)
EFEKT_SES = 0.3        # efekt ses seviyesi

# Ekranı oluştur
ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("ToplareSa")

# Font tanımla
font = pygame.font.Font(None, 28)

# Renklerin altına yeni sabitler ekliyoruz
SEVIYE_PUAN_GEREKSINIMLERI = {
    1: 5,   # 1. seviye için 5 puan
    2: 12,  # 2. seviye için 12 puan
    3: 20,  # 3. seviye için 20 puan
    4: 30,  # 4. seviye için 30 puan
    5: 45   # 5. seviye için 45 puan
}

PARCACIK_YASAM_SURESI = 30  # kaç frame yaşayacağı
TOPLAMA_ANIMASYON_SURESI = 15

# Renk sabitleri altına yeni renkler ve efekt seçenekleri ekleyelim
RENK_SECENEKLERI = {
    "Turkuaz": TURKUAZ,
    "Pembe": PEMBE,
    "Mor": MOR,
    "Yeşil": YESIL,
    "Mavi": MAVI,
    "Sarı": SARI,
    "Beyaz": BEYAZ,
    "Kırmızı": KIRMIZI
}

EFEKT_SECENEKLERI = {
    "Beyaz İz": BEYAZ,
    "Turkuaz İz": TURKUAZ,
    "Pembe İz": PEMBE,
    "Mor İz": MOR,
    "Yeşil İz": YESIL,
    "Mavi İz": MAVI,
    "Sarı İz": SARI,
    "Kırmızı İz": KIRMIZI
}

# Sabitler kısmına ekleyin
OYUN_MODLARI = {
    "Klasik": "klasik",
    "Zaman Yarışı": "zaman",
    "Hayatta Kalma": "survival"
}

ZAMAN_SINIRI = 60  # saniye
LABIRENT_DUVAR_KALINLIK = 20

# Sabitler kısmına meyve türlerini ekleyelim
MEYVELER = {
    "elma": (255, 0, 0),      # Kırmızı
    "muz": (255, 255, 0),     # Sarı
    "üzüm": (128, 0, 128),    # Mor
    "portakal": (255, 165, 0), # Turuncu
    "kivi": (154, 205, 50)     # Yeşilimsi
}

# Sabitler kısmına TNT özellikleri ekleyin
TNT_RENK = (184, 37, 37)  # Koyu kırmızı
TNT_YAZI_RENK = (255, 255, 255)  # Beyaz
TNT_BOYUT = 30

# Sabitler kısmına güç-yükseltme sabitleri ekleyin
GUC_TIPLERI = {
    "hiz": {
        "renk": (255, 215, 0),  # Altın
        "sembol": "H",
        "sure": 5  # saniye
    },
    "kalkan": {
        "renk": (0, 191, 255),  # Mavi
        "sembol": "K",
        "sure": 3
    },
    "puan2x": {
        "renk": (148, 0, 211),  # Mor
        "sembol": "2X",
        "sure": 7
    },
    "miknatis": {
        "renk": (169, 169, 169),  # Gri
        "sembol": "M",
        "sure": 4
    },
    "kucult": {
        "renk": (255, 105, 180),  # Pembe
        "sembol": "↓",
        "sure": 6
    }
}

GUC_BOYUT = 25
GUC_OLUSTURMA_SURESI = 15000  # 15 saniye (milisaniye cinsinden)

# Sabitler kısmına hayatta kalma modu sabitleri ekleyin
BASLANGIC_CAN = 3
CAN_YENILEME_PUANI = 10  # Her 10 puanda bir can kazanma

# Sabitler kısmına ekleyin
RESIM_KLASORU = "resimler"  # resimler klasörü oluşturun

BASARIMLAR = {
    "baslangic": {"ad": "Başlangıç", "aciklama": "İlk puanını kazan", "tamamlandi": False},
    "hizli": {"ad": "Hızlı", "aciklama": "10 saniyede 5 puan topla", "tamamlandi": False},
    "usta": {"ad": "Usta", "aciklama": "50 puan topla", "tamamlandi": False}
}

IPUCLARI = [
    "F11 tuşu ile tam ekran moduna geçebilirsin",
    "Güçlendirmeler sana avantaj sağlar!",
    "Her 10 puanda bir can kazanırsın"
]

# Sabitler kısmına eklenecek yeni sabitler
COMBO_SURESI = 2000  # 2 saniye

OZEL_GUCLER = {
    "super_hiz": {"tuş": pygame.K_SPACE, "süre": 3, "cooldown": 10},
    "zaman_yavas": {"tuş": pygame.K_LSHIFT, "süre": 5, "cooldown": 15}
}

SEVIYE_BONUSLARI = {
    "can": "Ekstra Can",
    "hiz": "Kalıcı Hız Artışı",
    "kucuk": "Karakter Küçültme",
    "puan": "Puan Çarpanı"
}

GUNLUK_GOREVLER = {
    "hizli": {"ad": "Hızlı Başlangıç", "hedef": 10, "aciklama": "10 saniyede 5 puan topla"},
    "combo": {"ad": "Combo Ustası", "hedef": 5, "aciklama": "5 combo yap"},
    "engel": {"ad": "Tehlikeli Yaşam", "hedef": 30, "aciklama": "Engellere çarpmadan 30 saniye hayatta kal"}
}

KOSTUMLER = {
    "normal": {"renk": TURKUAZ, "efekt": None},
    "ninja": {"renk": SIYAH, "efekt": "golge"},
    "alev": {"renk": KIRMIZI, "efekt": "parlak"},
    "buz": {"renk": MAVI, "efekt": "kristal"}
}

class Parcacik:
    def __init__(self, x, y, renk):
        self.x = x
        self.y = y
        self.renk = renk
        self.yasam = PARCACIK_YASAM_SURESI
        self.hiz_x = random.uniform(-2, 2)
        self.hiz_y = random.uniform(-2, 2)
        self.boyut = random.randint(8, 12)  # Meyveleri biraz daha büyük yaptık
        self.meyve_turu = random.choice(list(MEYVELER.keys()))
    
    def guncelle(self):
        # Parçacığın pozisyonunu güncelle
        self.x += self.hiz_x
        self.y += self.hiz_y
        self.yasam -= 1
    
    def meyve_ciz(self, surface, renk, boyut):
        if self.meyve_turu == "elma":
            # Elma gövdesi
            pygame.draw.circle(surface, (255, 0, 0), (boyut, boyut), boyut)
            # Sap
            pygame.draw.line(surface, (101, 67, 33), 
                           (boyut, 0), (boyut, boyut//2), 2)
            # Yaprak
            pygame.draw.ellipse(surface, (0, 255, 0), 
                              (boyut + 2, boyut//4, boyut//2, boyut//4))
        
        elif self.meyve_turu == "muz":
            # Muz şekli (yarım ay)
            pygame.draw.arc(surface, (255, 255, 0), 
                          (0, 0, boyut*2, boyut*2), 0, 3.14, max(2, boyut//3))
        
        elif self.meyve_turu == "üzüm":
            # Üzüm taneleri
            for i in range(3):
                for j in range(2):
                    pygame.draw.circle(surface, (128, 0, 128),
                                    (boyut//2 + i*boyut//2,
                                     boyut//2 + j*boyut//2),
                                    boyut//4)
        
        elif self.meyve_turu == "portakal":
            # Portakal
            pygame.draw.circle(surface, (255, 165, 0), (boyut, boyut), boyut)
            # Doku çizgileri
            pygame.draw.arc(surface, (255, 140, 0), 
                          (boyut//2, boyut//2, boyut, boyut), 0, 3.14, 1)
        
        elif self.meyve_turu == "kivi":
            # Kivi dış kabuk
            pygame.draw.circle(surface, (154, 205, 50), (boyut, boyut), boyut)
            # İç doku
            for _ in range(5):
                x = random.randint(boyut//2, boyut*3//2)
                y = random.randint(boyut//2, boyut*3//2)
                pygame.draw.circle(surface, (0, 0, 0), (x, y), 1)
    
    def ciz(self, ekran):
        # Saydamlık için alpha değeri
        alpha = int((self.yasam / PARCACIK_YASAM_SURESI) * 255)
        
        # Meyve surface'i oluştur
        surface = pygame.Surface((self.boyut * 2, self.boyut * 2), pygame.SRCALPHA)
        
        # Meyveyi çiz
        self.meyve_ciz(surface, MEYVELER[self.meyve_turu], self.boyut)
        
        # Alpha değerini uygula
        surface.set_alpha(alpha)
        
        # Ekrana çiz
        ekran.blit(surface, (self.x - self.boyut, self.y - self.boyut))

class HareketParcacik:
    def __init__(self, x, y, renk):
        self.x = x
        self.y = y
        self.renk = renk
        self.yasam = 15  # Daha kısa ömürlü
        self.boyut = random.randint(2, 4)  # Daha küçük parçacıklar
        self.alpha = 255  # Başlangıç saydamlığı
    
    def guncelle(self):
        self.yasam -= 1
        self.alpha = int((self.yasam / 15) * 255)  # Zamanla solarlar
    
    def ciz(self, ekran):
        if self.alpha > 0:
            surface = pygame.Surface((self.boyut * 2, self.boyut * 2), pygame.SRCALPHA)
            pygame.draw.circle(surface, (*self.renk, self.alpha), 
                             (self.boyut, self.boyut), self.boyut)
            ekran.blit(surface, (int(self.x - self.boyut), int(self.y - self.boyut)))

class Oyun:
    def __init__(self):
        self.tam_ekran = False
        self.pencere_boyut = (GENISLIK, YUKSEKLIK)
        self.ekran_genislik = GENISLIK
        self.ekran_yukseklik = YUKSEKLIK
        self.olcek_x = 1
        self.olcek_y = 1
        self.karakter_tipi = "daire"  # varsayılan karakteri daire yaptım
        self.menu_aktif = True
        self.oyun_aktif = False
        self.game_over = False
        self.skor = 0
        self.karakter_boyut = 20
        self.karakter_x = GENISLIK // 2
        self.karakter_y = YUKSEKLIK // 2
        self.karakter_hiz = 5
        
        # İkinci oyuncu özellikleri
        self.karakter2_tipi = "daire"  # İkinci oyuncu için de varsayılan daire
        self.karakter2_x = GENISLIK // 4
        self.karakter2_y = YUKSEKLIK // 2
        self.karakter2_boyut = 20
        self.karakter2_hiz = 5
        self.skor2 = 0
        self.seviye2 = 1
        
        self.hareket_parcaciklari = []  # Hareket parçacıkları listesi
        self.son_parcacik_zamani = 0  # Son parçacık oluşturma zamanı
        self.parcacik_rengi = BEYAZ  # Varsayılan parçacık rengi
        self.parcacik2_rengi = BEYAZ  # İkinci oyuncu için varsayılan parçacık rengi
        
        # Seviye özellikleri
        self.seviye = 1
        self.engel_hizi = 2
        self.hareketli_engeller = False
        
        # Nesneler ve engeller
        self.nesneler = []
        self.engeller = []
        self.engel_yonleri = []  # Buraya taşıdık
        
        # Başlangıç nesnelerini oluştur
        self.nesne_olustur()
        self.engel_olustur()
        
        # Mevcut özelliklere ek olarak:
        self.coklu_oyuncu = False
        
        # Mevcut özelliklerin altına ekleyin
        self.parcaciklar = []
        self.toplanan_nesneler = []  # Toplama animasyonu için
        self.karakter_acisi = 0  # Hareket animasyonu için
        self.karakter2_acisi = 0
        
        # Mevcut özelliklerin altına ses özelliklerini ekleyin
        self.ses_acik = True
        self.muzik_acik = True
        
        # Sesleri yükle
        try:
            # Müzik
            mixer.music.load(f"{SES_KLASORU}/muzik.mp3")
            mixer.music.set_volume(MUZIK_SES)
            
            # Ses efektleri
            self.toplama_sesi = mixer.Sound(f"{SES_KLASORU}/toplama.wav")
            self.seviye_sesi = mixer.Sound(f"{SES_KLASORU}/seviye.wav")
            self.game_over_sesi = mixer.Sound(f"{SES_KLASORU}/game_over.wav")
            
            # Ses seviyelerini ayarla
            self.toplama_sesi.set_volume(EFEKT_SES)
            self.seviye_sesi.set_volume(EFEKT_SES)
            self.game_over_sesi.set_volume(EFEKT_SES)
            
        except:
            print("Ses dosyaları yüklenemedi!")
            self.ses_acik = False
            self.muzik_acik = False
        
        # Mevcut özelliklerin altına ekleyin
        self.karakter1_renk = TURKUAZ
        self.karakter2_renk = PEMBE
        self.karakter1_efekt = "normal"
        self.karakter2_efekt = "normal"
        self.renk_secim_aktif = False
        self.efekt_secim_aktif = False
        self.secilen_oyuncu = 1
        self.rainbow_offset = 0  # Gökkuşağı efekti için
        
        # Mevcut özelliklerin altına ekleyin
        self.oyun_modu = "klasik"
        self.mod_secim_aktif = False
        self.kalan_sure = ZAMAN_SINIRI
        self.son_zaman = pygame.time.get_ticks()
        
        # Mevcut özelliklerin altına ekleyin
        self.tnt_font = pygame.font.Font(None, 20)  # TNT yazısı için daha küçük font
        
        # labirent ile ilgili özellikleri silin
        # self.labirent = [] gibi
        
        # Mevcut özelliklerin altına güç-yükseltme özelliklerini ekleyin
        self.gucler = []
        self.aktif_gucler = {}  # oyuncu: {güç_tipi: bitiş_zamanı}
        self.son_guc_zamani = pygame.time.get_ticks()
        self.kalkan_aktif = False
        self.puan_carpani = 1
        self.miknatis_aktif = False
        
        # Ses efektlerine yeni ses ekleyin
        try:
            # Mevcut ses yüklemelerinin altına
            self.guc_sesi = mixer.Sound(f"{SES_KLASORU}/powerup.wav")
            self.guc_sesi.set_volume(EFEKT_SES)
        except:
            print("Güç sesi yüklenemedi!")
        
        # Mevcut özelliklerin altına can sistemi ekleyin
        self.can = BASLANGIC_CAN
        self.can2 = BASLANGIC_CAN  # İkinci oyuncu için
        self.son_can_puani = 0  # Son can kazanılan puan
        self.son_can_puani2 = 0
        
        # Ses efektlerine yeni ses ekleyin
        try:
            self.can_kaybi_sesi = mixer.Sound(f"{SES_KLASORU}/hit.wav")
            self.can_kazanma_sesi = mixer.Sound(f"{SES_KLASORU}/heal.wav")
            self.can_kaybi_sesi.set_volume(EFEKT_SES)
            self.can_kazanma_sesi.set_volume(EFEKT_SES)
        except:
            print("Can sesleri yüklenemedi!")
        
        # Mevcut özelliklerin altına ekleyin
        try:
            # Arka plan resmini yükle
            self.arka_plan = pygame.image.load(join(RESIM_KLASORU, "arkaplan.jpg"))
            # Ekran boyutuna ölçeklendir
            self.arka_plan = pygame.transform.scale(self.arka_plan, (GENISLIK, YUKSEKLIK))
        except:
            print("Arka plan resmi yüklenemedi!")
            self.arka_plan = None
        
        # Mevcut özelliklerin altına ekle
        self.arena_sure = None
        self.kacis_zamani = None
        self.kacis_engel_suresi = None
        self.boss_aktif = None
        self.boss_x = None
        self.boss_y = None
        self.boss_hiz = None
        self.hizlanma_faktoru = None
        self.son_hizlanma = None
        self.hizlanma_suresi = None
        
        # Hızlanma modu için yeni özellikler ekle
        self.hizlanma_faktoru = 1.0
        self.son_hizlanma = 0
        self.hizlanma_suresi = 5000  # Her 5 saniyede bir hızlan
        
        # Mevcut özelliklere ekle
        self.yuksek_skor = self.yuksek_skoru_yukle()
        
        # Mevcut özelliklere ekle
        self.combo = 0
        self.son_toplama = 0
        self.max_combo = 0
        self.ozel_guc_hazir = True
        self.ozel_guc_zamani = 0
        self.bonus_secim_aktif = False
        self.gorevler = GUNLUK_GOREVLER.copy()
        self.secili_kostum = "normal"
        self.kazanilan_rozetler = set()
    
    def yuksek_skoru_yukle(self):
        try:
            with open("yuksek_skor.txt", "r") as dosya:
                return int(dosya.read())
        except:
            return 0
    
    def yuksek_skoru_kaydet(self):
        if self.skor > self.yuksek_skor:
            self.yuksek_skor = self.skor
            with open("yuksek_skor.txt", "w") as dosya:
                dosya.write(str(self.yuksek_skor))
    
    def arka_plan_ciz(self, hedef_yuzey):
        if self.arka_plan:
            hedef_yuzey.blit(self.arka_plan, (0, 0))
        else:
            hedef_yuzey.fill(SIYAH)
    
    def nesne_olustur(self):
        for _ in range(5):
            x = random.randint(0, GENISLIK - 20)
            y = random.randint(0, YUKSEKLIK - 20)
            self.nesneler.append(pygame.Rect(x, y, 20, 20))
            
    def engel_olustur(self, sayi=None):
        self.engeller.clear()
        self.engel_yonleri.clear()
        
        if sayi is None:
            engel_sayisi = 2 + self.seviye
        else:
            engel_sayisi = sayi
        
        for _ in range(engel_sayisi):
            x = random.randint(0, GENISLIK - 30)
            y = random.randint(0, YUKSEKLIK - 30)
            self.engeller.append(pygame.Rect(x, y, 30, 30))
            self.engel_yonleri.append([random.choice([-1, 1]), random.choice([-1, 1])])
    
    def engelleri_hareket_ettir(self):
        if self.hareketli_engeller:
            for i, engel in enumerate(self.engeller):
                # Engeli hareket ettir
                engel.x += self.engel_yonleri[i][0] * self.engel_hizi
                engel.y += self.engel_yonleri[i][1] * self.engel_hizi
                
                # Duvarlardan sekme
                if engel.left <= 0 or engel.right >= GENISLIK:
                    self.engel_yonleri[i][0] *= -1
                if engel.top <= 0 or engel.bottom >= YUKSEKLIK:
                    self.engel_yonleri[i][1] *= -1
    
    def seviye_guncelle(self):
        if self.oyun_modu == "klasik":
            # Klasik modda ortak seviye
            eski_seviye = self.seviye
            toplam_skor = self.skor  # İki oyuncunun puanı zaten birleşik
            
            for seviye, gerekli_puan in SEVIYE_PUAN_GEREKSINIMLERI.items():
                if toplam_skor >= gerekli_puan:
                    self.seviye = seviye
                    self.seviye2 = seviye  # İkinci oyuncunun seviyesi de aynı
            
            if self.seviye > eski_seviye:
                self.seviye_yukselt(1)  # Her iki oyuncu için seviye yükseltme
        else:
            # Diğer modlarda ayrı seviyeler
            # Birinci oyuncu için seviye kontrolü
            eski_seviye = self.seviye
            for seviye, gerekli_puan in SEVIYE_PUAN_GEREKSINIMLERI.items():
                if self.skor >= gerekli_puan:
                    self.seviye = seviye
            
            if self.seviye > eski_seviye:
                self.seviye_yukselt(1)
            
            # İkinci oyuncu için seviye kontrolü
            if self.coklu_oyuncu:
                eski_seviye2 = self.seviye2
                for seviye, gerekli_puan in SEVIYE_PUAN_GEREKSINIMLERI.items():
                    if self.skor2 >= gerekli_puan:
                        self.seviye2 = seviye
                
                if self.seviye2 > eski_seviye2:
                    self.seviye_yukselt(2)
    
    def seviye_yukselt(self, oyuncu_no):
        # Ses efekti
        self.ses_cal(self.seviye_sesi)
        
        if oyuncu_no == 1:
            # Birinci oyuncu için yükseltmeler
            self.karakter_boyut = min(40, self.karakter_boyut + 5)
            if self.seviye >= 4:
                self.karakter_hiz += 1
        else:
            # İkinci oyuncu için yükseltmeler
            self.karakter2_boyut = min(40, self.karakter2_boyut + 5)
            if self.seviye2 >= 4:
                self.karakter2_hiz += 1
        
        # Ortak yükseltmeler
        self.engel_hizi += 1
        if max(self.seviye, getattr(self, 'seviye2', 1)) >= 2:
            self.hareketli_engeller = True
        if max(self.seviye, getattr(self, 'seviye2', 1)) >= 3:
            self.engel_olustur()
    
    def menu_ciz(self, ekran):
        ekran.fill(SIYAH)
        
        # Başlık
        baslik = font.render("ToplareSa", True, TURKUAZ)
        ekran.blit(baslik, (GENISLIK//2 - 50, 50))
        
        # Menü seçenekleri
        y = 150
        secenekler = [
            ("1: Tek Oyunculu", TURKUAZ),
            ("2: Çok Oyunculu", PEMBE),
            ("K: Kare Karakter", BEYAZ),
            ("D: Daire Karakter", BEYAZ),
            ("U: Üçgen Karakter", BEYAZ),
            ("R: Renk Seçimi", BEYAZ),
            ("E: İz Rengi Seçimi", BEYAZ),
            ("O: Oyun Modu", BEYAZ),
            ("S: Ses Açık/Kapalı", BEYAZ if self.ses_acik else KIRMIZI),
            ("M: Müzik Açık/Kapalı", BEYAZ if self.muzik_acik else KIRMIZI),
            ("F11: Tam Ekran", BEYAZ),
            ("ESC: Çıkış", KIRMIZI)
        ]
        
        for secenek, renk in secenekler:
            text = font.render(secenek, True, renk)
            ekran.blit(text, (GENISLIK//2 - 80, y))
            y += 35
    
    def mod_menu_ciz(self, ekran):
        ekran.fill(SIYAH)
        baslik = font.render("Oyun Modu Seçin", True, TURKUAZ)
        ekran.blit(baslik, (GENISLIK//2 - 80, 30))
        
        y = 80
        for i, (mod_adi, _) in enumerate(OYUN_MODLARI.items()):
            mod_text = font.render(f"{i+1}: {mod_adi}", True, TURKUAZ)
            ekran.blit(mod_text, (GENISLIK//2 - 60, y))
            y += 40
        
        geri_text = font.render("ESC: Geri Dön", True, ACIK_TURKUAZ)
        ekran.blit(geri_text, (GENISLIK//2 - 60, y + 20))
    
    def parcacik_efekti_olustur(self, x, y, renk, miktar=8):
        for _ in range(miktar):
            self.parcaciklar.append(Parcacik(x, y, renk))
    
    def toplama_animasyonu_baslat(self, nesne, oyuncu_no):
        self.toplanan_nesneler.append({
            'rect': nesne,
            'sure': TOPLAMA_ANIMASYON_SURESI,
            'baslangic_boyut': nesne.width,
            'oyuncu': oyuncu_no
        })
    
    def animasyonlari_guncelle(self):
        # Parçacıkları güncelle
        for parcacik in self.parcaciklar[:]:
            parcacik.guncelle()
            if parcacik.yasam <= 0:
                self.parcaciklar.remove(parcacik)
        
        # Toplanan nesneleri güncelle
        for nesne in self.toplanan_nesneler[:]:
            nesne['sure'] -= 1
            if nesne['sure'] <= 0:
                self.toplanan_nesneler.remove(nesne)
        
        # Karakter animasyonlarını güncelle
        self.karakter_acisi += 0.1
        self.karakter2_acisi += 0.1
    
    def karakter_ciz(self, ekran):
        renk = self.efekt_uygula(self.karakter1_renk, self.karakter1_efekt)
        # Mevcut karakter_ciz kodunda TURKUAZ yerine renk kullanın
        offset_y = math.sin(self.karakter_acisi) * 3
        
        if self.karakter_tipi == "kare":
            pygame.draw.rect(ekran, renk, (self.karakter_x, 
                                         self.karakter_y + offset_y, 
                                         self.karakter_boyut, 
                                         self.karakter_boyut))
        elif self.karakter_tipi == "daire":
            pygame.draw.circle(ekran, renk, 
                            (self.karakter_x + self.karakter_boyut//2, 
                             self.karakter_y + self.karakter_boyut//2 + offset_y), 
                             self.karakter_boyut//2)
        elif self.karakter_tipi == "ucgen":
            points = [(self.karakter_x + self.karakter_boyut//2, self.karakter_y + offset_y),
                     (self.karakter_x, self.karakter_y + self.karakter_boyut + offset_y),
                     (self.karakter_x + self.karakter_boyut, self.karakter_y + self.karakter_boyut + offset_y)]
            pygame.draw.polygon(ekran, renk, points)
    
    def karakter2_ciz(self, ekran):
        renk = self.efekt_uygula(self.karakter2_renk, self.karakter2_efekt)
        # Mevcut karakter2_ciz kodunda PEMBE yerine renk kullanın
        # ... benzer şekilde
        offset_y = math.sin(self.karakter2_acisi) * 3
        
        if self.karakter2_tipi == "kare":
            pygame.draw.rect(ekran, renk, (self.karakter2_x, 
                                          self.karakter2_y + offset_y, 
                                          self.karakter2_boyut, 
                                          self.karakter2_boyut))
        elif self.karakter2_tipi == "daire":
            pygame.draw.circle(ekran, renk, 
                            (self.karakter2_x + self.karakter2_boyut//2, 
                             self.karakter2_y + self.karakter2_boyut//2 + offset_y), 
                             self.karakter2_boyut//2)
        elif self.karakter2_tipi == "ucgen":
            points = [(self.karakter2_x + self.karakter2_boyut//2, self.karakter2_y + offset_y),
                     (self.karakter2_x, self.karakter2_y + self.karakter2_boyut + offset_y),
                     (self.karakter2_x + self.karakter2_boyut, self.karakter2_y + self.karakter2_boyut + offset_y)]
            pygame.draw.polygon(ekran, renk, points)
    
    def game_over_ekrani(self):
        ekran.fill(SIYAH)
        game_over_text = font.render("OYUN BİTTİ!", True, KIRMIZI)
        
        if self.oyun_modu == "arena":
            if self.skor > self.skor2:
                kazanan_text = font.render("Oyuncu 1 Kazandı!", True, TURKUAZ)
            elif self.skor2 > self.skor:
                kazanan_text = font.render("Oyuncu 2 Kazandı!", True, PEMBE)
            else:
                kazanan_text = font.render("Berabere!", True, BEYAZ)
            ekran.blit(kazanan_text, (GENISLIK//2 - 80, YUKSEKLIK//2 - 90))
        elif self.oyun_modu == "kacis":
            hayatta_kalma_text = font.render(f"Toplam Engel: {len(self.engeller)}", True, KIRMIZI)
            ekran.blit(hayatta_kalma_text, (GENISLIK//2 - 80, YUKSEKLIK//2 - 90))
        
        skor_text = font.render(f"Skor: {self.skor}", True, TURKUAZ)
        if self.coklu_oyuncu:
            skor2_text = font.render(f"Skor 2: {self.skor2}", True, PEMBE)
        tekrar_text = font.render("Tekrar oynamak için SPACE'e basın", True, BEYAZ)
        menu_text = font.render("Ana menüye dönmek için ESC'ye basın", True, BEYAZ)
        
        ekran.blit(game_over_text, (GENISLIK//2 - 100, YUKSEKLIK//2 - 60))
        ekran.blit(skor_text, (GENISLIK//2 - 50, YUKSEKLIK//2 - 20))
        if self.coklu_oyuncu:
            ekran.blit(skor2_text, (GENISLIK//2 - 50, YUKSEKLIK//2 + 10))
        ekran.blit(tekrar_text, (GENISLIK//2 - 150, YUKSEKLIK//2 + 40))
        ekran.blit(menu_text, (GENISLIK//2 - 150, YUKSEKLIK//2 + 70))
    
    def seviye_bilgisi_ciz(self, ekran):
        if self.oyun_modu == "klasik" and self.coklu_oyuncu:
            # Klasik modda ortak seviye bilgisi
            seviye_text = font.render(f"Ortak Seviye: {self.seviye}", True, TURKUAZ)
            skor_text = font.render(f"Ortak Skor: {self.skor}", True, TURKUAZ)
            ekran.blit(seviye_text, (10, 10))
            ekran.blit(skor_text, (10, 35))
            
            sonraki_seviye = self.seviye + 1
            if sonraki_seviye in SEVIYE_PUAN_GEREKSINIMLERI:
                kalan_puan = SEVIYE_PUAN_GEREKSINIMLERI[sonraki_seviye] - self.skor
                ilerleme_text = font.render(f"Sonraki seviye için: {kalan_puan}", True, TURKUAZ)
                ekran.blit(ilerleme_text, (10, 60))
        else:
            # Diğer modlarda ayrı seviye bilgileri
            # Birinci oyuncu seviye bilgisi
            seviye_text = font.render(f"Seviye 1: {self.seviye}", True, TURKUAZ)
            sonraki_seviye = self.seviye + 1
            if sonraki_seviye in SEVIYE_PUAN_GEREKSINIMLERI:
                kalan_puan = SEVIYE_PUAN_GEREKSINIMLERI[sonraki_seviye] - self.skor
                ilerleme_text = font.render(f"Sonraki seviye için: {kalan_puan}", True, TURKUAZ)
                ekran.blit(ilerleme_text, (10, 35))
            ekran.blit(seviye_text, (10, 10))
            
            # İkinci oyuncu seviye bilgisi
            if self.coklu_oyuncu:
                seviye2_text = font.render(f"Seviye 2: {self.seviye2}", True, PEMBE)
                sonraki_seviye2 = self.seviye2 + 1
                if sonraki_seviye2 in SEVIYE_PUAN_GEREKSINIMLERI:
                    kalan_puan2 = SEVIYE_PUAN_GEREKSINIMLERI[sonraki_seviye2] - self.skor2
                    ilerleme2_text = font.render(f"Sonraki seviye için: {kalan_puan2}", True, PEMBE)
                    ekran.blit(ilerleme2_text, (10, 75))
                ekran.blit(seviye2_text, (10, 50))
    
    def muzik_baslat(self):
        if self.muzik_acik:
            mixer.music.play(-1)  # -1 sonsuz döngü
    
    def muzik_durdur(self):
        mixer.music.stop()
    
    def ses_cal(self, ses):
        if self.ses_acik and ses:
            try:
                ses.play()
            except:
                print("Ses çalınamadı!")
    
    def efekt_uygula(self, renk, efekt_tipi):
        if efekt_tipi == "normal":
            return renk
        elif efekt_tipi == "parlak":
            # Rengi parlat
            r = min(255, renk[0] + 50)
            g = min(255, renk[1] + 50)
            b = min(255, renk[2] + 50)
            return (r, g, b)
        elif efekt_tipi == "rainbow":
            # Gökkuşağı efekti
            hue = (self.rainbow_offset / 100.0) % 1.0
            rgb = pygame.Color(0)
            rgb.hsva = (hue * 360, 100, 100, 100)
            return rgb
        elif efekt_tipi == "titresim":
            # Titreşim efekti
            offset = random.randint(-20, 20)
            r = max(0, min(255, renk[0] + offset))
            g = max(0, min(255, renk[1] + offset))
            b = max(0, min(255, renk[2] + offset))
            return (r, g, b)
    
    def renk_menu_ciz(self, ekran):
        ekran.fill(SIYAH)
        baslik = font.render(f"Oyuncu {self.secilen_oyuncu} Renk Seçimi", True, TURKUAZ)
        ekran.blit(baslik, (GENISLIK//2 - 80, 30))
        
        y = 80
        for i, (renk_adi, renk) in enumerate(RENK_SECENEKLERI.items()):
            renk_text = font.render(f"{i+1}: {renk_adi}", True, renk)
            ekran.blit(renk_text, (GENISLIK//2 - 60, y))
            y += 40
        
        geri_text = font.render("ESC: Geri Dön", True, ACIK_TURKUAZ)
        ekran.blit(geri_text, (GENISLIK//2 - 60, y + 20))
    
    def efekt_menu_ciz(self, ekran):
        ekran.fill(SIYAH)
        baslik = font.render(f"Oyuncu {self.secilen_oyuncu} İz Rengi Seçimi", True, TURKUAZ)
        ekran.blit(baslik, (GENISLIK//2 - 80, 30))
        
        y = 80
        for i, (efekt_adi, renk) in enumerate(EFEKT_SECENEKLERI.items()):
            efekt_text = font.render(f"{i+1}: {efekt_adi}", True, renk)
            ekran.blit(efekt_text, (GENISLIK//2 - 60, y))
            y += 40
        
        geri_text = font.render("ESC: Geri Dön", True, ACIK_TURKUAZ)
        ekran.blit(geri_text, (GENISLIK//2 - 60, y + 20))
    
    def ekran_modu_degistir(self):
        global ekran  # ekran değişkenini global olarak kullan
        if self.tam_ekran:
            # Pencere moduna geç
            ekran = pygame.display.set_mode(self.pencere_boyut)
            self.tam_ekran = False
            self.ekran_genislik = GENISLIK
            self.ekran_yukseklik = YUKSEKLIK
            self.olcek_x = 1
            self.olcek_y = 1
        else:
            # Tam ekran moduna geç
            ekran_bilgisi = pygame.display.Info()
            self.ekran_genislik = ekran_bilgisi.current_w
            self.ekran_yukseklik = ekran_bilgisi.current_h
            ekran = pygame.display.set_mode((self.ekran_genislik, self.ekran_yukseklik), 
                                         pygame.FULLSCREEN)
            self.tam_ekran = True
            
            # Ölçeklendirme faktörlerini hesapla
            self.olcek_x = self.ekran_genislik / GENISLIK
            self.olcek_y = self.ekran_yukseklik / YUKSEKLIK
    
    def koordinat_donustur(self, x, y):
        # Koordinatları ekran boyutuna göre ölçeklendir
        return (int(x * self.olcek_x), int(y * self.olcek_y))
    
    def boyut_donustur(self, boyut):
        # Boyutu ekran boyutuna göre ölçeklendir
        return int(boyut * min(self.olcek_x, self.olcek_y))
    
    def oyunu_baslat(self):
        # Mevcut karakter tipini ve ayarları sakla
        mevcut_karakter_tipi = self.karakter_tipi
        mevcut_karakter2_tipi = self.karakter2_tipi
        mevcut_renk = self.karakter1_renk
        mevcut_efekt = self.karakter1_efekt
        
        # Mevcut özellikleri sıfırla
        self.skor = 0
        self.skor2 = 0
        self.seviye = 1
        self.can = BASLANGIC_CAN
        self.can2 = BASLANGIC_CAN
        
        # Saklanan karakter tipini ve ayarları geri yükle
        self.karakter_tipi = mevcut_karakter_tipi
        self.karakter2_tipi = mevcut_karakter2_tipi
        self.karakter1_renk = mevcut_renk
        self.karakter1_efekt = mevcut_efekt
        
        # Normal başlangıç konumları
        self.karakter_x = GENISLIK // 2
        self.karakter_y = YUKSEKLIK // 2
        self.karakter2_x = GENISLIK // 4
        self.karakter2_y = YUKSEKLIK // 2
        
        # Diğer başlangıç ayarları
        self.nesneler.clear()
        self.engeller.clear()
        self.parcaciklar.clear()
        self.gucler.clear()
        
        # Mod spesifik ayarlar
        if self.oyun_modu == "survival":
            self.can = BASLANGIC_CAN
            self.can2 = BASLANGIC_CAN
        elif self.oyun_modu == "zaman":
            self.kalan_sure = ZAMAN_SINIRI
        
        # Başlangıç nesnelerini oluştur
        self.nesne_olustur()
        self.engel_olustur()
    
    def hizlanma_modu_guncelle(self):
        simdiki_zaman = pygame.time.get_ticks()
        if simdiki_zaman - self.son_hizlanma >= self.hizlanma_suresi:
            self.son_hizlanma = simdiki_zaman
            self.hizlanma_faktoru += 0.2
            # Hızları güncelle
            self.karakter_hiz = 5 * self.hizlanma_faktoru
            self.karakter2_hiz = 5 * self.hizlanma_faktoru
            self.engel_hizi = 2 * self.hizlanma_faktoru
    
    def zaman_guncelle(self):
        if self.oyun_modu == "zaman":
            simdiki_zaman = pygame.time.get_ticks()
            gecen_sure = (simdiki_zaman - self.son_zaman) / 1000  # saniyeye çevir
            self.kalan_sure -= gecen_sure
            self.son_zaman = simdiki_zaman
            
            if self.kalan_sure <= 0:
                self.oyun_aktif = False
                self.game_over = True
    
    def tnt_ciz(self, ekran, x, y):
        # TNT kutusunu çiz
        pygame.draw.rect(ekran, TNT_RENK, (x, y, TNT_BOYUT, TNT_BOYUT))
        
        # TNT yazısını çiz
        tnt_text = font.render("TNT", True, TNT_YAZI_RENK)
        text_rect = tnt_text.get_rect(center=(x + TNT_BOYUT//2, y + TNT_BOYUT//2))
        ekran.blit(tnt_text, text_rect)
    
    def guc_olustur(self):
        simdiki_zaman = pygame.time.get_ticks()
        if simdiki_zaman - self.son_guc_zamani >= GUC_OLUSTURMA_SURESI:
            self.son_guc_zamani = simdiki_zaman
            
            # Rastgele güç tipi seç
            guc_tipi = random.choice(list(GUC_TIPLERI.keys()))
            
            # Rastgele konum belirle
            x = random.randint(0, GENISLIK - GUC_BOYUT)
            y = random.randint(0, YUKSEKLIK - GUC_BOYUT)
            
            self.gucler.append({
                "tip": guc_tipi,
                "rect": pygame.Rect(x, y, GUC_BOYUT, GUC_BOYUT)
            })
            
            # Güç oluşturma sesi
            self.ses_cal(self.guc_sesi)
    
    def guc_uygula(self, guc_tipi, oyuncu_no):
        simdiki_zaman = pygame.time.get_ticks()
        sure = GUC_TIPLERI[guc_tipi]["sure"] * 1000  # milisaniyeye çevir
        
        if oyuncu_no not in self.aktif_gucler:
            self.aktif_gucler[oyuncu_no] = {}
        
        self.aktif_gucler[oyuncu_no][guc_tipi] = simdiki_zaman + sure
        
        # Güç efektlerini uygula
        if guc_tipi == "hiz":
            if oyuncu_no == 1:
                self.karakter_hiz *= 2
            else:
                self.karakter2_hiz *= 2
        elif guc_tipi == "kalkan":
            self.kalkan_aktif = True
        elif guc_tipi == "puan2x":
            self.puan_carpani = 2
        elif guc_tipi == "kucult":
            if oyuncu_no == 1:
                self.karakter_boyut = max(10, self.karakter_boyut - 10)
            else:
                self.karakter2_boyut = max(10, self.karakter2_boyut - 10)
        elif guc_tipi == "miknatis":
            self.miknatis_aktif = True
    
    def gucleri_guncelle(self):
        simdiki_zaman = pygame.time.get_ticks()
        
        # Güç oluşturma kontrolü
        if simdiki_zaman - self.son_guc_zamani >= GUC_OLUSTURMA_SURESI:
            self.guc_olustur()
            self.son_guc_zamani = simdiki_zaman
        
        # Aktif güçleri güncelle
        for oyuncu_no in list(self.aktif_gucler.keys()):
            for guc_tipi in list(self.aktif_gucler[oyuncu_no].keys()):
                if simdiki_zaman >= self.aktif_gucler[oyuncu_no][guc_tipi]:
                    self.guc_etkisini_kaldir(oyuncu_no, guc_tipi)
    
    def guc_etkisini_kaldir(self, oyuncu_no, guc_tipi):
        if guc_tipi == "hiz":
            if oyuncu_no == 1:
                self.karakter_hiz = 5
            else:
                self.karakter2_hiz = 5
        elif guc_tipi == "kalkan":
            self.kalkan_aktif = False
        elif guc_tipi == "puan2x":
            self.puan_carpani = 1
        elif guc_tipi == "kucult":
            if oyuncu_no == 1:
                self.karakter_boyut = 20
            else:
                self.karakter2_boyut = 20
        elif guc_tipi == "miknatis":
            self.miknatis_aktif = False
        
        del self.aktif_gucler[oyuncu_no][guc_tipi]
    
    def guc_ciz(self, guc):
        # Güç kutusunu çiz
        pygame.draw.rect(ekran, GUC_TIPLERI[guc["tip"]]["renk"], guc["rect"])
        
        # Güç sembolünü çiz
        sembol = self.tnt_font.render(GUC_TIPLERI[guc["tip"]]["sembol"], True, BEYAZ)
        sembol_rect = sembol.get_rect(center=guc["rect"].center)
        ekran.blit(sembol, sembol_rect)
    
    def can_guncelle(self):
        # Can kazanma kontrolü (her 10 puanda bir)
        if self.skor - self.son_can_puani >= CAN_YENILEME_PUANI:
            self.can += 1
            self.son_can_puani = self.skor
            self.ses_cal(self.can_kazanma_sesi)
        
        if self.coklu_oyuncu and self.skor2 - self.son_can_puani2 >= CAN_YENILEME_PUANI:
            self.can2 += 1
            self.son_can_puani2 = self.skor2
            self.ses_cal(self.can_kazanma_sesi)
    
    def can_ciz(self):
        # Canları kalp simgesi olarak çiz
        for i in range(self.can):
            # Kalp şekli
            x = 20 + i * 30
            y = 20
            pygame.draw.polygon(ekran, KIRMIZI, [
                (x, y+5),
                (x-7, y-2),
                (x-14, y+5),
                (x-7, y+12),
                (x, y+5)
            ])
            pygame.draw.polygon(ekran, KIRMIZI, [
                (x, y+5),
                (x+7, y-2),
                (x+14, y+5),
                (x+7, y+12),
                (x, y+5)
            ])
        
        # İkinci oyuncu canları
        if self.coklu_oyuncu:
            for i in range(self.can2):
                x = 20 + i * 30
                y = 50
                pygame.draw.polygon(ekran, PEMBE, [
                    (x, y+5),
                    (x-7, y-2),
                    (x-14, y+5),
                    (x-7, y+12),
                    (x, y+5)
                ])
                pygame.draw.polygon(ekran, PEMBE, [
                    (x, y+5),
                    (x+7, y-2),
                    (x+14, y+5),
                    (x+7, y+12),
                    (x, y+5)
                ])
    
    def skor_ekle(self, oyuncu_no, miktar=1):
        # Puan çarpanını uygula
        miktar *= self.puan_carpani
        
        # Klasik modda puanlar ortak
        if self.oyun_modu == "klasik":
            self.skor += miktar  # Her iki oyuncunun puanı ortak skora eklenir
            if self.skor - self.son_can_puani >= CAN_YENILEME_PUANI:
                self.can += 1
                self.can2 += 1  # İkinci oyuncunun canı da artar
                self.son_can_puani = self.skor
                self.ses_cal(self.can_kazanma_sesi)
        else:
            # Diğer modlarda ayrı puanlar
            if oyuncu_no == 1:
                self.skor += miktar
                if self.skor - self.son_can_puani >= CAN_YENILEME_PUANI:
                    self.can += 1
                    self.son_can_puani = self.skor
                    self.ses_cal(self.can_kazanma_sesi)
            else:
                self.skor2 += miktar
                if self.skor2 - self.son_can_puani2 >= CAN_YENILEME_PUANI:
                    self.can2 += 1
                    self.son_can_puani2 = self.skor2
                    self.ses_cal(self.can_kazanma_sesi)
    
    def kar_efekti(self):
        # Yeni kar taneleri ekle
        if len(self.kar_taneleri) < 100:
            self.kar_taneleri.append([
                random.randint(0, GENISLIK),
                0,
                random.randint(2, 4)  # Kar tanesi boyutu
            ])
        
        # Kar tanelerini güncelle ve çiz
        for kar in self.kar_taneleri[:]:
            pygame.draw.circle(ekran, BEYAZ, 
                             (int(kar[0]), int(kar[1])), 
                             kar[2])
            kar[0] += math.sin(kar[1] / 30) * 2  # Yanlara sallanma
            kar[1] += kar[2] / 2  # Büyük taneler daha hızlı düşer
            
            if kar[1] > YUKSEKLIK:
                self.kar_taneleri.remove(kar)
    
    def basarim_kontrol(self):
        if self.skor >= 1 and not BASARIMLAR["baslangic"]["tamamlandi"]:
            BASARIMLAR["baslangic"]["tamamlandi"] = True
            self.basarim_goster("Başlangıç")
    
    def parilti_efekti(self, x, y, renk):
        for i in range(10):
            boyut = i * 2
            alpha = 255 - (i * 25)
            surface = pygame.Surface((boyut*2, boyut*2), pygame.SRCALPHA)
            pygame.draw.circle(surface, (*renk, alpha), (boyut, boyut), boyut)
            ekran.blit(surface, (x-boyut, y-boyut))
    
    def ipucu_goster(self):
        ipucu = random.choice(IPUCLARI)
        ipucu_text = font.render(ipucu, True, BEYAZ)
        ekran.blit(ipucu_text, (10, YUKSEKLIK - 30))
    
    def ses_efekti_cal(self, efekt_tipi):
        if self.ses_acik:
            ses_efektleri = {
                "toplama": self.toplama_sesi,
                "seviye": self.seviye_sesi,
                "hasar": self.can_kaybi_sesi,
                "guc": self.guc_sesi
            }
            if efekt_tipi in ses_efektleri:
                ses_efektleri[efekt_tipi].play()
    
    def basarim_goster(self, basarim_adi):
        basarim_text = font.render(f"Başarım Kazanıldı: {basarim_adi}!", True, SARI)
        ekran.blit(basarim_text, (GENISLIK//2 - 100, 10))
    
    def combo_guncelle(self):
        simdiki_zaman = pygame.time.get_ticks()
        if simdiki_zaman - self.son_toplama > COMBO_SURESI:
            self.combo = 0
        
        # Combo'yu göster
        if self.combo > 1:
            combo_text = font.render(f"Combo x{self.combo}!", True, SARI)
            ekran.blit(combo_text, (GENISLIK//2 - 50, 10))
            
            # Max combo kontrolü
            if self.combo > self.max_combo:
                self.max_combo = self.combo
    
    def ozel_guc_kullan(self, guc_tipi):
        if self.ozel_guc_hazir:
            if guc_tipi == "super_hiz":
                self.karakter_hiz *= 3
            elif guc_tipi == "zaman_yavas":
                self.engel_hizi *= 0.5
            
            self.ozel_guc_hazir = False
            self.ozel_guc_zamani = pygame.time.get_ticks()
            
            # Özel güç efekti
            self.parilti_efekti(self.karakter_x + self.karakter_boyut//2,
                              self.karakter_y + self.karakter_boyut//2,
                              SARI)
    
    def seviye_sonu_bonus(self):
        if self.bonus_secim_aktif:
            bonus_text = font.render("Bonus Seç!", True, SARI)
            ekran.blit(bonus_text, (GENISLIK//2 - 40, YUKSEKLIK//2))
            
            y = YUKSEKLIK//2 + 40
            for i, (bonus_id, bonus_ad) in enumerate(SEVIYE_BONUSLARI.items()):
                bonus_text = font.render(f"{i+1}: {bonus_ad}", True, BEYAZ)
                ekran.blit(bonus_text, (GENISLIK//2 - 60, y))
                y += 30
    
    def bonus_uygula(self, bonus_id):
        if bonus_id == "can":
            self.can += 1
        elif bonus_id == "hiz":
            self.karakter_hiz += 1
        elif bonus_id == "kucuk":
            self.karakter_boyut = max(10, self.karakter_boyut - 5)
        elif bonus_id == "puan":
            self.puan_carpani += 0.5
    
    def gorev_kontrol(self):
        for gorev_id, gorev in self.gorevler.items():
            if not gorev.get("tamamlandi", False):
                if gorev_id == "hizli" and self.skor >= 5 and self.kalan_sure >= 50:
                    gorev["tamamlandi"] = True
                    self.gorev_tamamlandi(gorev["ad"])
                elif gorev_id == "combo" and self.combo >= 5:
                    gorev["tamamlandi"] = True
                    self.gorev_tamamlandi(gorev["ad"])
    
    def gorev_tamamlandi(self, gorev_adi):
        self.kazanilan_rozetler.add(gorev_adi)
        self.basarim_goster(f"Görev Tamamlandı: {gorev_adi}")
    
    def rozet_ciz(self, x, y, rozet_tipi):
        # Rozet arka planı
        pygame.draw.circle(ekran, SARI, (x, y), 20)
        
        # Rozet simgesi (basit şekiller)
        if rozet_tipi == "hizli":
            pygame.draw.polygon(ekran, SIYAH, [(x-10, y+10), (x, y-10), (x+10, y+10)])
        elif rozet_tipi == "combo":
            pygame.draw.rect(ekran, SIYAH, (x-8, y-8, 16, 16))
        elif rozet_tipi == "engel":
            pygame.draw.circle(ekran, SIYAH, (x, y), 8)
    
    def rozetleri_goster(self):
        x = 50
        y = YUKSEKLIK - 30
        for rozet in self.kazanilan_rozetler:
            self.rozet_ciz(x, y, rozet)
            x += 50
    
    def kostum_uygula(self, kostum_id):
        if kostum_id in KOSTUMLER:
            self.karakter1_renk = KOSTUMLER[kostum_id]["renk"]
            self.karakter1_efekt = KOSTUMLER[kostum_id]["efekt"]

    def hareket_parcacigi_olustur(self, x, y, renk):
        simdiki_zaman = pygame.time.get_ticks()
        if simdiki_zaman - self.son_parcacik_zamani >= 50:  # Her 50ms'de bir parçacık
            self.hareket_parcaciklari.append(HareketParcacik(x, y, renk))
            self.son_parcacik_zamani = simdiki_zaman

    def hareket_parcaciklarini_guncelle(self):
        for parcacik in self.hareket_parcaciklari[:]:
            parcacik.guncelle()
            if parcacik.yasam <= 0:
                self.hareket_parcaciklari.remove(parcacik)

    def hareket_parcaciklarini_ciz(self, ekran):
        for parcacik in self.hareket_parcaciklari:
            parcacik.ciz(ekran)

# Oyun nesnesini oluştur
oyun = Oyun()

# Oyun döngüsü
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                oyun.ekran_modu_degistir()
            if oyun.menu_aktif:
                if event.key == pygame.K_s:
                    oyun.ses_acik = not oyun.ses_acik
                elif event.key == pygame.K_m:
                    oyun.muzik_acik = not oyun.muzik_acik
                    if oyun.muzik_acik:
                        oyun.muzik_baslat()
                    else:
                        oyun.muzik_durdur()
                elif event.key == pygame.K_o:
                    oyun.mod_secim_aktif = True
                    oyun.menu_aktif = False
                elif event.key == pygame.K_1:
                    oyun.coklu_oyuncu = False
                    oyun.menu_aktif = False
                    oyun.oyun_aktif = True
                    oyun.muzik_baslat()  # Oyun başladığında müziği başlat
                elif event.key == pygame.K_2:
                    oyun.coklu_oyuncu = True
                    oyun.menu_aktif = False
                    oyun.oyun_aktif = True
                elif event.key == pygame.K_k:
                    oyun.karakter_tipi = "kare"
                    oyun.karakter2_tipi = "kare"
                elif event.key == pygame.K_d:
                    oyun.karakter_tipi = "daire"
                    oyun.karakter2_tipi = "daire"
                elif event.key == pygame.K_u:
                    oyun.karakter_tipi = "ucgen"
                    oyun.karakter2_tipi = "ucgen"
                elif event.key == pygame.K_RETURN:
                    oyun.menu_aktif = False
                    oyun.oyun_aktif = True
                elif event.key == pygame.K_r:
                    oyun.renk_secim_aktif = True
                    oyun.menu_aktif = False
                elif event.key == pygame.K_e:
                    oyun.efekt_secim_aktif = True
                    oyun.menu_aktif = False
            
            if oyun.game_over:
                if event.key == pygame.K_ESCAPE:
                    # Ana menüye dön
                    oyun = Oyun()
                    oyun.menu_aktif = True
                    oyun.game_over = False
                elif event.key == pygame.K_SPACE:
                    # Oyunu yeniden başlat
                    oyun = Oyun()
                    oyun.menu_aktif = False
                    oyun.oyun_aktif = True
                    oyun.muzik_baslat()
            elif oyun.renk_secim_aktif:
                if event.key == pygame.K_ESCAPE:
                    oyun.renk_secim_aktif = False
                    oyun.menu_aktif = True
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6]:
                    renk_index = event.key - pygame.K_1
                    if renk_index < len(RENK_SECENEKLERI):
                        renk = list(RENK_SECENEKLERI.values())[renk_index]
                        if oyun.secilen_oyuncu == 1:
                            oyun.karakter1_renk = renk
                        else:
                            oyun.karakter2_renk = renk
                elif event.key == pygame.K_TAB:
                    oyun.secilen_oyuncu = 2 if oyun.secilen_oyuncu == 1 else 1
            
            elif oyun.efekt_secim_aktif:
                if event.key == pygame.K_ESCAPE:
                    oyun.efekt_secim_aktif = False
                    oyun.menu_aktif = True
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8]:
                    efekt_index = event.key - pygame.K_1
                    if efekt_index < len(EFEKT_SECENEKLERI):
                        renk = list(EFEKT_SECENEKLERI.values())[efekt_index]
                        if oyun.secilen_oyuncu == 1:
                            oyun.parcacik_rengi = renk
                        else:
                            oyun.parcacik2_rengi = renk
                elif event.key == pygame.K_TAB:
                    oyun.secilen_oyuncu = 2 if oyun.secilen_oyuncu == 1 else 1
            
            elif oyun.mod_secim_aktif:
                if event.key == pygame.K_ESCAPE:
                    oyun.mod_secim_aktif = False
                    oyun.menu_aktif = True
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    mod_index = event.key - pygame.K_1
                    if mod_index < len(OYUN_MODLARI):
                        oyun.oyun_modu = list(OYUN_MODLARI.values())[mod_index]
                        oyun.mod_secim_aktif = False
                        oyun.menu_aktif = True
            
    if oyun.menu_aktif:
        oyun.menu_ciz(ekran)
    elif oyun.mod_secim_aktif:
        oyun.mod_menu_ciz(ekran)
    elif oyun.renk_secim_aktif:
        oyun.renk_menu_ciz(ekran)
    elif oyun.efekt_secim_aktif:
        oyun.efekt_menu_ciz(ekran)
    elif oyun.oyun_aktif:
        # Ara yüzey oluştur
        ara_yuzey = pygame.Surface((GENISLIK, YUKSEKLIK))
        ara_yuzey.fill(SIYAH)
        
        # Arka planı çiz
        oyun.arka_plan_ciz(ara_yuzey)
        
        # Tuş kontrollerini al
        tuslar = pygame.key.get_pressed()
        eski_x, eski_y = oyun.karakter_x, oyun.karakter_y
        
        # Birinci oyuncu hareketi
        if tuslar[pygame.K_LEFT]:
            oyun.karakter_x -= oyun.karakter_hiz
        if tuslar[pygame.K_RIGHT]:
            oyun.karakter_x += oyun.karakter_hiz
        if tuslar[pygame.K_UP]:
            oyun.karakter_y -= oyun.karakter_hiz
        if tuslar[pygame.K_DOWN]:
            oyun.karakter_y += oyun.karakter_hiz
            
        # Sınırları kontrol et
        oyun.karakter_x = max(0, min(oyun.karakter_x, GENISLIK - oyun.karakter_boyut))
        oyun.karakter_y = max(0, min(oyun.karakter_y, YUKSEKLIK - oyun.karakter_boyut))
        
        # Hareket varsa parçacık oluştur
        if (eski_x != oyun.karakter_x or eski_y != oyun.karakter_y):
            oyun.hareket_parcacigi_olustur(
                oyun.karakter_x + oyun.karakter_boyut//2,
                oyun.karakter_y + oyun.karakter_boyut//2,
                oyun.parcacik_rengi
            )
        
        # İkinci oyuncu kontrolü
        if oyun.coklu_oyuncu:
            eski_x2, eski_y2 = oyun.karakter2_x, oyun.karakter2_y
            if tuslar[pygame.K_a]:
                oyun.karakter2_x -= oyun.karakter2_hiz
            if tuslar[pygame.K_d]:
                oyun.karakter2_x += oyun.karakter2_hiz
            if tuslar[pygame.K_w]:
                oyun.karakter2_y -= oyun.karakter2_hiz
            if tuslar[pygame.K_s]:
                oyun.karakter2_y += oyun.karakter2_hiz
            
            # İkinci oyuncu sınırları
            oyun.karakter2_x = max(0, min(oyun.karakter2_x, GENISLIK - oyun.karakter2_boyut))
            oyun.karakter2_y = max(0, min(oyun.karakter2_y, YUKSEKLIK - oyun.karakter2_boyut))
            
            # İkinci oyuncu hareketi varsa parçacık oluştur
            if (eski_x2 != oyun.karakter2_x or eski_y2 != oyun.karakter2_y):
                oyun.hareket_parcacigi_olustur(
                    oyun.karakter2_x + oyun.karakter2_boyut//2,
                    oyun.karakter2_y + oyun.karakter2_boyut//2,
                    oyun.parcacik2_rengi
                )
        
        # Karakter hitbox'larını tanımla
        karakter_rect = pygame.Rect(oyun.karakter_x, oyun.karakter_y, 
                                   oyun.karakter_boyut, oyun.karakter_boyut)
        karakter2_rect = pygame.Rect(oyun.karakter2_x, oyun.karakter2_y, 
                                    oyun.karakter2_boyut, oyun.karakter2_boyut)
        
        # Nesne toplama kontrolü - Birinci oyuncu
        for nesne in oyun.nesneler[:]:
            if karakter_rect.colliderect(nesne):
                oyun.nesneler.remove(nesne)
                oyun.skor_ekle(1)  # Birinci oyuncu için puan ekle
                oyun.ses_cal(oyun.toplama_sesi)
                oyun.parcacik_efekti_olustur(nesne.centerx, nesne.centery, TURKUAZ)
                oyun.toplama_animasyonu_baslat(nesne, 1)
                if len(oyun.nesneler) == 0:
                    oyun.nesne_olustur()
        
        # İkinci oyuncu için nesne toplama kontrolü
        if oyun.coklu_oyuncu:
            for nesne in oyun.nesneler[:]:
                if karakter2_rect.colliderect(nesne):
                    oyun.nesneler.remove(nesne)
                    oyun.skor_ekle(2)  # İkinci oyuncu için puan ekle
                    oyun.ses_cal(oyun.toplama_sesi)
                    oyun.parcacik_efekti_olustur(nesne.centerx, nesne.centery, PEMBE)
                    oyun.toplama_animasyonu_baslat(nesne, 2)
                    if len(oyun.nesneler) == 0:
                        oyun.nesne_olustur()
        
        # Engel kontrolü
        for engel in oyun.engeller:
            if karakter_rect.colliderect(engel):
                oyun.oyun_aktif = False
                oyun.game_over = True
                oyun.ses_cal(oyun.game_over_sesi)
            if oyun.coklu_oyuncu and karakter2_rect.colliderect(engel):
                oyun.oyun_aktif = False
                oyun.game_over = True
                oyun.ses_cal(oyun.game_over_sesi)
        
        # Engelleri hareket ettir
        oyun.engelleri_hareket_ettir()
        
        # Seviye kontrolü
        oyun.seviye_guncelle()
        
        # Çizim sıralaması
        # 1. Parçacıkları güncelle ve çiz
        oyun.hareket_parcaciklarini_guncelle()
        oyun.hareket_parcaciklarini_ciz(ara_yuzey)
        
        # 2. Nesneleri çiz
        for nesne in oyun.nesneler:
            pygame.draw.rect(ara_yuzey, KOYU_TURKUAZ, nesne)
        
        # 3. Engelleri çiz
        for engel in oyun.engeller:
            oyun.tnt_ciz(ara_yuzey, engel.x, engel.y)
        
        # 4. Karakterleri çiz
        oyun.karakter_ciz(ara_yuzey)
        if oyun.coklu_oyuncu:
            oyun.karakter2_ciz(ara_yuzey)
        
        # 5. Toplama animasyonlarını çiz
        for nesne in oyun.toplanan_nesneler:
            scale = nesne['sure'] / TOPLAMA_ANIMASYON_SURESI
            boyut = int(nesne['baslangic_boyut'] * scale)
            renk = TURKUAZ if nesne['oyuncu'] == 1 else PEMBE
            pygame.draw.rect(ara_yuzey, renk, 
                           (nesne['rect'].centerx - boyut//2,
                            nesne['rect'].centery - boyut//2,
                            boyut, boyut))
        
        # 6. Animasyonları güncelle
        oyun.animasyonlari_guncelle()
        
        # 7. Skoru göster
        skor_text = font.render(f"Skor: {oyun.skor}", True, TURKUAZ)
        ara_yuzey.blit(skor_text, (GENISLIK - 80, 10))
        
        # 8. Seviye bilgisi çiz
        oyun.seviye_bilgisi_ciz(ara_yuzey)
        
        # Ara yüzeyi ekrana ölçeklendirerek çiz
        if oyun.tam_ekran:
            scaled_surface = pygame.transform.scale(ara_yuzey, 
                (oyun.ekran_genislik, oyun.ekran_yukseklik))
            ekran.blit(scaled_surface, (0, 0))
        else:
            ekran.blit(ara_yuzey, (0, 0))
    
    elif oyun.game_over:
        oyun.game_over_ekrani()
    
    pygame.display.flip()
    pygame.time.Clock().tick(60) 