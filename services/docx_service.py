import json
from os import makedirs, path
from typing import Union

import docx2txt
from docx import Document
from docx.document import Document as DocumentObject
from docx.table import _Cell


class DocxExtractor:
    def __init__(self, data_dir: str, output_dir: str):
        self.data_dir = data_dir
        self.output_dir = output_dir

    def extract_images(self, filename: str):
        img_dir = path.join(
            self.output_dir,
            filename.split(".")[0],
            "images",
        )
        if not path.exists(img_dir):
            makedirs(img_dir)
        docx2txt.process(path.join(self.data_dir, filename), img_dir)

    def extract_formatting_and_convert_uppercase(
        self, document: Union[DocumentObject, _Cell]
    ):
        paragraphs = []
        for para in document.paragraphs:
            if not para.text or para.text.isspace():
                continue
            para_info = {"paragraph": para.text, "runs": []}
            for run in para.runs:
                font = run.font
                para_info["runs"].append(
                    {
                        "content": run.text,
                        "font": font.name,
                        "font_size": font.size.pt if font.size else None,
                        "color": font.color.rgb if font.color else None,
                        "bold": font.bold,
                        "italic": font.italic,
                        "underline": font.underline,
                    }
                )
                run.text = run.text.upper()

            paragraphs.append(para_info)

        for table in document.tables:
            for row in table.rows:
                for cell in row.cells:
                    paragraphs.extend(
                        self.extract_formatting_and_convert_uppercase(cell)
                    )

        return paragraphs

    def extract_convert_export(self, filename: str):
        self.extract_images(filename)

        document = Document(path.join(self.data_dir, filename))
        paragraphs = []

        paragraphs.extend(self.extract_formatting_and_convert_uppercase(document))

        with open(
            path.join(
                self.output_dir,
                filename.split(".")[0],
                filename.split(".")[0] + ".json",
            ),
            "w",
        ) as f:
            json.dump(paragraphs, f, indent=2)

        document.save(
            path.join(
                self.output_dir,
                filename.split(".")[0],
                filename.split(".")[0] + "_uppercase.docx",
            )
        )

        return paragraphs
