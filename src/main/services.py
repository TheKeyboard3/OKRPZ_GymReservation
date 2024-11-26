from PIL import Image, ImageDraw
from random import randint
import os


def get_html_image(image_url, obj, title='', width=50, height=50):
    title_html = ''
    if title != '':
        title_html = f' title="{title}"'
    if not image_url:
        return f'none:({image_url})'

    text = f"""
    <a href="{obj.get_absolute_url()}"{title_html}>
        <img src="{image_url}" width="{width}" height="{height}" />
    </a>"""
    return text


def get_html_button(url, title='Button'):
    return f'<a class="button" href="{url}">{title}</a>'


def create_image(path, width=600, height=600):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)

        color = (randint(0, 255),
                 randint(0, 255),
                 randint(0, 255))
        image = Image.new('RGB', (width, height), color=color)
        draw = ImageDraw.Draw(image)

        for _ in range(10):
            start = (randint(0, image.width), randint(0, image.height))
            end = (randint(0, image.width), randint(0, image.height))
            draw.line((start, end), fill='white')

        for _ in range(10):
            x1 = randint(0, image.width)
            y1 = randint(0, image.height)
            x2 = randint(x1, image.width)
            y2 = randint(y1, image.height)
            draw.ellipse(((x1, y1), (x2, y2)), outline='white')

        image.save(path)

    except Exception as e:
        print(e)
