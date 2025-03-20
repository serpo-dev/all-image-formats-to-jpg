import os
from PIL import Image, ImageOps
import time
import pillow_heif



FIX_ORIENTATION = True



input_folder = 'input'
output_folder = 'output'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

supported_formats = ['PNG', 'GIF', 'TIFF', 'BMP', 'ICO', 'PPM', 'PBM', 'PGM', 'APNG', 'JPEG', 'JFIF', 'HEIC']
files = [f for f in os.listdir(input_folder) if any(f.upper().endswith(fmt) for fmt in supported_formats)]
total_files = len(files)
start_time = time.time()

def correct_orientation(img):
    try:
        if hasattr(img, '_getexif'):
            exif = img._getexif()
            if exif is not None:
                orientation = exif.get(274)
                if orientation == 3:
                    img = img.rotate(180, expand=True)
                elif orientation == 6:
                    img = img.rotate(270, expand=True)
                elif orientation == 8:
                    img = img.rotate(90, expand=True)
    except Exception as e:
        print(f"EXIF processing error: {e}")
    return img

for i, file in enumerate(files):
    file_path = os.path.join(input_folder, file)
    output_path = os.path.join(output_folder, os.path.splitext(file)[0] + '.jpg')
    
    try:
        if not os.path.isfile(file_path):
            print(f"Error: {file} is not a valid file. Skipping.")
            continue

        if file.upper().endswith('.HEIC'):
            heif_file = pillow_heif.open_heif(file_path)
            img = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data, "raw")
        else:
            with Image.open(file_path) as img:
                if FIX_ORIENTATION:
                    img = correct_orientation(img)
                img = img.convert('RGB')
            
        img.save(output_path, 'JPEG')
        
        elapsed_time = time.time() - start_time
        avg_time_per_file = elapsed_time / (i + 1)
        remaining_time = avg_time_per_file * (total_files - i - 1)
        
        print(f'Processed: {i + 1}/{total_files}, Estimated time remaining: {remaining_time:.2f} sec')
    except Exception as e:
        print(f'Error processing file {file}: {str(e)}')

print('Conversion completed.')