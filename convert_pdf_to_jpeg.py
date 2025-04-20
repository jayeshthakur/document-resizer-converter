import os
from io import BytesIO

import fitz   # PyMuPDF
from PIL import Image

def pdf_to_single_jpg(pdf_path, output_path=None, dpi=100, target_kb=100):
    """
    Convert all pages of a PDF into one concatenated JPEG image,
    compressed to <= target_kb kilobytes, using only Python libs.

    Args:
        pdf_path (str): Path to source PDF.
        output_path (str): Output JPG path; defaults to '<basename>_combined.jpg'.
        dpi (int): Render DPI for each page (lower ⇒ smaller images).
        target_kb (int): Max size in KB for the final JPEG.
    """
    # Prepare output filename
    base, _ = os.path.splitext(pdf_path)
    if not output_path:
        output_path = f"{base}_combined.jpg"

    # Open PDF
    doc = fitz.open(pdf_path)
    images = []
    for page in doc:
        # render page to pixmap
        mat = fitz.Matrix(dpi / 72, dpi / 72)  # 72 is default PDF pts-per-inch
        pix = page.get_pixmap(matrix=mat, alpha=False)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)
    doc.close()

    # compute total dimensions
    total_height = sum(img.height for img in images)
    max_width    = max(img.width for img in images)

    # create blank canvas and paste pages
    combined = Image.new("RGB", (max_width, total_height), "white")
    y_offset = 0
    for img in images:
        combined.paste(img, (0, y_offset))
        y_offset += img.height

    # compress JPEG down in quality steps until ≤ target_kb
    quality = 95
    while quality >= 10:
        buf = BytesIO()
        combined.save(buf, format="JPEG", quality=quality)
        size_kb = buf.tell() / 1024
        if size_kb <= target_kb:
            with open(output_path, "wb") as f:
                f.write(buf.getvalue())
            print(f"✅ Saved '{output_path}' at quality={quality}, size={size_kb:.1f} KB")
            return output_path
        quality -= 5

    # fallback: lowest quality tried
    with open(output_path, "wb") as f:
        f.write(buf.getvalue())
    final_size_kb = os.path.getsize(output_path) / 1024
    print(f"⚠️ Fallback saved '{output_path}' at quality={quality}, size={final_size_kb:.1f} KB")
    return output_path

if __name__ == "__main__":
    pdf_file = input("Enter path to your PDF file: ").strip()
    if not os.path.isfile(pdf_file):
        print(f"Error: '{pdf_file}' not found.")
    else:
        pdf_to_single_jpg(pdf_file)
