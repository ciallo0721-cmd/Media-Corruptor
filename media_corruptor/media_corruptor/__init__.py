"""
Media Corruptor - A tool to partially corrupt media files
"""

from .corruptor import corrupt_media_file, corrupt_media_file_safe

__version__ = "0.1.0"
__all__ = ['corrupt_media_file', 'corrupt_media_file_safe']
