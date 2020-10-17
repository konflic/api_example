FROM python:3.7

WORKDIR app/

COPY . .

EXPOSE 8888

RUN pip install -r requirements.txt

CMD ["python", "app.py"]