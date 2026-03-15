FROM python:3.13
WORKDIR /BookService
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY comands.sh .
RUN chmod +x comands.sh
COPY . .
EXPOSE 800
ENV DJANGO_SETTINGS_MODULE=BookService.settings
CMD ["bash", "comands.sh"]


