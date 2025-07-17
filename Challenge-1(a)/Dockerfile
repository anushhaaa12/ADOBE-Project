FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY process_pdfs.py .
COPY app/input ./input
RUN mkdir -p /app/output

CMD ["python", "process_pdfs.py"]