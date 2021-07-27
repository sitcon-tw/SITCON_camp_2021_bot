FROM python:3.8

WORKDIR /usr/src/app

COPY . .

RUN pip install -U pipenv && \
    pipenv install --system --deploy --ignore-pipfile && \
    python pointsCodeGenerator.py && \
    mv setting-sample.json setting.json

CMD ["python", "-u", "bot.py"]
