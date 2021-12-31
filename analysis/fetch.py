"""Fetches large raw data files."""

import requests

from analysis import paths

# Adapted from an answer by @turdus-merula on Stack Overflow: https://stackoverflow.com/a/39225272


def __get_confirm_token(response):
    """Gets confirmation token from Google Drive to bypass large file
    warning.
    """

    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            return value

    return None


def __save_response_content(response, destination):
    """Saves download to file."""

    chunk_size = 32768

    with open(destination, "wb") as dest_file:
        for chunk in response.iter_content(chunk_size):
            if chunk:                     # Filter out keep-alive new chunks
                dest_file.write(chunk)


def __download_gdrive(drive_id, save_to):
    """Downloads a file from Google Drive using its ID."""

    url = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(url, params={"id": drive_id}, stream=True)
    token = __get_confirm_token(response)

    if token:
        params = {"id":drive_id, "confirm":token }
        response = session.get(url, params=params, stream=True)

    __save_response_content(response, save_to)


def fetch_raw(date: str = None):
    """Fetches large raw data files."""

    with open(paths.Tables.table_ref_path(date), "r", encoding="utf-8") as file:
        drive_id = file.read().strip()
        __download_gdrive(drive_id, paths.Tables.table_txt_path())
