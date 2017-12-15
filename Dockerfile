FROM python:latest
LABEL maintainer="truthadjustr@gmail.com"

RUN pip install redis pysnmp
CMD ["python3","/mainapp.py"]
