import logging
from os import makedirs, path

from services import PPTXHandler

DATA_DIR = path.join(path.dirname(path.abspath(__file__)), "data")
OUTPUT_DIR = path.join(path.dirname(path.abspath(__file__)), "output")

logging.basicConfig(
    format="%(levelname)s %(asctime)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def main():
    if not path.exists(OUTPUT_DIR):
        makedirs(OUTPUT_DIR)
    filepath = path.join(DATA_DIR, "Networking.pptx")
    if not path.isfile(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    logger.info(f"Processing file. This may take a while...")

    pptx_handler = PPTXHandler(data_dir=DATA_DIR, output_dir=OUTPUT_DIR)
    pptx_handler.extract_images_and_translate_text(filepath)

    logger.info(f"All done! Result has been saved to {filepath}")


if __name__ == "__main__":
    main()
