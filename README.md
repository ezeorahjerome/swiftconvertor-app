# PDFtoWhatever

https://pdftowhatever.streamlit.app/


This is a Streamlit multipage app for converting various file formats. It provides the following functionalities:

1. PDF to Image
2. Image to PDF
3. PDF to DOC
4. DOC to PDF
5. Split PDF
6. Merge PDF

For single files, such as PDF to DOC or DOC to PDF, the output is handled as usual. For multiple results, such as converting a multi-page PDF to images or splitting a PDF, the output is provided as a zip file of the results.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Dmukherjeetextiles/PDFtoWhatever.git
    ```

2. Navigate to the project directory:

    ```bash
    cd file-converter-app
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the Streamlit app:

    ```bash
    streamlit run streamlit_app.py
    ```

2. Open the provided URL in your web browser.

3. Use the sidebar to select the desired operation and upload the appropriate file(s).

4. Click on buttons to perform conversions and download the output files.

## File Structure

- `streamlit_app.py`: The main Streamlit application script containing the app logic.
- `requirements.txt`: A list of Python dependencies required to run the app.
- `README.md`: This file providing information about the app.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/Dmukherjeetextiles/PDFtoWhatever/blob/main/LICENSE) file for details.
