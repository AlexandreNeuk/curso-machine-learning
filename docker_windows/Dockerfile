# Dockerfile - this is a comment. Delete me if you want.
FROM python:3
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install requests
RUN pip install git+git://github.com/broadinstitute/cromwell-tools.git@v0.3.1
ENTRYPOINT ["python"]
CMD ["app.py"]
