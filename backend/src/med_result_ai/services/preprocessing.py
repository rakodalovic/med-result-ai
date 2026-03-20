"""Image preprocessing for improved OCR accuracy."""

import logging
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageOps

logger = logging.getLogger(__name__)


def _fix_orientation(image: Image.Image) -> Image.Image:
    """Apply EXIF orientation to the image pixels."""
    return ImageOps.exif_transpose(image)


def _to_grayscale(image: np.ndarray) -> np.ndarray:
    """Convert a BGR image to grayscale."""
    if len(image.shape) == 3:  # noqa: PLR2004
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image


def _denoise(image: np.ndarray) -> np.ndarray:
    """Remove noise while preserving edges."""
    return cv2.fastNlMeansDenoising(image, h=10)


def _enhance_contrast(image: np.ndarray) -> np.ndarray:
    """Enhance local contrast using CLAHE."""
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(image)


def _threshold(image: np.ndarray) -> np.ndarray:
    """Apply adaptive thresholding for crisp text."""
    return cv2.adaptiveThreshold(
        image,
        maxValue=255,
        adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        thresholdType=cv2.THRESH_BINARY,
        blockSize=11,
        C=2,
    )


def preprocess_image(
    image_path: str,
    *,
    save_debug: bool = False,
) -> np.ndarray:
    """Run the full preprocessing pipeline on a blood test image.

    Steps: fix EXIF orientation -> grayscale -> denoise ->
    CLAHE contrast -> adaptive threshold.

    Args:
        image_path: Path to the source image.
        save_debug: If True, save the result next to the original.

    Returns:
        Preprocessed image as a numpy array.

    Raises:
        FileNotFoundError: If the image does not exist.
    """
    path = Path(image_path)
    if not path.exists():
        msg = f"image not found: {image_path}"
        raise FileNotFoundError(msg)

    pil_image = Image.open(path)
    pil_image = _fix_orientation(pil_image)

    image = np.array(pil_image)
    image = _to_grayscale(image)
    image = _denoise(image)
    image = _enhance_contrast(image)
    image = _threshold(image)

    if save_debug:
        debug_path = path.with_stem(f"{path.stem}_preprocessed")
        cv2.imwrite(str(debug_path), image)
        logger.info("saved debug image to %s", debug_path)

    return image
