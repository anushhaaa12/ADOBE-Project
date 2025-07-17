import os
import json
from pathlib import Path
import fitz  # PyMuPDF
from collections import Counter, defaultdict


def extract_headings(pdf_path):
    doc = fitz.open(pdf_path)
    font_sizes = []
    text_blocks = []

    # Step 1: Collect all text spans with their font sizes and page numbers
    for page_num, page in enumerate(doc, 1):  # type: ignore
        blocks = page.get_text("dict")['blocks']
        for block in blocks:
            if 'lines' in block:
                for line in block['lines']:
                    for span in line['spans']:
                        text = span['text'].strip()
                        if text:
                            font_sizes.append(span['size'])
                            text_blocks.append({
                                'text': text,
                                'size': span['size'],
                                'page': page_num
                            })

    # Step 2: Determine the most common font sizes (title, H1, H2, H3)
    size_counts = Counter(font_sizes)
    most_common_sizes = [size for size, _ in size_counts.most_common(4)]
    most_common_sizes.sort(reverse=True)  # Largest = title, then H1, H2, H3

    # Step 3: Assign levels based on font size
    size_to_level = {}
    if most_common_sizes:
        size_to_level[most_common_sizes[0]] = 'Title'
    if len(most_common_sizes) > 1:
        size_to_level[most_common_sizes[1]] = 'H1'
    if len(most_common_sizes) > 2:
        size_to_level[most_common_sizes[2]] = 'H2'
    if len(most_common_sizes) > 3:
        size_to_level[most_common_sizes[3]] = 'H3'

    # Step 4: Build the outline
    title = None
    outline = []
    for block in text_blocks:
        level = size_to_level.get(block['size'])
        if level == 'Title' and not title:
            title = block['text']
        elif level in ('H1', 'H2', 'H3'):
            outline.append({
                'level': level,
                'text': block['text'],
                'page': block['page']
            })

    # Fallback if no title found
    if not title:
        title = Path(pdf_path).stem

    return {
        'title': title,
        'outline': outline
    }


def process_pdfs():
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    pdf_files = list(input_dir.glob("*.pdf"))

    for pdf_file in pdf_files:
        # Extract real headings and title
        data = extract_headings(pdf_file)
        output_file = output_dir / f"{pdf_file.stem}.json"
        with open(output_file, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Processed {pdf_file.name} -> {output_file.name}")

if __name__ == "__main__":
    print("Starting processing pdfs")
    process_pdfs()
    print("completed processing pdfs")