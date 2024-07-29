FROM python:3.9
WORKDIR /opt/bron-llm
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
CMD ["tail", "-f", "docker/requirements.txt"]

