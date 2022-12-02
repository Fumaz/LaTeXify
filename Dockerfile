FROM python:3.10-buster

RUN apt-get update -y
RUN apt-get install -y texlive-extra-utils pnmtopng poppler-utils netpbm poppler-utils ps2eps dvipng texlive-full

COPY requirements.txt .

RUN pip install -U -r requirements.txt