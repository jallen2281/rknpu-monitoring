FROM python:3.12-slim-bookworm
# Use slim to keep the image under 50MB for fast node pulls
RUN pip install prometheus_client
COPY exporter.py /app/exporter.py
WORKDIR /app
# Run unbuffered so logs show up in MicroK8s immediately
CMD ["python3", "-u", "exporter.py"]
