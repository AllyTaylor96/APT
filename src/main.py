import argparse
import logging
import os
import uuid

from io_functions import load_json
from transcribers import WhisperTranscriber


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Main driver function for APT')
    parser.add_argument('--config', '-c', help='Path to the config file')
    parser.add_argument('--audio_dir', '-a', help='Path to the audio directory')
    parser.add_argument('--output_dir', '-o', help='Path to the output directory')

    args = parser.parse_args()

    if args.config is None or args.audio_dir is None or args.output_dir is None:
        parser.print_usage()
        exit()

    return args

def configure_logging(request_id: str) -> logging.Logger:
    """Sets up a useful logger."""

    # create project-specific logger
    logger = logging.getLogger('apt')
    logger.setLevel(logging.DEBUG)

    # set up logger to output to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # set up console to output to log file
    file_handler = logging.FileHandler(f'{os.getcwd()}/logs/{request_id}.log',
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

    request_id = str(uuid.uuid4())

    logger = configure_logging(request_id)
    args = parse_args()

    config = load_json(args.config)
    requested_model = config['transcription']['whisperModel']

    logger.info(f'AnotherPodcastTranscriber - Request ID: {request_id}...')

    logger.info(f'Whisper - Model requested: {requested_model}...')
    transcription_handler = WhisperTranscriber(
        audio_dir=args.audio_dir,
        output_dir=args.output_dir,
        request_id=request_id,
        requested_model=requested_model
    )
    logger.info(f'Whisper - Model instantiated...')

    transcription_handler.run_transcription()

if __name__ == "__main__":
    main()
