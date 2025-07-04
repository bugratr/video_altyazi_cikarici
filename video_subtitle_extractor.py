#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Video Altyazı Çıkarıcı
Bu uygulama video dosyalarından altyazı çıkarmak için iki farklı yöntem kullanır:
1. Gömülü altyazıları çıkarma (ffmpeg kullanarak)
2. Ses transkripsiyon (Whisper AI kullanarak)
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path
import logging
from typing import List, Optional, Dict, Any
import argparse

try:
    import ffmpeg
    from moviepy.editor import VideoFileClip
    import whisper
except ImportError as e:
    print(f"Gerekli kütüphaneler eksik: {e}")
    print("Lütfen 'pip install -r requirements.txt' komutunu çalıştırın")
    sys.exit(1)

# Logging ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('video_subtitle_extractor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class VideoSubtitleExtractor:
    """Video dosyalarından altyazı çıkarma sınıfı"""
    
    def __init__(self, video_path: str):
        self.video_path = Path(video_path)
        self.whisper_model = None
        
        if not self.video_path.exists():
            raise FileNotFoundError(f"Video dosyası bulunamadı: {video_path}")
        
        logger.info(f"Video dosyası yüklendi: {self.video_path}")
    
    def extract_embedded_subtitles(self, output_dir: str = "subtitles") -> List[str]:
        """
        Video dosyasından gömülü altyazıları çıkarır
        
        Args:
            output_dir: Altyazı dosyalarının kaydedileceği dizin
            
        Returns:
            Çıkarılan altyazı dosyalarının listesi
        """
        logger.info("Gömülü altyazılar aranıyor...")
        
        # Çıktı dizinini oluştur
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # ffprobe ile altyazı akışlarını kontrol et
        try:
            probe = ffmpeg.probe(str(self.video_path))
            subtitle_streams = [
                stream for stream in probe['streams'] 
                if stream['codec_type'] == 'subtitle'
            ]
            
            if not subtitle_streams:
                logger.warning("Video dosyasında gömülü altyazı bulunamadı")
                return []
            
            logger.info(f"{len(subtitle_streams)} altyazı akışı bulundu")
            
            extracted_files = []
            
            for i, stream in enumerate(subtitle_streams):
                # Altyazı formatını belirle
                codec_name = stream.get('codec_name', 'unknown')
                language = stream.get('tags', {}).get('language', 'unknown')
                
                # Çıktı dosya adını oluştur
                base_name = self.video_path.stem
                if language != 'unknown':
                    subtitle_filename = f"{base_name}_{language}_{i}.srt"
                else:
                    subtitle_filename = f"{base_name}_subtitle_{i}.srt"
                
                subtitle_path = output_path / subtitle_filename
                
                try:
                    # ffmpeg ile altyazıyı çıkar
                    (
                        ffmpeg
                        .input(str(self.video_path))
                        .output(str(subtitle_path), map=f'0:s:{i}', c='srt')
                        .overwrite_output()
                        .run(quiet=True)
                    )
                    
                    extracted_files.append(str(subtitle_path))
                    logger.info(f"Altyazı çıkarıldı: {subtitle_path}")
                    
                except ffmpeg.Error as e:
                    logger.error(f"Altyazı çıkarma hatası (akış {i}): {e}")
                    continue
            
            return extracted_files
            
        except Exception as e:
            logger.error(f"Gömülü altyazı çıkarma hatası: {e}")
            return []
    
    def extract_audio_to_text(self, output_dir: str = "subtitles", 
                             model_size: str = "base") -> Optional[str]:
        """
        Video dosyasından ses çıkararak Whisper AI ile transkripsiyon yapar
        
        Args:
            output_dir: Altyazı dosyasının kaydedileceği dizin
            model_size: Whisper model boyutu (tiny, base, small, medium, large)
            
        Returns:
            Oluşturulan altyazı dosyasının yolu
        """
        logger.info("Ses transkripsiyon işlemi başlatılıyor...")
        
        # Çıktı dizinini oluştur
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        try:
            # Whisper modelini yükle
            if self.whisper_model is None:
                logger.info(f"Whisper model yükleniyor: {model_size}")
                self.whisper_model = whisper.load_model(model_size)
            
            # Geçici ses dosyası oluştur
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
                temp_audio_path = temp_audio.name
            
            logger.info("Video dosyasından ses çıkarılıyor...")
            
            # MoviePy ile ses çıkar
            video_clip = VideoFileClip(str(self.video_path))
            audio_clip = video_clip.audio
            audio_clip.write_audiofile(temp_audio_path, verbose=False, logger=None)
            
            # Kaynakları temizle
            audio_clip.close()
            video_clip.close()
            
            logger.info("Ses transkripsiyon işlemi yapılıyor...")
            
            # Whisper ile transkripsiyon yap
            result = self.whisper_model.transcribe(
                temp_audio_path,
                language='tr'  # Türkçe olarak ayarlandı
            )
            
            # SRT formatında altyazı dosyası oluştur
            base_name = self.video_path.stem
            subtitle_filename = f"{base_name}_transcribed.srt"
            subtitle_path = output_path / subtitle_filename
            
            self._write_srt_file(result, subtitle_path)
            
            # Geçici dosyayı sil
            os.unlink(temp_audio_path)
            
            logger.info(f"Ses transkripsiyon tamamlandı: {subtitle_path}")
            return str(subtitle_path)
            
        except Exception as e:
            logger.error(f"Ses transkripsiyon hatası: {e}")
            return None
    
    def _write_srt_file(self, whisper_result: Dict[Any, Any], output_path: Path):
        """Whisper sonuçlarını SRT formatında dosyaya yazar"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for i, segment in enumerate(whisper_result['segments'], 1):
                start_time = self._format_time(segment['start'])
                end_time = self._format_time(segment['end'])
                text = segment['text'].strip()
                
                f.write(f"{i}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{text}\n\n")
    
    def _format_time(self, seconds: float) -> str:
        """Saniyeyi SRT zaman formatına çevirir"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = seconds % 60
        
        return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}".replace('.', ',')
    
    def extract_all_subtitles(self, output_dir: str = "subtitles", 
                             use_whisper: bool = True) -> List[str]:
        """
        Hem gömülü altyazıları hem de ses transkripsiyon ile altyazı çıkarır
        
        Args:
            output_dir: Altyazı dosyalarının kaydedileceği dizin
            use_whisper: Whisper AI ile transkripsiyon yapılsın mı
            
        Returns:
            Tüm çıkarılan altyazı dosyalarının listesi
        """
        all_subtitles = []
        
        # Gömülü altyazıları çıkar
        embedded_subtitles = self.extract_embedded_subtitles(output_dir)
        all_subtitles.extend(embedded_subtitles)
        
        # Whisper ile transkripsiyon yap
        if use_whisper:
            transcribed_subtitle = self.extract_audio_to_text(output_dir)
            if transcribed_subtitle:
                all_subtitles.append(transcribed_subtitle)
        
        return all_subtitles

