import io

import numpy as np
from PIL import Image
from Quartz import (
    NSURL,
    CGColorSpaceCreateWithName,
    CIContext,
    CIImage,
    NSBitmapImageRep,
    NSPNGFileType,
    kCGColorSpaceSRGB,
)


def load_image_macOS_coreimage(path):
    url = NSURL.fileURLWithPath_(str(path))
    ci_image = CIImage.imageWithContentsOfURL_(url)
    if ci_image is None:
        raise ValueError(f"Failed to load CIImage from {path}")

    ctx = CIContext.context()
    color_space = CGColorSpaceCreateWithName(kCGColorSpaceSRGB)

    # Render CIImage to a bitmap
    extent = ci_image.extent()
    width = int(extent.size.width)
    height = int(extent.size.height)

    # Render to RGBA8 format explicitly
    bitmap = ctx.createCGImage_fromRect_(ci_image, extent)
    if bitmap is None:
        raise ValueError("Failed to create bitmap image from CIImage")

    # Create NSBitmapImageRep from CGImage
    bitmap_rep = NSBitmapImageRep.alloc().initWithCGImage_(bitmap)

    # Get PNG representation from bitmap
    png_data = bitmap_rep.representationUsingType_properties_(NSPNGFileType, None)
    if png_data is None:
        raise ValueError("Failed to convert bitmap image to PNG format")

    # NSData to bytes
    png_bytes = png_data.bytes().tobytes()

    # Read PNG into PIL Image
    pil_image = Image.open(io.BytesIO(png_bytes))

    # Convert PIL Image to numpy array
    image_array = np.array(pil_image)

    return image_array


if __name__ == "__main__":
    import sys

    path = sys.argv[1]
    img = load_image_macOS_coreimage(path)
    img = np.rot90(img, k=3)
    print(img.shape, img.dtype)
    Image.fromarray(img).save(path.replace(".DNG", "_raw.PNG"))
