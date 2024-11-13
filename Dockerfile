FROM python:3.9-slim

WORKDIR /opt/Projet_Mouha
COPY .. /opt/Projet_Mouha

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "src/loader_script.py"]
