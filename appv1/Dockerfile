FROM python:3.7
WORKDIR /tmp/workflow/appv1

ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_ENV development

RUN apt-get install libjpeg-dev \
                       zlib1g-dev \
                       libfreetype6-dev \
                       liblcms2-dev


COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

CMD ["flask", "run", "-p", "5010"]
