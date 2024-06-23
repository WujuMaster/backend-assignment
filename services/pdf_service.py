import io
import json
from os import path
from typing import Dict

import fitz
from fitz import find_tables, sRGB_to_rgb
from fitz.utils import (
    draw_rect,
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
        """Extract images from the PDF document

        Args:
            document (fitz.Document): PDF document object
            img_dir (str): Directory to save the images

        Returns:
            dict: Page number and image mapping
        """
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

    def extract_spans_formatting(self, page: fitz.Page):
        """Extract text spans formatting information from the page

        Args:
            page (fitz.Page): Page object

        Returns:
            list: List of formatting info dictionaries
        """
        page_text = get_text(page, option="dict")
        if not isinstance(page_text, dict):
            return []
        blocks = page_text["blocks"]
        span_list = []

        for block in blocks:
            # Text block
            if block["type"] == 0:
                for line in block["lines"]:
                    for span in line["spans"]:
                        if not span["text"].strip():
                            continue
                        span_list.append(
                            {
                                "content": span["text"].strip(),
                                "font": span["font"],
                                "font_size": span["size"],
                                "color": f'rgb{sRGB_to_rgb(span["color"])}',
                                "bold": bool(span["flags"] & 2**4),
                                "italic": bool(span["flags"] & 2**1),
                                "bbox": span["bbox"],
                            }
                        )
        return span_list

    def generate_html_text(self, span: dict):
        """Generate HTML text from span dict.

        Args:
            span (dict): Span dictionary

        Returns:
            str: HTML text
        """
        text_style = f"font-family:{span['font']}; font-size:{span['font_size']}pt; color:{span['color']};"
        if span["italic"]:
            text_style += " font-style:italic;"
        if span["bold"]:
            text_style += " font-weight:bold;"

        return f'<span style="{text_style}">{span["content"].upper()}</span>'

    def extract_convert_export(self, filename: str):
        """Main method to extract, convert and export the PDF file"""
        filepath = path.join(self.data_dir, filename)
        img_dir = prepare_output_dir(filename, self.output_dir)

        document = fitz.open(filepath)

        # Extract images
        page_image_mapping = self.extract_images(document, img_dir)

        new_doc = fitz.open()
        formatting_info = []
        for page in document:
            if not isinstance(page, fitz.Page):
                continue

            new_page = create_new_page(
                new_doc, width=page.rect.width, height=page.rect.height
            )

            # Extract formatting info
            span_list = self.extract_spans_formatting(page)
            formatting_info.extend(span_list)

            # Insert text boxes
            for span_item in span_list:
                insert_htmlbox(
                    page=new_page,
                    rect=span_item["bbox"],
                    text=self.generate_html_text(span_item),
                )

            # Insert images
            for image in page_image_mapping.get(page.number, []):
                insert_image(
                    new_page,
                    rect=get_image_rects(page, image["xref"])[0],
                    stream=image["image"]["image"],
                )

            # Insert table lines
            tabs = find_tables(page)
            for tab in tabs:
                for cell in tab.cells:
                    if not cell:
                        continue
                    draw_rect(new_page, cell)
                draw_rect(new_page, tab.bbox)

        filename = filename.split(".")[0]
        # Export the extracted formatting data
        with open(path.join(self.output_dir, filename, f"{filename}.json"), "w") as f:
            json.dump(formatting_info, f, indent=2)

        # Export the converted PDF file
        new_doc.save(path.join(self.output_dir, filename, f"{filename}_uppercase.pdf"))

        return formatting_info
