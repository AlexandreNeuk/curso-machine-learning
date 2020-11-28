FROM python:3
COPY . /app
WORKDIR /app
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        cmake \
        build-essential \
        gcc \
        g++
RUN pip install -r requirements.txt
#RUN pip install requests
#RUN pip install git+git://github.com/broadinstitute/cromwell-tools.git@v0.3.1
#ENTRYPOINT ["python"]
#CMD ["app.py"]
CMD gunicorn --bind 0.0.0.0:$PORT wsgi