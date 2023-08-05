from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt
from PyQt5.QtGui import QPixmap, QImage
import io


class MyImageOperations:

    def __init__(self, file_path=None):
        self.file_path = file_path

    # Меняет размер
    def resize_img(self, width, height):
        image = Image.open(self.file_path)

        if height == 'auto':
            height = int(image.height / (image.width / width))

        image = image.resize((width, height), Image.ANTIALIAS)

        return image

    def pix_map_image(self, image):
        img_tmp = ImageQt(image.convert('RGBA'))
        pix_map = QPixmap.fromImage(img_tmp)
        return pix_map

    def from_pil_to_bytes(self, image):
        # Будем пихать из PIL в байты
        stream = io.BytesIO()
        image.save(stream, format="png")
        imagebytes = stream.getvalue()
        return imagebytes

    # Достаёт картинку из байт
    def image_from_byte(self, image_byte):
        image = QImage.fromData(image_byte)
        return QPixmap.fromImage(image)

