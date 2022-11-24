from .spreadsheet import get_spreadsheet, write_to_spreadsheet
from .movies import get_video_files_from_folder
from pathlib import Path
from typing import List, Any


def main():
    movies_files = get_movies_files()
    series_files = get_series_files()

    sheet = get_spreadsheet()
    save_files_to_spreadsheet(sheet, "movies", "A", movies_files)
    save_files_to_spreadsheet(sheet, "series", "A", series_files)


def save_files_to_spreadsheet(sheet: Any, sheet_name: str, column_letter: str, files: List[Path]) -> None:
    file_names = [
        [file.name]
        for file in files
    ]
    parent_folders = [
        [file.parent.name]
        for file in files
    ]
    write_to_spreadsheet(sheet, f"{sheet_name}!{column_letter}:{column_letter}", parent_folders)
    next_column_letter = get_next_letter(column_letter)
    write_to_spreadsheet(sheet, f"{sheet_name}!{next_column_letter}:{next_column_letter}", file_names)


def get_next_letter(letter: str) -> str:
    # NOTE this is naive implementation and will not work for 'Z' and consequent letters
    return chr(ord(letter[0]) + 1)


def get_movies_files() -> List[Path]:
    movie_files = []
    movie_files.extend(get_video_files_from_folder("/home/davidf/HDD/movies/"))
    movie_files.extend(get_video_files_from_folder("/home/davidf/HDD1/"))
    movie_files.extend(get_video_files_from_folder("/home/davidf/HDD2/movies/"))
    return list(sorted(movie_files, key=lambda p: p.name.lower()))


def get_series_files() -> List[Path]:
    series_files = []
    series_files.extend(get_video_files_from_folder("/home/davidf/HDD2/series/"))
    return series_files


if __name__ == "__main__":
    main()
