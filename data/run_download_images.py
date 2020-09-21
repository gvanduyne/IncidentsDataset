"""run_download_images.py

Note that we provide the original URLs.
"""

import argparse
import requests
import json
import os
import sys
import pprint
from tqdm import tqdm
import shutil
import errno
from multiprocessing import Pool

DATASET_NAMES = ["eccv_train.json",
                 "eccv_val.json",
                 "multi_label_train.json",
                 "multi_label_val.json"]

parser = argparse.ArgumentParser(description='Download the Incident Dataset images.')
parser.add_argument('--show_json',
                    action="store_true",
                    help='Show what the .json data looks like.')
parser.add_argument('--output_dir',
                    type=str,
                    default="images",
                    help='Where to download the data.')
parser.add_argument('--dataset_name',
                    type=str,
                    default="eccv_val.json",
                    help='Dataset to download images for.')
parser.add_argument('--categories',
                    type=str,
                    default=None,
                    help='Comma separated list of categories.')
parser.add_argument('--max_num_images',
                    type=int,
                    default=None,
                    help='Maximum number of images to download.')


def get_download_data_of_categories(dataset_data, categories=None):
    """Get the data to attempt downloading with.
    TODO: add more support to filter by incidents and places

    Args:
        categories (list): If None, then obtain all URLs.

    Returns:
        dict: key = image_name, value = URL
    """
    download_data = {}  # url -> image filename
    for image_name, image_data in tqdm(dataset_data.items()):
        incidents = image_data["incidents"]
        places = image_data["incidents"]
        url = image_data["url"]
        if categories is None:
            download_data[image_name] = image_data
            continue
        # filter by categories
        for incident, value in incidents.items():
            if incident in categories and value == 1:  # recall that 1 means positive label
                download_data[image_name] = image_data
                continue

    return download_data


def make_dirs(filename):
    # make directories if needed
    # https://stackoverflow.com/questions/12517451/automatically-creating-directories-with-file-output
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def download_image(image_filename, image_url):
    # returns True is successful, False otherwise
    # https://towardsdatascience.com/how-to-download-an-image-using-python-38a75cfa21c
    success = False

    # wrapped in try/except since there are many exceptions that could occur, if something goes wrong
    try:
        # Open the url image, set stream to True, this will return the stream content.
        # And no redirects to avoid errors:
        # https://stackoverflow.com/questions/23651947/python-requests-requests-exceptions-toomanyredirects-exceeded-30-redirects
        r = requests.get(image_url, stream=True, allow_redirects=False, timeout=10)

        # Check if the image was retrieved successfully
        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True

            # make directories if folders don't exist yet
            make_dirs(image_filename)

            # Open a local file with wb ( write binary ) permission.
            with open(image_filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

            success = True
    except KeyboardInterrupt:
        sys.exit()
    except:
        pass
    return success


def download_images(output_dir, download_data, max_num_images=None):
    # iterate over data and attempt downloads
    downloaded_data = {}  # keep track of data that downloaded correctly
    print("Potentially downloading {} images.".format(len(download_data)))
    success_count = 0
    for image_name, image_data in tqdm(download_data.items()):
        image_url = image_data["url"]
        image_filename = os.path.join(output_dir, image_name)
        success = download_image(image_filename, image_url)
        if success:
            downloaded_data[image_name] = image_data
            success_count += 1
        if max_num_images is not None and success_count >= max_num_images:
            break
    return downloaded_data


def main():
    args = parser.parse_args()

    # load dataset from dataset_name arg
    assert os.path.exists(args.dataset_name)
    with open(args.dataset_name, "r") as f:
        dataset_data = json.load(f)

    # show what the JSON format looks like and exist
    if args.show_json:
        print("Showing examples inside JSON file: {}".format(args.dataset_name))
        for key, value in list(dataset_data.items())[:5]:
            print("Key: {}".format(key))
            print("Value:")
            pprint.pprint(value)
            print("-" * 50)
        print("Exiting.")
        sys.exit()

    # obtain dictionary mapping category
    categories = args.categories
    if categories is not None:
        categories = categories.split(",")
    print("Filtering by categories: {}".format(categories))
    download_data = get_download_data_of_categories(dataset_data,
                                                    categories=categories)

    # now download the images at the URLs
    # downloaded_data is in the same format as dataset_data
    # write to file
    downloaded_data = download_images(args.output_dir, download_data, max_num_images=args.max_num_images)
    with open("downloaded_data.json", 'w') as outfile:
        json.dump(downloaded_data, outfile)


if __name__ == "__main__":
    main()
