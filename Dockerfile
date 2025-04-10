FROM python:3.10

WORKDIR /app

COPY requirements.txt ./
COPY model_weights/ ./model_weights
COPY src/ ./src
RUN pip install -r requirements.txt -f https://download.pytorch.org/whl/torch_stable.html

CMD [ "python", "./src/app.py" ]

