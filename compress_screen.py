import os
import subprocess

PDF_SETTINGS = [
    '/screen',   # lowest quality, smallest file (72 dpi)
    '/ebook',    # medium quality, medium file (150 dpi)
    '/printer',  # higher quality, larger file (300 dpi)
]

def gs_compress(input_path, output_path, pdf_setting):
    """Run Ghostscript with a given PDFSETTINGS preset."""
    cmd = [
        'gs',
        '-sDEVICE=pdfwrite',
        '-dCompatibilityLevel=1.4',
        f'-dPDFSETTINGS={pdf_setting}',
        '-dNOPAUSE',
        '-dQUIET',
        '-dBATCH',
        '-dDetectDuplicateImages',
        '-dCompressFonts=true',
        f'-sOutputFile={output_path}',
        input_path
    ]
    subprocess.run(cmd, check=True)

def smart_compress(input_path, min_kb=75, max_kb=100):
    """
    Try each PDFSETTINGS preset in turn until the output size is <= max_kb.
    Warn if below min_kb. Always saves as <basename>_compressed.pdf.
    """
    base, _ = os.path.splitext(input_path)
    output_path = f"{base}_compressed.pdf"
    temp_path  = f"{base}_temp.pdf"

    for setting in PDF_SETTINGS:
        gs_compress(input_path, temp_path, setting)
        size_kb = os.path.getsize(temp_path) / 1024
        print(f"→ Tried {setting}: {size_kb:.1f} KB")
        if size_kb <= max_kb:
            os.replace(temp_path, output_path)
            print(f"✅ Success: {setting} → {size_kb:.1f} KB")
            if size_kb < min_kb:
                print(f"⚠️ Warning: output below {min_kb} KB")
            return output_path

    # If none hit the target, keep the smallest we got
    size_kb = os.path.getsize(temp_path) / 1024
    os.replace(temp_path, output_path)
    print(f"❗ Couldn’t get under {max_kb} KB. Final: {size_kb:.1f} KB")
    return output_path

if __name__ == "__main__":
    pdf = input("Path to PDF: ").strip()
    if not os.path.isfile(pdf):
        print("File not found!")
    else:
        out = smart_compress(pdf)
        print("Saved compressed to:", out)
