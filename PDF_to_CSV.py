import os
import re
import cv2
import pytesseract
import pandas as pd
import numpy as np
from pdf2image import convert_from_path


# -------------------- CONFIGURE --------------------

POPPLER_PATH = r"tools\poppler\Library\bin"

PDF_FILE = r"input\id_cards.pdf"
PDF_DPI = 300

OUTPUT_FILE = "candidate_details.xlsx"

CARDS_PER_PAGE = 5 #Each Page in PDF has 5 ID cards

pytesseract.pytesseract.tesseract_cmd = (
    r"tools\Tesseract-OCR\tesseract.exe"
)

OCR_CONFIGS = [
    "--psm 6",
    "--psm 4",
    "--psm 11"
]

# -------------------- VALIDATORS --------------------

def valid_name(name):
    return bool(
        name
        and re.fullmatch(r"[A-Za-z .'-]{3,50}", name)
    )

def valid_roll(roll):
    return bool(re.fullmatch(r"(PGP|IPM)\d{5}", roll))

def valid_dob(dob):
    return bool(re.fullmatch(r"\d{2}-\d{2}-\d{4}", dob))

# -------------------- OCR HELPERS --------------------

def ocr_retry(img):
    for cfg in OCR_CONFIGS:
        text = pytesseract.image_to_string(img, config=cfg)
        if text.strip():
            return text
    return ""

# -------------------- REGION SPLITTING --------------------

def split_regions(card):
    h, w = card.shape[:2]

    return {
        "name": card[int(0.15*h):int(0.35*h), int(0.05*w):int(0.7*w)],
        "roll": card[int(0.45*h):int(0.65*h), int(0.05*w):int(0.6*w)],
        "dob":  card[int(0.05*h):int(0.25*h), int(0.6*w):int(0.95*w)],
        "full": card
    }

# -------------------- CORE EXTRACTION --------------------

def extract_force(card):
    regions = split_regions(card)
    texts = {k: ocr_retry(v) for k, v in regions.items()}

    # -------- NAME --------
    name = ""
    for src in ("name", "full"):
        m = re.search(r"Name\s*[:>]\s*([A-Za-z .'-]+)", texts[src], re.I)
        if m:
            candidate = m.group(1).strip()
            if valid_name(candidate):
                name = candidate
                break

    # -------- ROLL --------
    roll = ""
    for src in ("roll", "full"):
        m = re.search(r"(PGP|IPM)\d{5}", texts[src])
        if m and valid_roll(m.group(0)):
            roll = m.group(0)
            break

    # -------- DOB --------
    dob = ""
    for src in ("dob", "full"):
        m = re.search(r"\d{2}-\d{2}-\d{4}", texts[src])
        if m and valid_dob(m.group(0)):
            dob = m.group(0)
            break

    return {
        "Name": name,
        "Roll No": roll,
        "DOB": dob
    }

# -------------------- MAIN PIPELINE --------------------

def main():
    rows = []

    pages = convert_from_path(
    PDF_FILE,
    dpi=300,
    poppler_path=POPPLER_PATH
)

    print(f"Processing {len(pages)} pages...")

    for page_index, page in enumerate(pages):
        img = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)

        h, w = img.shape[:2]
        card_h = h // CARDS_PER_PAGE

        for i in range(CARDS_PER_PAGE):
            card = img[i*card_h:(i+1)*card_h, 0:w]
            data = extract_force(card)
            rows.append(data)

        print(f"Page {page_index + 1}/{len(pages)} done")

    df = pd.DataFrame(rows)
    df.to_excel(OUTPUT_FILE, index=False)

    print(f"\nDONE")
    print(f"Total records: {len(df)}")
    print(f"Saved to: {OUTPUT_FILE}")

# -------------------- RUN --------------------

if __name__ == "__main__":
    main()
