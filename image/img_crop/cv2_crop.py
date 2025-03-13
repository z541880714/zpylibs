import os
import cv2
import numpy as np

SIZE = 1024


def make_circle(image):
    size = (SIZE, SIZE)
    mask = np.zeros((SIZE, SIZE), dtype=np.uint8)
    cv2.circle(mask, (SIZE // 2, SIZE // 2), SIZE // 2, 255, -1)
    output = cv2.resize(image, size)
    output[:, :, 3] = mask
    output = cv2.GaussianBlur(output, (5, 5), 0)  # Apply Gaussian blur to reduce aliasing
    return output


def resize_and_crop(image, size):
    h, w = image.shape[:2]
    aspect_ratio = w / h

    new_h = int(min(SIZE, SIZE / aspect_ratio))
    new_w = int(aspect_ratio * new_h)
    resized_image = cv2.resize(image, (new_w, new_h))
    new_size = min(new_h, new_w)
    top = (new_h - new_size) // 2
    left = (new_w - new_size) // 2
    result = resized_image[top:top + new_size, left:left + new_size]
    return result


def process_image(file_path, output_directory):
    try:
        img = cv2.imread(file_path)
        if img is None:
            raise ValueError(f"Image not found or unable to read: {file_path}")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        img = resize_and_crop(img, SIZE)
        img = make_circle(img)
        output_path = os.path.join(output_directory, f'circle_{os.path.basename(file_path)}.png')
        cv2.imwrite(output_path, img)
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
