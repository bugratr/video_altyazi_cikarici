# 🎬 Video Altyazı Çıkarıcı

Python ile geliştirilmiş video dosyalarından altyazı çıkarma uygulaması. İki farklı yöntemle çalışır:

1. **Gömülü Altyazılar**: Video dosyasında zaten mevcut olan altyazıları çıkarır
2. **Ses Transkripsiyon**: OpenAI Whisper AI kullanarak video sesini metne çevirir

## ✨ Özellikler

- 🎯 **Çift Mod**: Hem gömülü altyazıları hem de ses transkripsiyon
- 💻 **Komut Satırı**: Hızlı ve etkili konsol arayüzü
- 🌍 **Türkçe Destek**: Whisper AI ile Türkçe transkripsiyon
- 📝 **SRT Format**: Standart altyazı formatında çıktı
- 🎚️ **Model Seçenekleri**: Farklı Whisper model boyutları
- 📊 **İşlem Logları**: Detaylı işlem takibi
- ⚡ **Hızlı**: Minimum bağımlılık ile hafif çalışma

## 📋 Gereksinimler

### Sistem Gereksinimleri
- Python 3.7+
- FFmpeg (sistem PATH'inde olmalı)
- En az 4GB RAM (büyük video dosyaları için)

### Python Paketleri
```bash
pip install -r requirements.txt
```

## 🚀 Kurulum

1. **Projeyi klonlayın:**
```bash
git clone <repository-url>
cd video-altyazi
```

2. **Gerekli paketleri yükleyin:**
```bash
pip install -r requirements.txt
```

3. **FFmpeg'i kurun:**

**Windows:**
- [FFmpeg](https://ffmpeg.org/download.html#build-windows) sitesinden indirin
- Dosyaları `C:\ffmpeg\bin` klasörüne çıkarın
- System PATH'e `C:\ffmpeg\bin` ekleyin

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt update
sudo apt install ffmpeg
```

## 🎯 Kullanım

**Temel kullanım:**
```bash
python video_subtitle_extractor.py video.mp4
```

**Gelişmiş seçenekler:**
```bash
# Sadece gömülü altyazıları çıkar
python video_subtitle_extractor.py video.mp4 --embedded-only

# Sadece ses transkripsiyon yap
python video_subtitle_extractor.py video.mp4 --transcribe-only

# Özel çıktı dizini
python video_subtitle_extractor.py video.mp4 -o /path/to/output

# Farklı Whisper model
python video_subtitle_extractor.py video.mp4 --whisper-model large

# Whisper kullanma
python video_subtitle_extractor.py video.mp4 --no-whisper
```

## 🎚️ Whisper Model Boyutları

| Model | Boyut | Hız | Kalite | Önerilen Kullanım |
|-------|-------|-----|--------|------------------|
| `tiny` | 39 MB | En hızlı | Düşük | Hızlı test |
| `base` | 74 MB | Hızlı | İyi | **Genel kullanım** |
| `small` | 244 MB | Orta | Yüksek | Kaliteli sonuç |
| `medium` | 769 MB | Yavaş | Çok yüksek | Profesyonel |
| `large` | 1550 MB | En yavaş | En yüksek | Mükemmel kalite |

## 📁 Çıktı Dosyaları

Uygulama aşağıdaki dosyaları oluşturur:

```
subtitles/
├── video_turkish_0.srt          # Gömülü Türkçe altyazı
├── video_english_1.srt          # Gömülü İngilizce altyazı
├── video_transcribed.srt        # Whisper transkripsiyon
└── video_subtitle_extractor.log # İşlem logları
```

## 🔧 Sorun Giderme

### FFmpeg Bulunamadı
```bash
# FFmpeg kurulu mu kontrol et
ffmpeg -version

# PATH'e ekle (Windows)
set PATH=%PATH%;C:\ffmpeg\bin

# PATH'e ekle (macOS/Linux)
export PATH=$PATH:/usr/local/bin
```

### Whisper Model İndirme
İlk kullanımda Whisper modeli otomatik indirilir. İnternet bağlantısı gereklidir.

### Bellek Hatası
Büyük video dosyaları için:
- Daha küçük Whisper modeli seçin (`tiny` veya `base`)
- Videoyu parçalara bölün
- Sistem belleğini artırın

### Desteklenen Video Formatları
- MP4, AVI, MKV, MOV, WMV, FLV, WebM, M4V
- Diğer formatlar FFmpeg destekli olmalı

## 📊 Performans İpuçları

1. **Hızlı Test**: `tiny` model kullanın
2. **Dengeli Kullanım**: `base` model (önerilen)
3. **Yüksek Kalite**: `small` veya `medium` model
4. **Profesyonel**: `large` model
5. **Sadece Gömülü**: `--embedded-only` parametresi

## 🐛 Bilinen Sorunlar

- Çok büyük video dosyaları bellek hatası verebilir
- Bazı eski video formatları desteklenmeyebilir
- İnternet bağlantısı Whisper model indirimi için gerekli

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📝 Lisans

Bu proje MIT lisansı altında dağıtılmaktadır.

## 🙏 Teşekkürler

- [OpenAI Whisper](https://github.com/openai/whisper) - Ses transkripsiyon
- [FFmpeg](https://ffmpeg.org/) - Video işleme
- [MoviePy](https://github.com/Zulko/moviepy) - Video manipülasyonu

## 📞 İletişim

Sorularınız için issue açabilir veya pull request gönderebilirsiniz.

---

⭐ **Projeyi beğendiyseniz yıldız vermeyi unutmayın!** # video_altyazi_cikarici
