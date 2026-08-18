"""OCR para verificar imágenes: extrae el texto de la imagen.

Usa RapidOCR (ONNX, sin servicios externos). El modelo se carga la primera
vez que se usa (inicialización perezosa) para no frenar el arranque de la API.
"""

import logging

logger = logging.getLogger(__name__)

_ocr = None


def _get_ocr():
    global _ocr
    if _ocr is None:
        from rapidocr_onnxruntime import RapidOCR

        _ocr = RapidOCR()
        logger.info("Modelo OCR cargado")
    return _ocr


def extract_text(image_bytes: bytes) -> str:
    """Extrae el texto de una imagen (bytes) y lo devuelve como string."""
    import cv2
    import numpy as np

    arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        logger.warning("No se pudo decodificar la imagen")
        return ""

    result, _ = _get_ocr()(img)
    if not result:
        return ""

    lines = [str(item[1]).strip() for item in result if item and item[1]]
    return " ".join(lines).strip()
