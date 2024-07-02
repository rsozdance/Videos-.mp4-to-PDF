# Video to PDF Converter

This Python application converts MP4 video files into PDF documents using Tkinter for the graphical interface and Pillow for image processing.

## Installation

### Prerequisites

- Python 3.6+
- pip (Python package installer)

### Clone the Repository

```bash
git clone https://github.com/rsozdance/Videos-.mp4-to-PDF.git
cd Videos-.mp4-to-PDF
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

The `requirements.txt` file contains the necessary Python packages for this application. Make sure you have Python and pip installed before proceeding with the installation.

## Usage

To run the application, execute the following command:

```bash
python main.py
```

### Instructions

1. **Select Video File(s)**:
   - Click on the **Browse** button to select one or multiple MP4 video files.
   - Selected files will be displayed in the text area labeled "Select video file(s):".

2. **Convert to PDF**:
   - After selecting video files, click on the **Convert to PDF** button to start the conversion process.
   - The application will create a PDF file for each selected video file containing extracted frames.

3. **Progress and Completion**:
   - During conversion, the window title will change to "Please Wait..." to indicate processing.
   - After conversion completes, the window title will revert to "Video to PDF Converter", and a success message box will appear.

## Contributing

Contributions are welcome! If you would like to contribute to this project, please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
