import qrcode
from docx import Document
from datetime import datetime
from io import BytesIO
from docxtpl import DocxTemplate, InlineImage
import os
from data import input_data
from docx.shared import Cm

def generate_qr_code(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    file_path = f"./source/{url}.png"

    # Save the QR code image directly to the specified file path
    img.save(file_path, format="PNG")
    
    return file_path

def building(data):
    subject = str(input("Apa nama subject? "))
    sub_bab = str(input("Apa nama sub bab? "))
    url = input("Masukan URL source: ")
    
    qr_source = generate_qr_code(url)

    return subject, sub_bab, qr_source

def generate_docx(subject, sub_bab, file_path, data):
    doc = DocxTemplate('./template/template.docx')

    # Fill in template variables
    context = {
        'subject': subject.upper(),
        'sub_bab': sub_bab.capitalize(),
        'source': InlineImage(doc, file_path, width=Cm(1)),  
        'date': datetime.now().strftime("%d-%m-%Y"),
        'data': data,
    }

    # Apply context to the template
    doc.render(context)

    # Save the document
    name = f"{subject}-{sub_bab}"
    doc.save(f'{name}.docx')

    print(f'File {name}.docx berhasil dibuat!')

if __name__ == '__main__':
    data = input_data()
    subject, sub_bab, qr_source = building(data)
    generate_docx(subject, sub_bab, qr_source, data)