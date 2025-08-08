FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# The default website file can be overridden at build time
ARG WEBSITE_FILE=site1.html
ENV WEBSITE_FILENAME=${WEBSITE_FILE}

EXPOSE 5000

CMD ["python", "app.py"]