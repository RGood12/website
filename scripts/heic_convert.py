import pyheif
from PIL import Image
import zipfile
import io

def heic_convert(request_handler, file):
    with io.BytesIO() as zip_buffer:
        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
            for file_key, files in file:
                for file_data in files:
                    original_fname = file_data['filename'].split(".")[0]
                    original_fname = f"{original_fname}.jpeg"

                    i = pyheif.read_heif(file_data['body'])

                    # Convert to other file format like jpeg
                    converted_file = io.BytesIO()
                    pi = Image.frombytes(mode=i.mode, size=i.size, data=i.data)
                    pi.save(converted_file, "JPEG")

                    # Reset the position of the buffer
                    converted_file.seek(0)

                    # Add the converted file to the zip archive
                    zip_file.writestr(original_fname, converted_file.getvalue())

        # Set headers for the zip file response
        request_handler.set_header('Content-Type', 'application/zip')
        request_handler.set_header('Content-Disposition', 'attachment; filename=converted_files.zip')
        request_handler.write(zip_buffer.getvalue())