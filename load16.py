import io

import numpy as np
from PIL import Image
from Quartz import (
    NSURL,
    CGColorSpaceCreateWithName,
    CIContext,
    CIImage,
    kCGColorSpaceSRGB,
)


def load_image_macOS_coreimage_16bit(path):
    url = NSURL.fileURLWithPath_(str(path))
    ci_image = CIImage.imageWithContentsOfURL_(url)
    if ci_image is None:
        raise ValueError(f"Failed to load CIImage from {path}")

    ctx = CIContext.context()
    color_space = CGColorSpaceCreateWithName(kCGColorSpaceSRGB)

    # Render as 16-bit TIFF explicitly
    rendered = ctx.TIFFRepresentationOfImage_format_colorSpace_options_(
        ci_image, 0, color_space, None
    )

    if rendered is None:
        raise ValueError("Failed to render CIImage to TIFF.")

    # NSData to Python bytes
    rendered_bytes = rendered.bytes().tobytes()

    # Load TIFF into PIL Image (preserves 16-bit depth)
    pil_image = Image.open(io.BytesIO(rendered_bytes))

    # Ensure it's in a known 16-bit RGB format (e.g., "I;16", "RGB;16")
    pil_image = pil_image.convert("RGB")

    # Convert PIL Image to numpy array (dtype=uint16)
    image_array = np.array(pil_image, dtype=np.uint16)

    return image_array


if __name__ == "__main__":
    import sys

    path = sys.argv[1]
    img = load_image_macOS_coreimage_16bit(path)
    print(img.shape, img.dtype)

    # Save as 16-bit PNG explicitly (for previewing)
    Image.fromarray(img, mode="I;16").save("output_16bit.png")
