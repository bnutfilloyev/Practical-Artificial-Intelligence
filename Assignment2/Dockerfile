FROM python:3.9.14-buster

WORKDIR /app

RUN pip install --upgrade pip

RUN pip install -U spacy &&  \
    pip install -U nltk &&  \
    pip install -U numpy

COPY . .

RUN python -m spacy download en_core_web_sm

CMD ["python", "main.py"]