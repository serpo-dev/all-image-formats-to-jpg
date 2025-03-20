from PIL import Image, ImageDraw, ImageFont
import os
import pillow_heif

format_colors = {
    'PNG': 'red',
    'GIF': 'green',
    'TIFF': 'blue',
    'BMP': 'yellow',
    'ICO': 'pink',
    'PPM': 'gray',
    'PBM': 'lime',
    'PGM': 'teal',
    'APNG': 'olive',
    'JPEG': 'indigo',
    'JFIF': 'silver',
    'HEIC': 'violet'
}

image_size = (1024, 1024)

try:
    font = ImageFont.truetype("arial.ttf", 200)
except IOError:
    font = ImageFont.load_default()

output_folder = 'input'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def generate_images():
    for index, (format, color) in enumerate(format_colors.items(), start=1):
        image = Image.new('RGB', image_size, color)
        draw = ImageDraw.Draw(image)
        
        text = format
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_position = ((image_size[0] - text_width) // 2, (image_size[1] - text_height) // 2)
        
        text_color = 'white' if color in ['blue', 'green', 'red', 'purple', 'navy', 'maroon', 'indigo'] else 'black'
        
        draw.text(text_position, text, fill=text_color, font=font)
        
        output_path = os.path.join(output_folder, f'sample-{index}.{format.lower()}')
        
        if format.upper() == 'HEIC':
            heif_file = pillow_heif.from_pillow(image)
            heif_file.save(output_path)
        else:
            image.save(output_path)
        
        print(f'Generated: {output_path}')

generate_images()