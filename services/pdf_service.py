import io
from os import path
from typing import Dict

import fitz
from fitz import sRGB_to_rgb
from fitz.utils import (
    get_image_info,
    get_image_rects,
    get_text,
    insert_htmlbox,
    insert_image,
)
from fitz.utils import new_page as create_new_page
from PIL import Image

from utils.helper import prepare_output_dir


class PDFExtractor:
    def __init__(self, data_dir: str, output_dir: str):
        self.data_dir = data_dir
        self.output_dir = output_dir

    def extract_images(self, document: fitz.Document, img_dir: str):
        page_image_mapping: Dict[int, list] = {}
        for page in document:
            if not isinstance(page, fitz.Page):
                continue
            image_infos = get_image_info(page, xrefs=True)
            for img_id, image_info in enumerate(image_infos, start=1):
                image = document.extract_image(xref=image_info["xref"])

                image_file = Image.open(io.BytesIO(image["image"]))

                image_file.save(
                    path.join(
                        img_dir, f"page{page.number}_image{img_id}.{image['ext']}"
                    )
                )

                page_image_mapping.setdefault(page.number, []).append(
                    {
                        "page_num": page.number,
                        "xref": image_info["xref"],
                        "image": image,
                    }
                )

        return page_image_mapping

    def extract_formatting_and_convert_uppercase(self, page: fitz.Page):
        page_text = get_text(page, option="dict")
        if not isinstance(page_text, dict):
            return []
        blocks = page_text["blocks"]
        formatted_text = []

        for block in blocks:
            if block["type"] == 0:
                for line in block["lines"]:
                    for span in line["spans"]:
                        formatted_text.append(
                            {
                                "text": span["text"].upper(),
                                "font": span["font"],
                                "size": span["size"],
                                "flags": span["flags"],
                                "color": f'rgb{sRGB_to_rgb(span["color"])}',
                                "bbox": span["bbox"],
                            }
                        )
        return formatted_text

    def extract_convert_export(self, filename: str):
        filepath = path.join(self.data_dir, filename)
        img_dir = prepare_output_dir(filename, self.output_dir)

        document = fitz.open(filepath)
        page_image_mapping = self.extract_images(document, img_dir)

        new_doc = fitz.open()

        for page in document:
            if not isinstance(page, fitz.Page):
                continue

            new_page = create_new_page(
                new_doc, width=page.rect.width, height=page.rect.height
            )

            formatted_text = self.extract_formatting_and_convert_uppercase(page)

            for text_item in formatted_text:
                insert_htmlbox(
                    page=new_page,
                    rect=text_item["bbox"],
                    text=f'<span style="font-family:{text_item["font"]}; font-size:{text_item["size"]}pt; color:{text_item["color"]};">{text_item["text"]}</span>',
                )

            for image in page_image_mapping.get(page.number, []):
                insert_image(
                    new_page,
                    rect=get_image_rects(page, image["xref"])[0],
                    stream=image["image"]["image"],
                )

        filename = filename.split(".")[0]
        new_doc.save(path.join(self.output_dir, filename, f"{filename}_uppercase.pdf"))
