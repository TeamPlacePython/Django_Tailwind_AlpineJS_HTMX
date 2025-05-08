from PIL import Image as PilImage
from io import BytesIO
from django.core.files.base import ContentFile


class ImageResizeMixin:
    IMAGE_RESIZE_MODE = "thumbnail"  # ou 'resize'
    FORCE_LANDSCAPE = False
    TARGET_SIZE = (400, 300)  # défaut paysage

    def resize_image_field(self, image_field):
        if not image_field:
            return

        img = PilImage.open(image_field)
        img = img.convert("RGB")
        width, height = img.size

        if self.FORCE_LANDSCAPE and width <= height:
            raise ValueError("L'image doit être en format paysage")

        if self.IMAGE_RESIZE_MODE == "resize":
            resized = img.resize(self.TARGET_SIZE, PilImage.LANCZOS)
        else:
            resized = img.copy()
            resized.thumbnail(self.TARGET_SIZE, PilImage.LANCZOS)

        buffer = BytesIO()
        resized.save(buffer, format="JPEG", quality=90)
        buffer.seek(0)

        # 🔁 Nouveau nom plus propre, sans chemin
        original_name = image_field.name.split("/")[-1].split(".")[0]
        filename = f"{original_name}_resized.jpg"

        # 🔁 On réassigne à self.image pour s'assurer qu’il est pris en compte
        self.image.save(filename, ContentFile(buffer.read()), save=False)
