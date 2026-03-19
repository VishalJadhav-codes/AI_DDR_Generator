import fitz
import os

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""

    for page in doc:
        text += page.get_text()

    return text

if __name__ == "__main__":
    inspection_path = "Input_reports\Sample Report.pdf"
    thermal_path = "Input_reports\Thermal Images.pdf"

    output_folder = "output"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    inspection_text = extract_text_from_pdf(inspection_path)
    thermal_text = extract_text_from_pdf(thermal_path)

    with open("output/inspection_text.txt", "w", encoding="utf-8") as f:
        f.write(inspection_text)

    with open("output/thermal_text.txt", "w", encoding="utf-8") as f:
        f.write(thermal_text)

    print("The extraction completed.")