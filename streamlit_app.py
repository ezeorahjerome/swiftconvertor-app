import streamlit as st
import os
import tempfile
from PyPDF2 import PdfReader, PdfWriter
from pdf2image import convert_from_path
from PIL import Image
import zipfile
from docx import Document
from io import BytesIO


# Function to convert PDF to images
def pdf_to_images(pdf_file):
    images = convert_from_path(pdf_file)
    return images


# Function to convert images to PDF
def images_to_pdf(image_files):
    with BytesIO() as f:
        img = Image.open(image_files[0])
        img.save(f, "PDF", resolution=100.0, save_all=True, append_images=image_files[1:])
        return f.getvalue()


# Function to convert PDF to DOC
def pdf_to_doc(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    doc = Document()
    for page_num in range(pdf_reader.numPages):
        page = pdf_reader.getPage(page_num)
        doc.add_paragraph(page.extractText())
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.docx')
    doc.save(temp_file.name)
    return temp_file.name


# Function to convert DOC to PDF
def doc_to_pdf(doc_file):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    os.system(f'libreoffice --headless --convert-to pdf {doc_file} --outdir {tempfile.gettempdir()}')
    return temp_file.name


# Function to split PDF
def split_pdf(pdf_file):
    with open(pdf_file, 'rb') as f:
        pdf_reader = PdfReader(f)
        for page_num in range(pdf_reader.numPages):
            pdf_writer = PdfWriter()
            pdf_writer.addPage(pdf_reader.getPage(page_num))
            output_filename = f"{os.path.splitext(pdf_file)[0]}_page_{page_num+1}.pdf"
            with open(output_filename, 'wb') as output_file:
                pdf_writer.write(output_file)


# Function to merge PDF
def merge_pdf(pdf_files):
    merged_pdf = PdfWriter()
    for pdf_file in pdf_files:
        with open(pdf_file, 'rb') as f:
            pdf_reader = PdfReader(f)
            for page_num in range(pdf_reader.numPages):
                merged_pdf.addPage(pdf_reader.getPage(page_num))
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    with open(temp_file.name, 'wb') as output_file:
        merged_pdf.write(output_file)
    return temp_file.name


# Function to create a zip file
def create_zip(files):
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_file = os.path.join(temp_dir, 'output.zip')
        with zipfile.ZipFile(zip_file, 'w') as zipf:
            for file in files:
                zipf.write(file, os.path.basename(file))
        return zip_file


# Main function
def main():
    st.title("File Converter App")

    # Sidebar menu
    option = st.sidebar.selectbox("Select Operation", ["PDF to Image", "Image to PDF", "PDF to DOC", "DOC to PDF",
                                                       "Split PDF", "Merge PDF"])

    # Main content
    if option == "PDF to Image":
        st.subheader("PDF to Image Conversion")
        pdf_file = st.file_uploader("Upload a PDF file", type=['pdf'])
        if pdf_file is not None:
            images = pdf_to_images(pdf_file)
            st.image(images, caption="Converted Images", use_column_width=True)
            if st.button("Download Images as ZIP"):
                with tempfile.TemporaryDirectory() as temp_dir:
                    zip_file = create_zip([image.filename for image in images])
                    st.download_button(label="Download ZIP", data=zip_file, file_name="converted_images.zip")

    elif option == "Image to PDF":
        st.subheader("Image to PDF Conversion")
        image_file = st.file_uploader("Upload an image file", type=['png', 'jpg', 'jpeg'])
        if image_file is not None:
            pdf_bytes = images_to_pdf([image_file])
            st.write("PDF conversion complete!")
            if st.button("Download PDF"):
                st.download_button(label="Download PDF", data=pdf_bytes, file_name="converted_pdf.pdf")

    elif option == "PDF to DOC":
        st.subheader("PDF to DOC Conversion")
        pdf_file = st.file_uploader("Upload a PDF file", type=['pdf'])
        if pdf_file is not None:
            doc_file = pdf_to_doc(pdf_file)
            st.write("DOC conversion complete!")
            if st.button("Download DOC"):
                st.download_button(label="Download DOC", data=doc_file, file_name="converted_doc.docx")

    elif option == "DOC to PDF":
        st.subheader("DOC to PDF Conversion")
        doc_file = st.file_uploader("Upload a DOC file", type=['doc', 'docx'])
        if doc_file is not None:
            pdf_file = doc_to_pdf(doc_file)
            st.write("PDF conversion complete!")
            if st.button("Download PDF"):
                st.download_button(label="Download PDF", data=pdf_file, file_name="converted_pdf.pdf")

    elif option == "Split PDF":
        st.subheader("Split PDF")
        pdf_file = st.file_uploader("Upload a PDF file", type=['pdf'])
        if pdf_file is not None:
            split_pdf(pdf_file)
            st.write("PDF splitting complete!")
            if st.button("Download Split PDFs as ZIP"):
                files = [f"{os.path.splitext(pdf_file.name)[0]}_page_{i+1}.pdf" for i in range(PdfReader(pdf_file).numPages)]
                zip_file = create_zip(files)
                st.download_button(label="Download ZIP", data=zip_file, file_name="split_pdfs.zip")

    elif option == "Merge PDF":
        st.subheader("Merge PDF")
        pdf_files = st.file_uploader("Upload PDF files to merge", type=['pdf'], accept_multiple_files=True)
        if pdf_files is not None:
            merged_pdf_file = merge_pdf(pdf_files)
            st.write("PDF merging complete!")
            if st.button("Download Merged PDF"):
                st.download_button(label="Download PDF", data=merged_pdf_file, file_name="merged_pdf.pdf")


if __name__ == '__main__':
    main()
