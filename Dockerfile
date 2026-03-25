# περιγραφει πως θα χτιστει το docker image για την εφαρμογη

FROM python:3.12slim

WORKDIR /app "οριζεται ο φακελος εργασιας μεσα στο container"

COPY requirements.txt . "αντιγραφει τα requirements.txt"

RUN pip install --no-cache-dir -r requirements.txt "εγκαθιστα dependencies"

COPY . . "αντιγραφει ολα τα αρχεια της εφαρμογης μεσα στο container"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
"οριζει την εντολη που θα τρεχει οταν ξεκιναει το container"