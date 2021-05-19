FROM python:3

WORKDIR /tmp/workflow/ar_model

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "./ar.py" ]
