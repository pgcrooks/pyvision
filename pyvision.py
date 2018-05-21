#!/usr/bin/env python3

import io
import os
import re

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types


def get_string_from_screen(placeholder, input):
    """
    Foo
    """
    return re.search('{}: (.*)'.format(placeholder), input).group(1)


def main():
    """
    Main method.
    """

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # The name of the image file to annotate
    file_name = os.path.join(
        os.path.dirname(__file__),
        '/home/pcrooks/Pictures/admin.png')

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.document_text_detection(image=image)
    admin_text = response.text_annotations[0].description
    print('Found:')
    print(admin_text)

    ip_address = get_string_from_screen('IP address', admin_text)
    serial_number = get_string_from_screen('Serial number', admin_text)
    hostname = get_string_from_screen('Hostname', admin_text)
    print('IP: {}'.format(ip_address))
    print('Hostname: {}'.format(hostname))
    print('Serial: {}'.format(serial_number))


if __name__ == "__main__":
    # Execute only if run as a script
    try:
        main()
    except Exception as e:
        print(e)
