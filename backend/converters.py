from pdf2docx import Converter
from PIL import Image

def convert_pdf_to_docx(pdf_path, output_path):

    try: 
        print(f"Starting conversion of: {pdf_path}")

        cv = Converter(pdf_path)
        cv.convert(output_path)
        cv.close()

        print(f"Success! Saved at: {output_path}")
        return True
    
    except Exception as ex:
        print(f"Error in .docx conversion: {ex}")
        return False
    
def convert_image_to_pdf(image_path, output_path):

    try:
        print(f"Starting conversion of: {image_path}")

        image = Image.open(image_path)

        if image.mode != 'RGB':
            image = image.convert('RGB')

        image.save(output_path)
        return True
    
    except Exception as ex: 
        print(f"Error in image conversion: {ex}")
        return False
