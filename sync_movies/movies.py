from os import path
from pathlib import Path
from typing import List
from glob import glob

def get_video_files_from_folder(folder: str) -> List[Path]:
    all_files = [
        Path(file_path)
        for file_path in glob(path.join(folder, "**/*"), recursive=True)
    ]

    movies = [
        path
        for path in all_files
        if path.suffix in [".mkv", ".avi", ".mp4", ".mpeg4"]
    ]

    return movies
