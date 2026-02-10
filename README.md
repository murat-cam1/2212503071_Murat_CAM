# 🚗 El Hareketleri ile İnteraktif Araba Park Etme Oyunu

Bu proje, **Python**, **OpenCV** ve **MediaPipe** kütüphaneleri kullanılarak geliştirilmiş bir bilgisayarlı görü (Computer Vision) uygulamasıdır. Kullanıcılar, fiziksel bir fare veya klavye kullanmak yerine sadece el hareketlerini kullanarak ekrandaki araçları park yerlerine taşırlar.



## 🎯 Projenin Amacı
Yapay zeka ve görüntü işleme tekniklerini kullanarak insan-bilgisayar etkileşimini (HCI) eğlenceli bir oyun kurgusuyla deneyimlemek.

## 🚀 Öne Çıkan Özellikler

* **El Takibi (Hand Tracking):** MediaPipe kütüphanesi ile eldeki 21 farklı eklem noktası gerçek zamanlı takip edilir.
* **Sürükle-Bırak Mekaniği:** İşaret parmağı ucu (Landmark 8) bir arabanın üzerine geldiğinde araba parmağa "yapışır".
* **Akıllı Kontrol:** Arabaların ID numaraları ile park yerlerinin ID numaraları eşleşmelidir. Yanlış yere park etmeye çalışıldığında araç başlangıç noktasına döner.
* **Gelişmiş Ses Sistemi:** `Pygame` mixer kanalları sayesinde motor sesi, korna ve efektler birbirini kesmeden aynı anda çalabilir.
* **Hızlı Reset:** `R` tuşu ile oyun her an sıfırlanabilir.

## 🛠️ Kurulum

Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin:

1.  **Gerekli Kütüphaneleri Yükleyin:**
    ```bash
    pip install opencv-python mediapipe pygame numpy
    ```

2.  **Gerekli Dosyalar:**
    Kodun çalışması için aşağıdaki dosyaların ana dizinde bulunması gerekir:
    * `car.png` (Araç görseli)
    * `engine.wav` (Motor sesi)
    * `park.wav` (Başarılı park sesi)
    * `error.wav` (Hata sesi)
    * `horn.wav` (Korna sesi)

3.  **Çalıştırın:**
    ```bash
    python main.py
    ```

## 🎮 Oyun Kuralları ve Kontroller

* **Aracı Seçme:** İşaret parmağınızı aracın üzerine getirin.
* **Park Etme:** Aracı ekranın sağındaki ilgili mavi kutuya sürükleyin.
* **Korna:** Elinizi 5 parmak açık şekilde kameraya gösterdiğinizde korna çalar.
* **Süre:** 60 saniye içinde tüm araçları park etmeniz gerekir.
* **Tekrar Başlatma:** Oyun bitince veya ortasında `R` tuşuna basarak her şeyi sıfırlayabilirsiniz.
* **Çıkış:** `ESC` tuşuna basarak programdan çıkabilirsiniz.

## 📂 Dosya Yapısı ve Görevleri

* `main.py`: Görüntü işleme, el takibi algoritması ve oyun mantığının bulunduğu ana dosya.
* `draw_png_fixed`: PNG dosyalarındaki şeffaflık (alpha channel) sorununu çözen özel çizim fonksiyonu.
* `create_game_objects`: Oyunun her başında araçları ve park yerlerini yeniden tanımlayan fonksiyon.

## 🖥️ Teknik Detaylar
Bu projede kullanılan temel algoritmalar şunlardır:
* **Alpha Blending:** Görsellerin arka planla pürüzsüz birleşmesi için.
* **Euclidean Distance (Öklid Mesafesi):** Parmakların açık olup olmadığını kontrol etmek için koordinat farkı analizi.
* **Bounding Box Kontrolü:** Arabanın park alanı içinde olup olmadığını saptayan geometrik kontrol.

---
⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayn!
