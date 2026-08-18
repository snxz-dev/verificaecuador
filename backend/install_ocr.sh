#!/usr/bin/env bash
# Instala las dependencias del backend + el motor OCR.
# rapidocr se instala con --no-deps para que pip no arrastre
# opencv-python (con GUI) que rompe en imágenes slim.
set -e

pip install -r requirements.txt
pip install --no-deps rapidocr-onnxruntime==1.2.3
