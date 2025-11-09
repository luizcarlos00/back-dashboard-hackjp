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
    
    Args:
        video_id: ID do vídeo no YouTube (ex: dQw4w9WgXcQ)
    
    Returns:
        Dict com url, title, thumbnail_url, duration ou None se falhar
    """
    try:
        # Tentar como vídeo normal primeiro, depois como Shorts
        urls_to_try = [
            f"https://www.youtube.com/watch?v={video_id}",
            f"https://www.youtube.com/shorts/{video_id}"
        ]
        
        for url in urls_to_try:
            try:
                ydl_opts = {
                    'quiet': True,
                    'no_warnings': True,
                    'extract_flat': False,
                    'format': 'best/bestvideo+bestaudio',
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    
                    if info:
                        # Construir URL do YouTube (para exibir no app)
                        youtube_url = f"https://www.youtube.com/watch?v={video_id}"
                        if 'shorts' in url:
                            youtube_url = f"https://www.youtube.com/shorts/{video_id}"
                        
                        return {
                            'url': youtube_url,  # URL do YouTube para exibir
                            'title': info.get('title'),
                            'thumbnail_url': info.get('thumbnail'),
                            'duration': info.get('duration'),
                            'description': info.get('description'),
                            'uploader': info.get('uploader'),
                            'view_count': info.get('view_count'),
                        }
            except Exception as e:
                logger.debug(f"Tentativa com {url} falhou: {str(e)}")
                continue
        
        # Se ambas falharam, retornar URL básica do YouTube
        logger.warning(f"Não foi possível extrair info detalhada do vídeo {video_id}, usando URL padrão")
        return {
            'url': f"https://www.youtube.com/watch?v={video_id}",
            'title': None,
            'thumbnail_url': f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
            'duration': None,
        }
    
    except Exception as e:
        logger.error(f"Erro ao extrair info do vídeo {video_id}: {str(e)}")
        # Fallback: retornar URL básica
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

