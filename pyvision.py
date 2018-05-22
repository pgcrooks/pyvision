#!/usr/bin/env python3

import argparse
import io
import os
import re
import requests

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types


def download_file(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename


def get_string_from_screen(placeholder, input):
    """
    Finds a string by placeholder on an image and returns it.
    Example:
      IP address: <bit_we_want>
    """
    return re.search('{}: (.*)'.format(placeholder), input).group(1)


def main(image_path):
    """
    Main method.
    """

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # If the image path is a URL, get it
    if not os.path.isfile(image_path):
        file_name = download_file(image_path)
    else:
        file_name = os.path.join(os.path.dirname(__file__), image_path)

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.document_text_detection(image=image)
    screen_text = response.text_annotations[0].description
    print('Found:')
    print(screen_text)

    ip_address = get_string_from_screen('IP address', screen_text)
    serial_number = get_string_from_screen('Serial number', screen_text)
    hostname = get_string_from_screen('Hostname', screen_text)
    print('IP: {}'.format(ip_address))
    print('Hostname: {}'.format(hostname))
    print('Serial: {}'.format(serial_number))


if __name__ == "__main__":
    # Execute only if run as a script

    parser = argparse.ArgumentParser(description='Parse text out of images')
    parser.add_argument('-i', '--image', required=True, help="Image file or URL")
    args = parser.parse_args()

    try:
        main(args.image)
    except Exception as e:
        print(e)
