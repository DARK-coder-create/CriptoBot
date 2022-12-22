FROM python:3
WORKDIR /api_flask_rest
COPY requirements.txt /api_flask_rest
RUN pip install --no-cache-dir -r requirements.txt
COPY /api_flask_rest /api_flask_rest
CMD ["python3", "app.py"]