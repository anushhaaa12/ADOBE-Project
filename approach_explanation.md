# Approach Explanation

## Challenge 1(a): PDF Outline Extraction

The primary goal for Challenge 1(a) was to extract a structured outline from a PDF, including the document title and headings (H1, H2, H3). To achieve this, I used the PyMuPDF library, which provides detailed access to text blocks, font sizes, and layout information within a PDF. The core idea was to leverage font size as a heuristic for heading detection: the largest font on the first page is typically the title, followed by progressively smaller fonts for H1, H2, and H3 headings. By collecting all text spans and their font sizes, I ranked the most common sizes and mapped them to heading levels. This approach is robust across a variety of document layouts, as it does not rely on hardcoded keywords or file-specific logic. The extracted outline is then output as a JSON file, matching the required format. The solution is containerized with Docker, ensuring reproducibility and compliance with the assignment’s constraints (CPU only, no internet access, amd64 compatibility).

## Challenge 1(b): Persona-Driven Document Intelligence

For Challenge 1(b), the task was to extract and prioritize the most relevant sections from a collection of PDFs, given a specific persona and job-to-be-done. The solution first extracts all text blocks from each PDF, treating each block as a potential section. To rank these sections by relevance, I used the TF-IDF (Term Frequency-Inverse Document Frequency) technique from scikit-learn, which is a standard method for measuring the importance of words in context. The persona and job description are combined into a single query, and each section is scored based on its similarity to this query. The top-ranked sections are selected, and for sub-section analysis, each section is further split into sentences using NLTK’s sentence tokenizer. The final output includes metadata, ranked sections, and sub-section analysis, all formatted as required.

## Design Choices and Challenges

A key design choice was to avoid any file-specific or font-name-based logic, making the solution generalizable to a wide range of PDFs. Using font size and TF-IDF provides a balance between simplicity and effectiveness, especially given the constraints of no internet access and limited runtime. One challenge was handling the diversity of PDF layouts and ensuring that heading detection works even when font sizes are not strictly hierarchical. Another was ensuring that the solution runs efficiently within the Docker container, with all dependencies installed offline. By containerizing both solutions, I ensured that the code is portable, reproducible, and easy to evaluate.

Overall, the approach emphasizes modularity, generalizability, and compliance with all hackathon requirements. 