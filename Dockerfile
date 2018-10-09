FROM python:3.6

EXPOSE 5000
WORKDIR /app

# deploy project
COPY ./src ./src
COPY ./requirement.txt ./
RUN pip install -U pip
RUN pip install -r ./requirement.txt

# define file storage
ENV DOLLSITE_FILE_STORAGE /app/files
RUN mkdir files
RUN ls

ENV DS_DB_PASSW masterkey123
ENV FLASK_APP src/entry.py
CMD ["flask", "run", "--host=0.0.0.0"]
