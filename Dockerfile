FROM python:latest
LABEL maintainer="truthadjustr@gmail.com"

RUN pip install redis pysnmp pysnmp-mibs
CMD ["python3","/mainapp.py"]
