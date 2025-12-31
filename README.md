# Yapay Zeka Destekli Hastane Randevu Sistemi

Bu proje, hastaların sağlık şikayetlerini analiz ederek doğru polikliniğe yönlendiren, sesli komutlarla çalışabilen ve acil durumları tespit edebilen **Django tabanlı akıllı bir randevu yönetim sistemidir.**

Standart randevu sistemlerinden farklı olarak **Google Gemini AI** entegrasyonu sayesinde hastaların tıbbi terim bilmesine gerek kalmadan, sadece şikayetlerini söyleyerek doğru doktora ulaşmasını sağlar.

## Öne Çıkan Özellikler

### 1. AI Destekli Branş Tespiti (Google Gemini)
Kullanıcı şikayetini doğal bir dille yazar (örn: *"Sabahları uyanınca gözüm bulanık görüyor"*). Sistem arka planda **Google Gemini API** kullanarak bu şikayeti analiz eder ve hastayı otomatik olarak **Göz Hastalıkları** bölümüne yönlendirir.

### 2. Akıllı Sesli Asistan
Klavye kullanmakta zorlanan hastalar için **Web Speech API** teknolojisi kullanılmıştır. Mikrofon ikonuna basılarak söylenen şikayetler anlık olarak metne çevrilir ve sisteme işlenir.

### 3. Acil Durum Tespiti
Şikayet metni içerisinde hayati risk taşıyan anahtar kelimeler (örn: *"kalp krizi", "nefes alamıyorum", "bayılma"* vb.) geçtiğinde sistem bunu algılar. Kullanıcıya anında kırmızı uyarı ekranı göstererek acil durum prosedürlerini devreye sokar.

### 4. Kapsamlı Randevu Yönetimi
* **Dinamik Saatler:** Doktorların doluluk durumuna göre sadece boş saatler listelenir.
* **Raporlarım:** Hastalar doktorların yüklediği tahlil ve rapor sonuçlarını görüntüleyebilir.

## Kullanılan Teknolojiler

| Alan | Teknoloji | Açıklama |
| **Backend** | Python, Django | Sunucu tarafı mimarisi ve veritabanı yönetimi |
| **Yapay Zeka** | Google Gemini API | Doğal Dil İşleme (NLP) ve karar destek sistemi |
| **Frontend** | HTML, CSS, JavaScript | Kullanıcı arayüzü ve dinamik etkileşimler |
| **Ses İşleme** | Web Speech API | Tarayıcı tabanlı ses tanıma teknolojisi |
| **Veritabanı** | SQLite | Veri saklama (Geliştirme ortamı için) |


## Ekran Görüntüleri
<img width="1918" height="867" alt="Rapor" src="https://github.com/user-attachments/assets/2631b8a3-2962-405b-9917-91c707fd1a80" />
<img width="1901" height="870" alt="GecmisRandevu" src="https://github.com/user-attachments/assets/9613085b-37db-493f-9aa5-fefbe4bc9115" />
<img width="1898" height="867" alt="Anasayfa" src="https://github.com/user-attachments/assets/ad0c24a1-36d1-4bf9-8ba9-c57e71217de0" />
<img width="1287" height="865" alt="Randevu" src="https://github.com/user-attachments/assets/77b1de70-3a0d-462f-b1ce-00ecce4dd76c" />


## ⚙️ Kurulum (Nasıl Çalıştırılır?)

Projeyi kendi bilgisayarınızda çalıştırmak için:

1.  Depoyu klonlayın:
    ```bash
    git clone [https://github.com/KULLANICI_ADIN/REPO_ISMI.git](https://github.com/KULLANICI_ADIN/REPO_ISMI.git)
    ```
2.  Gerekli kütüphaneleri yükleyin:
    ```bash
    pip install -r requirements.txt
    ```
3.  Veritabanını oluşturun:
    ```bash
    python manage.py migrate
    ```
4.  Sunucuyu başlatın:
    ```bash
    python manage.py runserver
    ```

**Geliştirici:** Özkan Şimşek
