'''

'''


from PIL import Image
import os

def resize_and_compress(input_path, output_path, width=160, height=212, kb_limit=20):
    # Open the image
    img = Image.open(input_path)
    
    # Resize the image
    # Use Image.ANTIALIAS or Image.Resampling.LANCZOS for quality in newer Pillow versions
    img = img.resize((width, height), Image.LANCZOS)

    # Save in a loop with decreasing quality until file size is under kb_limit
    quality = 95
    while quality > 10:  # avoid going too low in quality
        img.save(output_path, format='JPEG', quality=quality)
        file_size_kb = os.path.getsize(output_path) / 1024
        if file_size_kb <= kb_limit:
            break
        quality -= 5

    # Double-check final size is above 5kb (if that’s a requirement)
    file_size_kb = os.path.getsize(output_path) / 1024
    if file_size_kb < 5:
        print("Warning: The file is below 5 KB. Consider using less compression if needed.")

# Example usage:
resize_and_compress(
    input_path='DSC_2085.JPG',
    output_path='DSC_2085_resized.jpg',
    width=160,
    height=212,
    kb_limit=20
)
