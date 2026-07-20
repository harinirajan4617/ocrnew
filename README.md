# 🪪 Aadhaar OCR Web Application

A Streamlit-based web application that extracts information from Indian Aadhaar cards using EasyOCR. The application supports both front and back images of Aadhaar cards and automatically identifies important fields such as Name, Date of Birth, Gender, Aadhaar Number, and Address.

---

## Features

- Upload front and back Aadhaar images
- Supports JPG, JPEG and PNG images
- OCR using EasyOCR
- Extracts:
  - Name
  - Date of Birth
  - Gender
  - Aadhaar Number
  - Address
- Displays extracted information in a structured format
- User-friendly Streamlit interface

---

## Tech Stack

- Python
- Streamlit
- EasyOCR
- OpenCV
- NumPy
- Pandas
- Pillow

---

## Project Structure

```
ocrnew/
│── ocr.py
│── requirements.txt
│── README.md
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/harinirajan4617/ocrnew.git
```

Move into the project directory

```bash
cd ocrnew
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Application

```bash
streamlit run ocr.py
```

The application will open in your browser at

```
http://localhost:8501
```

---

## Requirements

Install all required packages using

```bash
pip install -r requirements.txt
```

Example requirements:

```
streamlit
easyocr
opencv-python-headless
numpy
pandas
Pillow
torch
torchvision
```

---

## Supported Image Formats

- JPG
- JPEG
- PNG

---

## Future Improvements

- QR Code extraction
- Better OCR accuracy
- Automatic image rotation
- Mask Aadhaar number for privacy
- Export extracted data to Excel or CSV

---

## Author

**Harini Rajan**

GitHub: https://github.com/harinirajan4617

---

## License

This project is developed for educational and learning purposes.
