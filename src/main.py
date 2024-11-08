import argparse
import logging
import os
import uuid

from dotenv import dotenv_values

from azure_handlers import AzureBlobHandler
from io_functions import load_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Main driver function for APT')
    parser.add_argument('--config', '-c', help='Path to the config file')
    parser.add_argument('--audio_dir', '-a', help='Path to the audio directory')

    args = parser.parse_args()

    if args.config is None or args.audio_dir is None:
        parser.print_usage()
        exit()

    return args

def configure_logging() -> logging.Logger:
    """Sets up a useful logger."""

    # suppress tonnes of post request clogging up logging
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpx").propagate = False
    logging.getLogger("azure").setLevel(logging.WARNING)
    logging.getLogger("azure").propagate = False

    # create project-specific logger
    logger = logging.getLogger('apt')
    logger.setLevel(logging.DEBUG)

    # set up logger to output to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # set up console to output to log file
    # TO DO - add audio filename as logfile name
    file_handler = logging.FileHandler(f'{os.getcwd()}/logs/apt.log',
                                      mode = 'w')
    file_handler.setLevel(logging.DEBUG)

    # set up log formatting
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # add specific handlers to the main logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def main():

    logger = configure_logging()
    args = parse_args()

    request_id = str(uuid.uuid4())

    # load in config values from both .env and config json given
    config = dotenv_values(".env") | load_json(args.config)

    logger.info('Beginning APT: Request ID {request_id}...')

    blob_handler = AzureBlobHandler(audio_dir=args.audio_dir,
                                    blob_key=config['AZ_BLOB_KEY'],
                                    blob_container_link=config['AZ_BLOB_CONTAINER_LINK'],
                                    request_id=request_id)


    container_client = blob_handler.upload_to_blob()

    # TO DO - transcription, assigning speakers etc.

    # at some point after transcription, delete the container that had the audio in it
    # container_client.delete_container()



if __name__ == "__main__":
    main()
