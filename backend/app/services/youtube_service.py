"""
Serviço para extrair informações de vídeos do YouTube usando yt-dlp
"""
import yt_dlp
from typing import Optional, Dict
import logging

logger = logging.getLogger(__name__)


def get_video_info(video_id: str) -> Optional[Dict]:
    """
    Extrai informações do vídeo do YouTube usando yt-dlp
    Retorna a URL DIRETA do arquivo de vídeo (não a página web)
    
    Args:
        video_id: ID do vídeo no YouTube (ex: dQw4w9WgXcQ)
    
    Returns:
        Dict com url (direta), title, thumbnail_url, duration
    """
    try:
        urls_to_try = [
            f"https://www.youtube.com/watch?v={video_id}",
            f"https://www.youtube.com/shorts/{video_id}"
        ]
        
        for youtube_url in urls_to_try:
            try:
                ydl_opts = {
                    'quiet': True,
                    'no_warnings': True,
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(youtube_url, download=False)
                    
                    if not info:
                        continue
                    
                    # YouTube usa DASH (streams separados de vídeo e áudio)
                    # Retornar TODAS as opções para o app decidir
                    
                    formats = info.get('formats', [])
                    
                    # 1. Tentar formatos combinados (vídeo + áudio)
                    video_audio_formats = [
                        f for f in formats 
                        if f.get('url') and 
                        f.get('vcodec') != 'none' and 
                        f.get('acodec') != 'none' and 
                        'googlevideo.com' in f.get('url', '')
                    ]
                    
                    # 2. Formatos separados (DASH)
                    video_only = [
                        f for f in formats 
                        if f.get('url') and 
                        f.get('vcodec') != 'none' and 
                        f.get('acodec') == 'none' and 
                        'googlevideo.com' in f.get('url', '')
                    ]
                    
                    audio_only = [
                        f for f in formats 
                        if f.get('url') and 
                        f.get('vcodec') == 'none' and 
                        f.get('acodec') != 'none' and 
                        'googlevideo.com' in f.get('url', '')
                    ]
                    
                    # Priorizar formato combinado
                    if video_audio_formats:
                        best = video_audio_formats[-1]
                        logger.info(f"Formato combinado encontrado: {best.get('format_id')}")
                        return {
                            'url': best.get('url'),
                            'audio_url': None,
                            'youtube_url': youtube_url,
                            'title': info.get('title'),
                            'thumbnail_url': info.get('thumbnail'),
                            'duration': info.get('duration'),
                            'description': info.get('description'),
                            'uploader': info.get('uploader'),
                            'view_count': info.get('view_count'),
                        }
                    
                    # Se só tem separados (DASH), retornar ambos
                    elif video_only and audio_only:
                        best_video = video_only[-1]
                        best_audio = audio_only[-1]
                        logger.info(f"DASH detectado: vídeo={best_video.get('format_id')}, áudio={best_audio.get('format_id')}")
                        return {
                            'url': best_video.get('url'),
                            'audio_url': best_audio.get('url'),
                            'youtube_url': youtube_url,
                            'title': info.get('title'),
                            'thumbnail_url': info.get('thumbnail'),
                            'duration': info.get('duration'),
                            'description': info.get('description'),
                            'uploader': info.get('uploader'),
                            'view_count': info.get('view_count'),
                        }
                    
                    # Se só tem vídeo
                    elif video_only:
                        best_video = video_only[-1]
                        logger.warning(f"Apenas vídeo disponível: {best_video.get('format_id')}")
                        return {
                            'url': best_video.get('url'),
                            'audio_url': None,
                            'youtube_url': youtube_url,
                            'title': info.get('title'),
                            'thumbnail_url': info.get('thumbnail'),
                            'duration': info.get('duration'),
                            'description': info.get('description'),
                            'uploader': info.get('uploader'),
                            'view_count': info.get('view_count'),
                        }
                    
            except Exception as e:
                logger.debug(f"Tentativa com {youtube_url} falhou: {str(e)}")
                continue
        
        # Se ambas falharam, retornar URL da página (fallback)
        logger.warning(f"Não foi possível extrair URL direta do vídeo {video_id}, retornando URL da página")
        return {
            'url': f"https://www.youtube.com/watch?v={video_id}",
            'title': None,
            'thumbnail_url': f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
            'duration': None,
        }
    
    except Exception as e:
        logger.error(f"Erro ao extrair info do vídeo {video_id}: {str(e)}")
        return {
            'url': f"https://www.youtube.com/watch?v={video_id}",
            'title': None,
            'thumbnail_url': f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
            'duration': None,
        }


def extract_video_id(url_or_id: str) -> str:
    """
    Extrai o ID do vídeo de uma URL do YouTube ou retorna o ID se já for um
    
    Args:
        url_or_id: URL completa ou ID do vídeo
    
    Returns:
        ID do vídeo (ex: dQw4w9WgXcQ)
    """
    # Se já for só o ID (sem / ou ?), retorna direto
    if '/' not in url_or_id and '?' not in url_or_id:
        return url_or_id
    
    # Tenta extrair o ID de URLs comuns do YouTube
    if 'youtu.be/' in url_or_id:
        # https://youtu.be/dQw4w9WgXcQ
        return url_or_id.split('youtu.be/')[-1].split('?')[0]
    elif 'youtube.com/watch?v=' in url_or_id:
        # https://www.youtube.com/watch?v=dQw4w9WgXcQ
        return url_or_id.split('v=')[-1].split('&')[0]
    elif 'youtube.com/embed/' in url_or_id:
        # https://www.youtube.com/embed/dQw4w9WgXcQ
        return url_or_id.split('embed/')[-1].split('?')[0]
    
    # Fallback: retorna o que foi passado
    return url_or_id

