FROM python:3.10-slim
ENV TOKEN='7060128802:AAF6AYAlZU1OnfrfW0tFvXe7asFjcd5vfaM'
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT [ "python", "bot.py" ]