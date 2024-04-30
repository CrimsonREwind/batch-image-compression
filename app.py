import streamlit as st
from PIL import Image
import io
import zipfile

st.title("Bulk Image Compressor")
uploaded_files = st.file_uploader("Select images to compress", type=["jpg", "jpeg", "png", "gif", "bmp"], accept_multiple_files=True)
quality = st.slider("Compression quality", 1, 95, 80)
compress_button = st.button("Compress images")
compressed_images = []
download_link = ""

if compress_button and uploaded_files:
    progress_bar = st.progress(0)

    for i, file in enumerate(uploaded_files):
        image = Image.open(io.BytesIO(file.getvalue()))
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=quality)
        compressed_image = buffer.getvalue()
        compressed_images.append(compressed_image)
        progress_bar.progress((i + 1) / len(uploaded_files))
        
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for i, compressed_image in enumerate(compressed_images):
            zip_file.writestr(f"image_{i}.jpg", compressed_image)

    zip_buffer.seek(0)
    download_link = st.download_button("Download", zip_buffer.getvalue(), "compressed_images.zip", "application/zip")
