FROM python:3.8.3

WORKDIR /app

COPY src/requirements.txt ./

RUN pip install -r requirements.txt

COPY src/ /app/
COPY *.pkl /app/
RUN ls -al /app

CMD [ "python", "predict_supplier.py" ]
