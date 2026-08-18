"""OCR para verificar imágenes: extrae el texto de la imagen.

Usa RapidOCR (ONNX, sin servicios externos). El modelo se carga la primera
vez que se usa (inicialización perezosa) para no frenar el arranque de la API.

Optimizado para el plan gratuito de Render (512 MB RAM): onnxruntime se limita
a 1 hilo (por defecto usa todos los cores del host y agota la memoria) y los
lotes de reconocimiento se reducen.
"""

import logging

logger = logging.getLogger(__name__)

_ocr = None


def _patch_onnxruntime_threads() -> None:
    """Fuerza onnxruntime a 1 hilo por sesión para reducir el consumo de RAM.

    RapidOCR crea sesiones con SessionOptions() por defecto, que usa todos los
    cores del host → thread pools enormes × 3 modelos → >512 MB (mata el
    proceso en el plan gratis de Render). Parcheamos la creación de sesiones.
    """
    try:
        from rapidocr_onnxruntime import utils as rapidocr_utils
        import onnxruntime as ort

        original = rapidocr_utils.InferenceSession

        def limited_session(*args, **kwargs):
            so = ort.SessionOptions()
            so.log_severity_level = 4
            so.enable_cpu_mem_arena = False
            so.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
            so.intra_op_num_threads = 1
            so.inter_op_num_threads = 1
            kwargs["sess_options"] = so
            return original(*args, **kwargs)

        rapidocr_utils.InferenceSession = limited_session
    except Exception as e:
        logger.warning("No se pudo limitar hilos de onnxruntime: %s", e)


def _get_ocr():
    global _ocr
    if _ocr is None:
        from rapidocr_onnxruntime import RapidOCR

        _patch_onnxruntime_threads()
        import cv2

        cv2.setNumThreads(1)  # menos pools de hilos de OpenCV
        # model_path="" deja que rapidocr use los modelos por defecto
        _ocr = RapidOCR(
            use_angle_cls=False,  # capturas normalmente verticales: ahorra un modelo
            det_model_path="",
            det_limit_side_len=480,
            det_max_candidates=500,
            det_use_dilation=False,
            rec_model_path="",
            rec_batch_num=1,
            cls_model_path="",
            cls_batch_num=1,
        )
        logger.info("Modelo OCR cargado (memoria optimizada)")
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
