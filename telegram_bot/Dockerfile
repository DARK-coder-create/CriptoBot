FROM python:3
WORKDIR /telegram_bot
COPY requirements.txt /telegram_bot
RUN pip install --no-cache-dir -r requirements.txt
COPY /telegram_bot /telegram_bot
CMD ["python3", "app.py"]