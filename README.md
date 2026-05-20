# FuzzyDev
## Akıllı Yazılım Geliştirici Verimlilik ve Yorgunluk Analiz Sistemi

### Proje Hakkında

FuzzyDev, yazılım geliştiricilerin günlük çalışma koşullarına göre verimlilik düzeylerini bulanık mantık yöntemi ile analiz eden bir karar destek sistemidir.

Sistem aşağıdaki girdileri kullanmaktadır:

- Çalışma süresi
- Uyku süresi
- Aktivite seviyesi
- Stres seviyesi

Bu girdiler bulanık mantık yöntemleri ile değerlendirilerek kullanıcı için 0–100 arası bir verimlilik skoru oluşturulmaktadır.

---

## Kullanılan Teknolojiler

- Python
- Scikit-Fuzzy
- NumPy
- Pandas
- Matplotlib
- Streamlit

---

## Sistem Mimarisi

Giriş Değişkenleri:

1. Çalışma Süresi (0–12 saat)

Dilsel ifadeler:

- Az
- Normal
- Fazla

2. Uyku Süresi (0–10 saat)

Dilsel ifadeler:

- Kötü
- Orta
- İyi

3. Aktivite Seviyesi (0–100)

Dilsel ifadeler:

- Düşük
- Orta
- Yüksek

4. Stres Seviyesi (0–100)

Dilsel ifadeler:

- Düşük
- Orta
- Yüksek

Çıkış:

Verimlilik Skoru (0–100)

Dilsel ifadeler:

- Çok Düşük
- Düşük
- Orta
- Yüksek
- Çok Yüksek

---

## Bulanık Mantık Süreci

### Bulanıklaştırma

Sistem kullanıcıdan alınan sayısal girişleri üyelik fonksiyonları yardımıyla dilsel değerlere dönüştürmektedir.

### Kural Tabanı

Projede 20 farklı IF–THEN kuralı kullanılmıştır.

Örnek:

IF çalışma süresi Normal  
AND uyku İyi  
AND aktivite Yüksek  
AND stres Düşük

THEN verimlilik Çok Yüksek

### Çıkarım Motoru

Mamdani çıkarım yöntemi kullanılmıştır.

### Durulaştırma

Centroid (Ağırlık Merkezi) yöntemi kullanılmıştır.

---

## Arayüz Özellikleri

✔ Slider ile giriş alma

✔ Gerçek zamanlı sonuç üretme

✔ Üyelik fonksiyonlarının gösterimi

✔ Aktif kuralların listelenmesi

✔ Durulaştırılmış sonuç grafiği

✔ Test senaryoları

---

## Kurulum

Projeyi klonlayın:

```bash
git clone PROJE_LINKI
```

Klasöre girin:

```bash
cd FuzzyDev
```

Gerekli kütüphaneleri kurun:

```bash
pip install -r requirements.txt
```

Projeyi çalıştırın:

```bash
streamlit run app.py
```

---

## Test Sonuçları

Proje içerisinde örnek test senaryoları bulunmaktadır.

Örnek:

| Çalışma | Uyku | Aktivite | Stres | Sonuç |
|----------|-------|----------|--------|--------|
|6|8|85|20|Çok Yüksek|
|9|3|30|90|Çok Düşük|

---

## Geliştirici

Hatice Kocatürk

GitHub:

https://github.com/haticekctrk02

LinkedIn:

www.linkedin.com/in/hatice-kocatürk-94b311288