def main():
    parser = argparse.ArgumentParser(description='Video Altyazı Çıkarıcı')
    parser.add_argument('video_path', help='Video dosyasının yolu')
    parser.add_argument('--output-dir', '-o', default='subtitles', 
                       help='Çıktı dizini (varsayılan: subtitles)')
    parser.add_argument('--no-whisper', action='store_true', 
                       help='Whisper AI transkripsiyon kullanma')
    parser.add_argument('--whisper-model', default='base', 
                       choices=['tiny', 'base', 'small', 'medium', 'large'],
                       help='Whisper model boyutu')
    parser.add_argument('--embedded-only', action='store_true', 
                       help='Sadece gömülü altyazıları çıkar')
    parser.add_argument('--transcribe-only', action='store_true', 
                       help='Sadece ses transkripsiyon yap')
    
    args = parser.parse_args()
    
    try:
        extractor = VideoSubtitleExtractor(args.video_path)
        
        if args.embedded_only:
            # Sadece gömülü altyazıları çıkar
            subtitles = extractor.extract_embedded_subtitles(args.output_dir)
        elif args.transcribe_only:
            # Sadece transkripsiyon yap
            subtitle = extractor.extract_audio_to_text(args.output_dir, args.whisper_model)
            subtitles = [subtitle] if subtitle else []
        else:
            # Tüm yöntemleri kullan
            use_whisper = not args.no_whisper
            subtitles = extractor.extract_all_subtitles(args.output_dir, use_whisper)
        
        if subtitles:
            print(f"\n✅ Altyazı çıkarma işlemi tamamlandı!")
            print(f"📁 Çıkarılan dosyalar:")
            for subtitle in subtitles:
                print(f"   - {subtitle}")
        else:
            print("\n❌ Herhangi bir altyazı çıkarılamadı.")
            
    except Exception as e:
        logger.error(f"Uygulama hatası: {e}")
        print(f"❌ Hata: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 