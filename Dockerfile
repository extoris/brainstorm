FROM python:3.9

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /code

COPY data/ handlers/ keyboards/ misc/ model/ bot.py brainstorm.db sql.py voices.db /code/

CMD [ "python", "bot.py" ]