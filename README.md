# PageVLM: Convert Handwritten PDF Notes to Text

This script uses a local Vision Language Model (VLM) running via an OpenAI-compatible API (like LM Studio) to transcribe handwritten notes from PDF files. Each page of the PDF is treated as a separate image and sent to the VLM for transcription.

## Features

*   Extracts pages from a PDF as images.
*   Sends images to a locally running VLM via its API.
*   Prompts the VLM to transcribe the handwritten text.
*   Outputs the transcribed text to the console or a specified file.
*   Shows a progress bar during processing.

## Requirements

*   Python 3.x
*   pip (Python package installer)
*   A running local VLM server with an OpenAI-compatible API endpoint (e.g., LM Studio) serving a model capable of image transcription (like Gemma-3).
*   Dependencies listed in `requirements.txt`:
    *   `pymupdf`: For PDF processing.
    *   `pillow`: For image handling.
    *   `openai`: For interacting with the VLM's API.
    *   `tqdm`: For the progress bar.

## Setup

1.  **Clone or Download:** Get the script (`main.py`) and `requirements.txt` file.
2.  **Install Dependencies:** Open your terminal or command prompt in the script's directory and run:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Start Local VLM:** Ensure your local VLM server (e.g., LM Studio) is running, has loaded a suitable VLM (like `gemma-3-4b-it-qat` or similar), and has its API server active.

    **Steps for LM Studio:**
    *   Open the LM Studio application.
    *   Go to the **Search** tab (magnifying glass icon) and download a suitable VLM that supports vision/image input (e.g., search for "Gemma 3 Instruct").
    *   Go to the **Local Server** tab ( `<->` icon).
    *   At the top, select the model you downloaded from the dropdown menu.
    *   Ensure the configuration options are suitable (GPU offloading, context length, etc. - defaults are often fine to start).
    *   Click the **Start Server** button.
    *   The server will start, and the **Model Configuration** section will show the exact model identifier loaded (e.g., `lmstudio-community/gemma-3-4b-it-gguf`) and the API Base URL (e.g., `http://localhost:1234/v1`). Note these down if they differ from the script's defaults, as you may need them for the `--model` and `--api_base_url` arguments.
    *   For more details, refer to the [LM Studio API Documentation](https://lmstudio.ai/docs/app/api).

## Configuration

The script needs to know the API endpoint URL of your VLM server and the specific model identifier being served.

*   **API Base URL:**
    *   Default: `http://localhost:1234/v1`
    *   Override with: `--api_base_url <your_vlm_api_url>`
*   **Model Name:**
    *   Default: `gemma-3-4b-it-qat`
    *   Override with: `--model <your_vlm_model_identifier>` (Make sure this exactly matches the model name/identifier shown in your VLM server interface/logs).

## Usage

Run the script from your terminal, providing the path to the input PDF file.

**Basic Usage (using defaults):**

```bash
python main.py path/to/your/notes.pdf
```

**Save Output to File:**

```bash
python main.py path/to/your/notes.pdf -o output.txt
```

**Specify VLM API URL and Model:**

```bash
python main.py path/to/your/notes.pdf --api_base_url http://192.168.1.50:1234/v1 --model specific-model-name-from-lmstudio
```

**Combine Options:**

```bash
python main.py handwritten_lecture.pdf -o lecture_notes.txt --model gemma-3-8b-it
```

The script will process each page and print the transcription to the console (or save it to the specified file), prepending each page's text with `--- Page X ---`.
