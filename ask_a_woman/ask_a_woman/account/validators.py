import os

import cloudinary.api
from django.core.exceptions import ValidationError
from PIL import Image, ImageOps
from io import BytesIO
from django.core.files.base import ContentFile


def check_valid_size(value):
    max_size_kb = 5120  # 5 MB

    # Handle CloudinaryResource
    if hasattr(value, 'public_id'):  # Check if the value is a CloudinaryResource
        try:
            resource_info = cloudinary.api.resource(value.public_id)
            size_in_bytes = resource_info.get('bytes', 0)  # Get size in bytes
            size_in_kb = size_in_bytes / 1024
        except cloudinary.exceptions.Error as e:
            raise ValidationError(f"Error fetching image metadata from Cloudinary: {e}")
    else:
        # Handle local or in-memory file uploads
        try:
            size_in_kb = value.size / 1024
        except AttributeError:
            raise ValidationError("Unable to determine the file size.")

    if size_in_kb > max_size_kb:
        raise ValidationError(f"Image file size should not exceed {max_size_kb} KB.")


def validate_and_crop_image(image):
    max_width, max_height = 480, 480  # Desired dimensions

    # Check if the uploaded image is from Cloudinary
    if hasattr(image, 'build_url'):
        # This is a CloudinaryResource. Cloudinary handles transformations directly.
        return

    # For local or in-memory files (during testing)
    try:
        from PIL import Image, ImageOps
        from io import BytesIO

        img = Image.open(image)
        img = ImageOps.exif_transpose(img)

        width, height = img.size
        img_format = img.format or image.content_type.split('/')[-1].upper()

        if width > max_width or height > max_height:
            img = img.resize((max_width, max_height), Image.Resampling.LANCZOS)
            output = BytesIO()
            img.save(output, format=img_format)
            image.file = ContentFile(output.getvalue())
            image.size = image.file.size  # Update the image size
    except Exception as e:
        raise ValidationError(f"Error processing the image: {e}")