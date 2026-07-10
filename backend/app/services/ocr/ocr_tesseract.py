from pathlib import Path

import pytesseract
from PIL import Image

from app.services.ocr.base_ocr import BaseOCR


class TesseractOCR(BaseOCR):
    def extract_text(self, file_path: str) -> str:
        path = Path(file_path)
        extension = path.suffix.lower()

        if extension in [".png", ".jpg", ".jpeg"]:
            return self._extract_from_image(path)

        if extension == ".pdf":
            return self._extract_from_pdf(path)

        raise ValueError(f"Unsupported file extension for OCR: {extension}")

    def _extract_from_image(self, path: Path) -> str:
        image = Image.open(path)
        text = pytesseract.image_to_string(image)
        return text.strip()

    def _extract_from_pdf(self, path: Path) -> str:
        raise NotImplementedError(
            "PDF OCR is not implemented yet. We will add it in the next step."
        )