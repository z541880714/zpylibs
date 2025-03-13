import os
from PIL import Image, ImageOps, ImageDraw

SIZE = 1024


def make_circle(image):
    size = (SIZE, SIZE)
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    output = ImageOps.fit(image, size, centering=(0.5, 0.5), method=Image.LANCZOS)
    output.putalpha(mask)
    return output


def process_image(file_path, output_directory):
    try:
        with Image.open(file_path) as img:
            img.thumbnail((SIZE, SIZE), Image.LANCZOS)
            img = img.convert('RGBA')
            img = make_circle(img)
            output_path = os.path.join(output_directory, f'circle_{os.path.basename(file_path)}')
            img.save(output_path, 'PNG', quality=95)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")


def process_images(input_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    for entry in os.scandir(input_directory):
        if entry.is_file() and entry.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            process_image(entry.path, output_directory)


if __name__ == '__main__':
    process_images('res', 'out')
