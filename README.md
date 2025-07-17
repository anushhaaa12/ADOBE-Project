# Adobe India Hackathon 2025 Submission

## Overview
This repository contains solutions for both rounds of the Adobe India Hackathon 2025:
- **Challenge 1(a): PDF Outline Extraction**
- **Challenge 1(b): Persona-Driven Document Intelligence**

Both solutions are fully containerized with Docker and require no internet access at runtime.

---

## Challenge 1(a): PDF Outline Extraction
- **Goal:** Extract the title and headings (H1, H2, H3) from a PDF and output a structured JSON outline.
- **How it works:**
  - Uses PyMuPDF to analyze font sizes and text blocks.
  - Assigns heading levels based on font size ranking.
  - Outputs a JSON file for each PDF in the required format.
- **Input:** Place PDFs in `app/input/`.
- **Output:** JSON files in `app/output/`.

### Build & Run (Docker)
```sh
cd Challenge-1(a)
docker build -t adobe-challenge-1a .
docker run --rm -v ${PWD}/app/input:/app/input -v ${PWD}/app/output:/app/output adobe-challenge-1a
```

---

## Challenge 1(b): Persona-Driven Document Intelligence
- **Goal:** Given a persona and job-to-be-done, extract and rank the most relevant sections from a collection of PDFs.
- **How it works:**
  - Extracts all text blocks from each PDF.
  - Uses TF-IDF to score and rank sections by relevance to the persona/job.
  - Outputs a JSON file with metadata, ranked sections, and sub-section analysis.
- **Input:** Place PDFs in `sample_docs/`.
- **Output:** `challenge1b_output_generated.json` in the same folder.

### Build & Run (Docker)
```sh
cd Challenge_1b
docker build -t adobe-challenge-1b .
docker run --rm -v ${PWD}:/app adobe-challenge-1b
```

---

## Dependencies
- Python 3.12
- PyMuPDF
- scikit-learn
- nltk

All dependencies are installed via `requirements.txt` in each challenge folder.

---

## Notes
- No internet access is required at runtime.
- All code runs on CPU and is compatible with amd64 architecture.
- For any issues, please check the folder structure and ensure Docker Desktop is running. 