FROM python:3.10-alpine3.17
WORKDIR /bot
COPY ./requirements.txt /bot/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /bot/requirements.txt
COPY . .
RUN chmod a+x *.sh
CMD ["sh", "app.sh"]