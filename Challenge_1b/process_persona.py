import os
import json
import fitz  # PyMuPDF
from pathlib import Path
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

# --- CONFIGURATION ---
INPUT_DIR = Path("sample_docs")
PERSONA = "Undergraduate Chemistry Student"
JOB_TO_BE_DONE = "Identify key concepts and mechanisms for exam preparation on reaction kinetics"
OUTPUT_FILE = "challenge1b_output_generated.json"
TOP_N_SECTIONS = 5  # Number of top sections to extract

# --- STEP 1: Extract sections from PDFs ---
def extract_sections_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    sections = []
    for page_num, page in enumerate(doc, 1):
        blocks = page.get_text("dict")['blocks']
        for block in blocks:
            if 'lines' in block:
                text = " ".join(span['text'] for line in block['lines'] for span in line['spans']).strip()
                if text:
                    sections.append({
                        'document': pdf_path.name,
                        'page': page_num,
                        'section_title': text[:60],  # Use first 60 chars as a pseudo-title
                        'full_text': text
                    })
    return sections

# --- STEP 2: Score sections for relevance ---
def rank_sections(sections, persona, job, top_n=5):
    # Combine persona and job as the query
    query = persona + " " + job
    corpus = [s['full_text'] for s in sections]
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(corpus + [query])
    query_vec = X[-1]
    section_vecs = X[:-1]
    scores = (section_vecs * query_vec.T).toarray().flatten()
    # Attach scores and sort
    for i, score in enumerate(scores):
        sections[i]['score'] = float(score)
    ranked = sorted(sections, key=lambda s: s['score'], reverse=True)
    return ranked[:top_n]

# --- STEP 3: Build output JSON ---
def build_output_json(input_docs, persona, job, ranked_sections):
    now = datetime.now().isoformat()
    output = {
        'metadata': {
            'input_documents': input_docs,
            'persona': persona,
            'job_to_be_done': job,
            'processing_timestamp': now
        },
        'extracted_sections': [],
        'sub_section_analysis': []
    }
    for rank, section in enumerate(ranked_sections, 1):
        output['extracted_sections'].append({
            'document': section['document'],
            'page_number': section['page'],
            'section_title': section['section_title'],
            'importance_rank': rank
        })
        # Sub-section: split into sentences as a simple refinement
        for sent in sent_tokenize(section['full_text']):
            output['sub_section_analysis'].append({
                'document': section['document'],
                'refined_text': sent,
                'page_number': section['page']
            })
    return output

# --- MAIN EXECUTION ---
def main():
    # 1. Gather all PDFs
    pdf_files = list(INPUT_DIR.glob("*.pdf"))
    input_docs = [f.name for f in pdf_files]
    all_sections = []
    for pdf in pdf_files:
        all_sections.extend(extract_sections_from_pdf(pdf))
    # 2. Rank sections
    ranked = rank_sections(all_sections, PERSONA, JOB_TO_BE_DONE, TOP_N_SECTIONS)
    # 3. Build output
    output = build_output_json(input_docs, PERSONA, JOB_TO_BE_DONE, ranked)
    # 4. Write output
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"Output written to {OUTPUT_FILE}")

if __name__ == "__main__":
    main() 