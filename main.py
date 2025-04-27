import argparse
import fitz  # PyMuPDF
import base64
from openai import OpenAI
from PIL import Image
import io
from tqdm import tqdm

def pdf_page_to_image_bytes(doc, page_num):
    """Converts a PDF page to PNG image bytes."""
    page = doc.load_page(page_num)
    pix = page.get_pixmap()

    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr

def image_to_base64(image_bytes):
    return base64.b64encode(image_bytes).decode('utf-8')

def process_image_with_vlm(client, image_base64, model_name):
    """Sends the image to the VLM and returns the text description."""
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Convert the image to text, only output the converted text.",},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_base64}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=2048,
        )
        if response.choices and response.choices[0].message:
            return response.choices[0].message.content.strip()
        else:
            return "Error: Could not extract text from VLM response."
    except Exception as e:
        return f"Error interacting with VLM: {e}"

def main(pdf_path, output_file, api_base_url, model_name):
    print(f"Loading local model '{model_name}' via API at {api_base_url}...")
    client = OpenAI(base_url=api_base_url, api_key="lm-studio") # API key is often ignored by local servers but required by the lib

    print(f"Processing PDF: {pdf_path}")
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening PDF file: {e}")
        return

    num_pages = len(doc)
    print(f"Found {num_pages} page(s). Starting transcription...")

    all_text = []
    for page_num in tqdm(range(num_pages), desc="Processing pages"):
        try:
            image_bytes = pdf_page_to_image_bytes(doc, page_num)
            image_base64 = image_to_base64(image_bytes)
            extracted_text = process_image_with_vlm(client, image_base64, model_name)
            all_text.append(f"--- Page {page_num + 1} ---\n{extracted_text}\n")
        except Exception as e:
            all_text.append(f"--- Page {page_num + 1} ---\nError processing page: {e}\n")

    doc.close()

    output_content = "\n".join(all_text)

    if output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output_content)
            print(f"Transcription complete. Output saved to: {output_file}")
        except Exception as e:
            print(f"Error writing to output file: {e}")
            print("\n--- Transcription Output ---\n")
            print(output_content)
    else:
        print("\n--- Transcription Output ---\n")
        print(output_content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert handwritten notes in a PDF to text using a local VLM.")
    parser.add_argument("pdf_path", help="Path to the input PDF file.")
    parser.add_argument("-o", "--output", help="Path to the output text file (optional). Prints to console if not provided.")
    parser.add_argument("--api_base_url", default="http://localhost:1234/v1", help="Base URL for the local VLM API endpoint.")
    parser.add_argument("--model", default="gemma-3-4b-it-qat", help="Name/identifier of the VLM model loaded in LM Studio.")

    args = parser.parse_args()

    model_identifier = args.model
    default_model_name = "gemma-3-4b-it-qat"

    using_default_model = args.model == default_model_name

    if using_default_model:
        print(f"Warning: Using default model name '{default_model_name}'. Ensure this matches the model loaded in LM Studio or use the --model argument to override.")
    else:
        print(f"Using model: {model_identifier}")

    main(args.pdf_path, args.output, args.api_base_url, model_identifier)
