FROM python:3.10-buster

RUN apt-get update -y
RUN apt-get install -y texlive-extra-utils pnmtopng poppler-utils netpbm poppler-utils

COPY requirements.txt .

RUN pip install --no-cache-dir -U -r requirements.txt