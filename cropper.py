from PIL import Image
import os
import math

def crop_image_with_padding(
    image_path,
    output_folder,
    crop_width=None,
    crop_height=None,
    rows=None,
    cols=None,
    grid=False,
    fill_color=(255, 255, 255, 0)  # transparent if RGBA; use (255, 255, 255) for white RGB
):
    Image.MAX_IMAGE_PIXELS = None
    image = Image.open(image_path)
    img_width, img_height = image.size
    mode = image.mode

    os.makedirs(output_folder, exist_ok=True)

    # Fill in missing crop info
    if crop_width and crop_height:
        cols = math.ceil(img_width / crop_width)
        rows = math.ceil(img_height / crop_height)
    elif rows and cols:
        crop_width = math.ceil(img_width / cols)
        crop_height = math.ceil(img_height / rows)
    elif cols and grid:
        crop_width = math.ceil(img_width / cols)
        rows = math.ceil(img_height / 5000)
    elif rows:
        crop_height = math.ceil(img_height / rows)
        crop_width = img_width
        cols = 1
    elif cols:
        crop_width = math.ceil(img_width / cols)
        crop_height = img_height
        rows = 1
    else:
        raise ValueError("Provide (width and height) or (rows and/or cols)")

    print(f"Cropping into {rows} rows and {cols} cols of {crop_width}x{crop_height}px")

    for row in range(rows):
        for col in range(cols):
            left = col * crop_width
            upper = row * crop_height
            right = min(left + crop_width, img_width)
            lower = min(upper + crop_height, img_height)

            # Actual cropped region
            crop_box = (left, upper, right, lower)
            cropped = image.crop(crop_box)

            # Pad if not full size
            if cropped.size != (crop_width, crop_height):
                # Create blank canvas
                background = Image.new(
                    mode if 'A' in mode else 'RGBA', (crop_width, crop_height), fill_color
                )
                background.paste(cropped, (0, 0))
                cropped = background

            filename = f"{output_folder}/crop_r{row}_c{col}.png"
            cropped.save(filename)
            print(f"Saved: {filename}")

# ======= Usage Example =======
if __name__ == "__main__":
    image_path = "test.png"
    output_folder = "output_test"
    crop_image_with_padding(
        image_path,
        output_folder,
        crop_width=4000,
        crop_height=5000,
        fill_color=(255, 255, 255, 0)  # transparent padding
    )
