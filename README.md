# Request-Results-using-PDF

This project implements an end-to-end Python automation pipeline to consolidate academic result data from a form-based web system into structured Excel outputs using candidate details from id_cards.pdf

## Problem Statement
Manual retrieval and consolidation of individual academic results is time-consuming and error-prone when performed at scale.

## Solution Overview
The automation extracts structured identifiers from ID cards using OCR, prepares validated input datasets, submits form-based queries programmatically, and parses returned HTML responses to generate subject-wise grades along with TGPA and CGPA.

## Workflow
1. Cut PDF into single ID card img
2. OCR-based parsing of ID card images
3. Structured CSV generation for input validation
4. Programmatic form submission using HTTP requests
5. HTML response parsing for subject-wise grades
6. Consolidated Excel output generation

## Ethical Note
This project is intended for educational and administrative automation purposes only.  
No real credentials or personal information are included in this repository.
