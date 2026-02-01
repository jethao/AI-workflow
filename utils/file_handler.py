import json
import os
from pathlib import Path
from typing import Any, Dict
from datetime import datetime


class FileHandler:
    """Utility for handling file I/O operations"""

    @staticmethod
    def ensure_dir(directory: str) -> None:
        """Ensure directory exists"""
        Path(directory).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def save_json(data: Dict[str, Any], filepath: str) -> None:
        """Save data as JSON file"""
        FileHandler.ensure_dir(os.path.dirname(filepath))
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)

    @staticmethod
    def load_json(filepath: str) -> Dict[str, Any]:
        """Load JSON file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def save_text(content: str, filepath: str) -> None:
        """Save text to file"""
        FileHandler.ensure_dir(os.path.dirname(filepath))
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    @staticmethod
    def load_text(filepath: str) -> str:
        """Load text from file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def create_timestamped_filename(base_name: str, extension: str) -> str:
        """Create filename with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{base_name}_{timestamp}.{extension}"
