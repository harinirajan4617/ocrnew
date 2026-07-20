import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import cv2
import re
import pandas as pd

st.set_page_config(page_title="Aadhaar OCR", layout="wide")

st.title("🪪 Aadhaar OCR")

reader = easyocr.Reader(['en'])

uploaded = st.file_uploader(
    "Upload Aadhaar Card",
    type=["jpg", "jpeg", "png"]
)

if uploaded:

    image = Image.open(uploaded).convert("RGB")

    img = np.array(image)

    st.image(image, use_container_width=True)

    result = reader.readtext(img)

    full_text = ""

    boxes = []

    for r in result:

        box = r[0]
        text = r[1]
        conf = r[2]

        full_text += text + "\n"

        boxes.append((box, text, conf))

    ########################################

    aadhaar = ""

    m = re.search(r"\d{4}\s?\d{4}\s?\d{4}", full_text)

    if m:
        aadhaar = m.group()

    ########################################

    dob = ""

    m = re.search(r"\d{2}/\d{2}/\d{4}", full_text)

    if m:
        dob = m.group()

    ########################################

    ########################################
    # Improved Gender Extraction
    ########################################

    gender = ""

    text_lower = full_text.lower()

    # Check each OCR line individually
    for line in full_text.split("\n"):

        l = line.strip().lower()

        # Ignore labels like "Gender :"
        l = l.replace("gender", "").replace(":", "").strip()

        if re.fullmatch(r"female", l):
            gender = "Female"
            break

        elif re.fullmatch(r"male", l):
            gender = "Male"
            break

    # Fallback if OCR merged text
    if gender == "":
        if re.search(r"\bfemale\b", text_lower):
            gender = "Female"
        elif re.search(r"\bmale\b", text_lower):
            gender = "Male"

    ########################################

    ########################################
    # Improved Name Extraction
    ########################################

    ocr_lines = []

    for box, text, conf in boxes:
        t = text.strip()

        # Ignore low confidence OCR results
        if conf < 0.40:
            continue

        if t:
            ocr_lines.append(t)

    name = ""

    # Try finding the line just above DOB / Year of Birth / Gender
    for i, line in enumerate(ocr_lines):

        l = line.lower()

        if (
            "dob" in l
            or "year of birth" in l
            or re.search(r"\d{2}[/-]\d{2}[/-]\d{4}", line)
            or re.search(r"\b(19|20)\d{2}\b", line)
            or l == "male"
            or l == "female"
        ):

            if i > 0:

                candidate = ocr_lines[i - 1].strip()

                # Ignore unwanted lines
                if not any(x in candidate.lower() for x in [
                    "government",
                    "india",
                    "unique",
                    "authority",
                    "address",
                    "vid"
                ]):

                    name = candidate
                    break

    # Fallback
    if name == "":

        for line in ocr_lines:

            l = line.lower()

            # Ignore lines containing digits
            if re.search(r"\d", line):
                continue

            # Ignore common Aadhaar headings
            if any(x in l for x in [
                "government",
                "india",
                "unique",
                "authority",
                "address",
                "dob",
                "birth",
                "male",
                "female",
                "vid"
            ]):
                continue

            # Accept only probable names
            if 2 <= len(line.split()) <= 5:
                name = line
                break
    ########################################

    address = ""

    start = False

    for line in full_text.split("\n"):

        if "Address" in line:

            start = True

            continue

        if start:

            if "VID" in line:

                break

            if "1947" in line:

                break

            address += line + " "

    ########################################

    c1, c2 = st.columns(2)

    with c1:

        st.text_input("Name", name)

        st.text_input("DOB", dob)

        st.text_input("Gender", gender)

    with c2:

        st.text_input("Aadhaar Number", aadhaar)

        st.text_area("Address", address)

    ########################################

    draw = img.copy()

    for box, text, conf in boxes:

        pts = np.array(box).astype(int)

        cv2.polylines(draw, [pts], True, (0,255,0), 2)

        cv2.putText(
            draw,
            text,
            tuple(pts[0]),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255,0,0),
            2
        )

    st.subheader("Detected Text")

    st.image(draw, use_container_width=True)

    ########################################

    df = pd.DataFrame({
        "Field":[
            "Name",
            "DOB",
            "Gender",
            "Aadhaar Number",
            "Address"
        ],
        "Value":[
            name,
            dob,
            gender,
            aadhaar,
            address
        ]
    })

    st.dataframe(df)

    st.download_button(
        "Download CSV",
        df.to_csv(index=False),
        "aadhaar.csv",
        "text/csv"
    )

    with st.expander("Raw OCR"):

        st.text(full_text)