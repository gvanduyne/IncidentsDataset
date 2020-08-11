"""run_download_json_files.py

Helper code comes from the following URLs:
    - https://github.com/nsadawi/Download-Large-File-From-Google-Drive-Using-Python/blob/master/Download-Large-File-from-Google-Drive.ipynb
    - https://stackoverflow.com/a/39225039
"""
import requests




def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)


# TODO(ethan): change this to have 4 unique names and ids
dataset_name_to_file_id = {
    "eccv_train.json": "1FVS89WN_o4GU_sqgwlKk-thyR2zQM45Y",
    "eccv_train.json": "1FVS89WN_o4GU_sqgwlKk-thyR2zQM45Y",
    "eccv_train.json": "1FVS89WN_o4GU_sqgwlKk-thyR2zQM45Y",
    "eccv_train.json": "1FVS89WN_o4GU_sqgwlKk-thyR2zQM45Y"
}

if __name__ == "__main__":
    # TODO(ethan): finish this script
    # train
    file_id = '0B1fGSuBXAh1IeEpzajRISkNHckU'
    destination = '/home/myusername/work/myfile.ext'
    download_file_from_google_drive(file_id, destination)

    # train
    file_id = '0B1fGSuBXAh1IeEpzajRISkNHckU'
    destination = '/home/myusername/work/myfile.ext'
    download_file_from_google_drive(file_id, destination)

    file_id = '0B1fGSuBXAh1IeEpzajRISkNHckU'
    destination = '/home/myusername/work/myfile.ext'
    download_file_from_google_drive(file_id, destination)

    file_id = '0B1fGSuBXAh1IeEpzajRISkNHckU'
    destination = '/home/myusername/work/myfile.ext'
    download_file_from_google_drive(file_id, destination)
