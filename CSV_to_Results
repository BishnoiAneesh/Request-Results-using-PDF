import pandas as pd
import requests
import time
import urllib3
from bs4 import BeautifulSoup
import re

# ---------------- CONFIG ----------------

INPUT_FILE = r"candidate details.xlsx"
OUTPUT_FILE = r"final_results_Term I_subjectwise.xlsx"

URL = "https://results.Term1/fetchdata1.php"
TERM = "I"

urllib3.disable_warnings()

session = requests.Session()

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://results.Term1/index.php?t=1"
}

                                                                                                                                                                             ":"""""| :)"""
def parse_result_html(html, roll_no):
    soup = BeautifulSoup(html, "html.parser")

    header_table = soup.find("table")

    # If no table → portal did not return a result page
    if header_table is None:
        return {
            "Roll No": roll_no,
            "Name": "",
            "Term": "",
            "TGPA": "",
            "CGPA": "",
            "Status": "Result not returned"
        }

    rows = soup.find_all("tr")
    header_text = header_table.get_text(" ", strip=True)

    name_match = re.search(r"Name:([A-Za-z ]+)", header_text)
    roll_match = re.search(r"Roll_No\s*:\s*(\w+)", header_text)
    term_match = re.search(r"Term\s*:\s*(\w+)", header_text)

    result = {
        "Roll No": roll_match.group(1).strip() if roll_match else roll_no,
        "Name": name_match.group(1).strip() if name_match else "",
        "Term": term_match.group(1).strip() if term_match else "",
        "TGPA": "",
        "CGPA": "",
        "Status": "OK"
    }

    for r in rows:
        cols = r.find_all("td")

        # Subject rows
        if len(cols) == 3 and cols[0].text.strip().isdigit():
            subject = cols[1].text.strip()
            grade = cols[2].text.strip()
            result[subject] = grade

        # TGPA / CGPA rows
        if len(cols) == 3 and "TGPA" in cols[1].text:
            result["TGPA"] = cols[2].text.strip()
        if len(cols) == 3 and "CGPA" in cols[1].text:
            result["CGPA"] = cols[2].text.strip()

    return result

# ---------------- MAIN ----------------

def main():
    df = pd.read_excel(INPUT_FILE)
    total = len(df)

    final_rows = []

    for i, row in df.iterrows():
        payload = {
            "rollno": row["Roll No"],
            "termresult": TERM,
            "password": row["DOB"],
            "generate_pdf": ""
        }

        try:
            response = session.post(
                URL,
                data=payload,
                headers=HEADERS,
                verify=False,
                timeout=10
            )

            parsed = parse_result_html(response.text, row["Roll No"])

        except Exception as e:
            parsed = {
                "Roll No": row["Roll No"],
                "Name": "",
                "Term": "",
                "TGPA": "",
                "CGPA": "",
                "Status": f"Error: {str(e)}"
            }

        final_rows.append(parsed)

        # Progress print
        print(f"{i+1}/{total} done → {row['Roll No']}")

        time.sleep(1)  # polite delay

    out_df = pd.DataFrame(final_rows)
    out_df.to_excel(OUTPUT_FILE, index=False)

    print("\nDONE")
    print("Saved to:", OUTPUT_FILE)

# ---------------- RUN ----------------

if __name__ == "__main__":
    main()
