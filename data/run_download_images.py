"""run_download_images.py

Note that we provide the original URLs.
"""

import argparse

parser = argparse.ArgumentParser(description='Download the Incident Dataset images.')
parser.add_argument('--images_folder',
                    type=str,
                    default="images",
                    help='Dataset to download images for.')
parser.add_argument('--dataset_name',
                    type=str,
                    default="eccv_test.json",
                    help='Dataset to download images for.')


def main():
    args = parser.parse_args()
    # TODO: finish this script
    raise NotImplementedError("This script is not complete.")


if __name__ == "__main__":
    main()
