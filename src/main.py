import argparse
import logging

from dotenv import load_dotenv


def parse_args():
    parser = argparse.ArgumentParser(description='Main driver function for APT')
    parser.add_argument('--config', '-c', help='Path to the config file')

    args = parser.parse_args()

    if args.config is None:
        parser.print_usage()
        exit()

    return args

def configure_logging():
    """Sets up logging to have sensible format and to output to console."""

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )

    # suppress tonnes of post request clogging up logging
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpx").propagate = False
    logging.getLogger("azure").setLevel(logging.WARNING)
    logging.getLogger("azure").propagate = False


def main():

    # admin
    configure_logging()
    load_dotenv()

    logging.info('Testing...')






if __name__ == "__main__":
    main()
