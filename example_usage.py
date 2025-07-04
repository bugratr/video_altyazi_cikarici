#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Video Altyazı Çıkarıcı - Örnek Kullanım
Bu dosya uygulamanın nasıl kullanılacağını gösterir
"""

from video_subtitle_extractor import VideoSubtitleExtractor
import os
from pathlib import Path

def example_usage():
    """Örnek kullanım senaryoları"""
    
    # Örnek video dosyası yolu (kendi video dosyanızı kullanın)
    video_path = "ornek.mp4"
    
    # Video dosyası var mı kontrol et
    if not os.path.exists(video_path):
        print(f"❌ Örnek video dosyası bulunamadı: {video_path}")
        print("📁 Lütfen mevcut bir video dosyasının yolunu belirtin")
        return
    
    print("🎬 Video Altyazı Çıkarıcı - Örnek Kullanım")
    print("=" * 50)
    
    try:
        # 1. VideoSubtitleExtractor nesnesini oluştur
        print("📂 Video dosyası yükleniyor...")
        extractor = VideoSubtitleExtractor(video_path)
        
        # 2. Sadece gömülü altyazıları çıkar
        print("\n🔍 Gömülü altyazılar aranıyor...")
        embedded_subtitles = extractor.extract_embedded_subtitles("output/embedded")
        
        if embedded_subtitles:
            print(f"✅ {len(embedded_subtitles)} gömülü altyazı bulundu:")
            for subtitle in embedded_subtitles:
                print(f"   📄 {subtitle}")
        else:
            print("❌ Gömülü altyazı bulunamadı")
        
        # 3. Ses transkripsiyon yap (küçük model ile hızlı test)
        print("\n🎙️ Ses transkripsiyon yapılıyor (tiny model ile hızlı test)...")
        transcribed_subtitle = extractor.extract_audio_to_text("output/transcribed", "tiny")
        
        if transcribed_subtitle:
            print(f"✅ Ses transkripsiyon tamamlandı:")
            print(f"   📄 {transcribed_subtitle}")
        else:
            print("❌ Ses transkripsiyon başarısız")
        
        # 4. Tüm altyazıları çıkar
        print("\n🚀 Tüm altyazılar çıkarılıyor...")
        all_subtitles = extractor.extract_all_subtitles("output/all", use_whisper=True)
        
        print(f"\n📊 Sonuçlar:")
        print(f"   📁 Toplam çıkarılan altyazı: {len(all_subtitles)}")
        for i, subtitle in enumerate(all_subtitles, 1):
            print(f"   {i}. {subtitle}")
        
        print(f"\n✅ İşlem tamamlandı!")
        print(f"📁 Çıkarılan dosyalar 'output' klasöründe")
        
    except Exception as e:
        print(f"❌ Hata: {e}")

def simple_example():
    """En basit kullanım örneği"""
    
    video_file = input("🎬 Video dosyasının yolunu girin: ").strip()
    
    if not os.path.exists(video_file):
        print("❌ Video dosyası bulunamadı!")
        return
    
    try:
        print("🚀 İşlem başlatılıyor...")
        extractor = VideoSubtitleExtractor(video_file)
        
        # Hem gömülü hem de transkripsiyon
        subtitles = extractor.extract_all_subtitles()
        
        if subtitles:
            print(f"\n✅ {len(subtitles)} altyazı dosyası oluşturuldu:")
            for subtitle in subtitles:
                print(f"   📄 {subtitle}")
        else:
            print("❌ Altyazı çıkarılamadı")
            
    except Exception as e:
        print(f"❌ Hata: {e}")

def interactive_example():
    """Etkileşimli örnek"""
    
    print("🎬 Video Altyazı Çıkarıcı - Etkileşimli Mod")
    print("=" * 50)
    
    # Video dosyası al
    video_file = input("📁 Video dosyasının yolunu girin: ").strip()
    if not os.path.exists(video_file):
        print("❌ Video dosyası bulunamadı!")
        return
    
    # Seçenekler
    print("\n🎯 Hangi işlemi yapmak istiyorsunuz?")
    print("1. Sadece gömülü altyazıları çıkar")
    print("2. Sadece ses transkripsiyon yap")
    print("3. Her ikisini de yap")
    
    choice = input("Seçiminiz (1-3): ").strip()
    
    try:
        extractor = VideoSubtitleExtractor(video_file)
        
        if choice == "1":
            # Sadece gömülü
            subtitles = extractor.extract_embedded_subtitles()
            
        elif choice == "2":
            # Sadece transkripsiyon
            # Model seçimi
            print("\n🎚️ Whisper model seçin:")
            print("1. tiny (hızlı, düşük kalite)")
            print("2. base (dengeli)")
            print("3. small (yüksek kalite)")
            
            model_choice = input("Model seçimi (1-3): ").strip()
            models = {"1": "tiny", "2": "base", "3": "small"}
            model = models.get(model_choice, "base")
            
            subtitle = extractor.extract_audio_to_text(model_size=model)
            subtitles = [subtitle] if subtitle else []
            
        elif choice == "3":
            # Her ikisi
            subtitles = extractor.extract_all_subtitles()
            
        else:
            print("❌ Geçersiz seçim!")
            return
        
        # Sonuçları göster
        if subtitles:
            print(f"\n✅ {len(subtitles)} altyazı dosyası oluşturuldu:")
            for subtitle in subtitles:
                print(f"   📄 {subtitle}")
        else:
            print("❌ Altyazı çıkarılamadı")
            
    except Exception as e:
        print(f"❌ Hata: {e}")

if __name__ == "__main__":
    print("🎬 Video Altyazı Çıkarıcı - Örnekler")
    print("=" * 50)
    print("1. Örnek kullanım (önceden tanımlı video ile)")
    print("2. Basit kullanım")
    print("3. Etkileşimli kullanım")
    
    choice = input("\nHangi örneği çalıştırmak istiyorsunuz? (1-3): ").strip()
    
    if choice == "1":
        example_usage()
    elif choice == "2":
        simple_example()
    elif choice == "3":
        interactive_example()
    else:
        print("❌ Geçersiz seçim!") 