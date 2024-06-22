import re
from os import listdir, makedirs, path

from services import DocxExtractor, PDFExtractor

DATA_DIR = path.join(path.dirname(path.abspath(__file__)), "data")
OUTPUT_DIR = path.join(path.dirname(path.abspath(__file__)), "output")


def main():
    if not path.exists(OUTPUT_DIR):
        makedirs(OUTPUT_DIR)

    file_pattern = re.compile("mock_file")

    docx_extractor = DocxExtractor(data_dir=DATA_DIR, output_dir=OUTPUT_DIR)
    pdf_extractor = PDFExtractor(data_dir=DATA_DIR, output_dir=OUTPUT_DIR)

    for file in listdir(DATA_DIR):
        if not file_pattern.search(file.split(".")[0]):
            continue

        if file.endswith(".pdf"):
            print(f"Processing PDF file: {file}")
        elif file.endswith(".docx"):
            print(f"Processing DOCX file: {file}")
            docx_extractor.extract_convert_export(file)
        else:
            continue


if __name__ == "__main__":
    main()
