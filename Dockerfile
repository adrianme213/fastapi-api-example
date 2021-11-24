FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN pip install --upgrade pip

COPY app/requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY . /app

EXPOSE 3000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000", "--reload"]
