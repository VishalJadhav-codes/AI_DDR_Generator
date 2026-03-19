import fitz
import os

def extract_images_from_pdf(pdf_path, output_folder):

    doc = fitz.open(pdf_path)

    # Create Output Folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    image_count = 0

    # Loop through each page
    for page_number in range(len(doc)):
        page = doc.load_page(page_number)

        # Get images from page 
        image_list = page.get_images(full=True)

        for img in image_list:
            xref = img[0]

            # Extract image 
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            image_filename = f"image_{image_count}.{image_ext}"
            image_path = os.path.join(output_folder, image_filename)

            # Save image
            with open(image_path, "wb") as f:
                f.write(image_bytes)
 
            image_count += 1

    print(f"Total images extracted: {image_count}")

if __name__ == "__main__":
    pdf_path = "Input_reports/Sample Report.pdf"
    output_folder = "../extracted_images"

    extract_images_from_pdf(pdf_path, output_folder)
