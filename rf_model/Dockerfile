FROM python:3

WORKDIR /tmp/workflow/rf_model

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "./rf.py" ]
