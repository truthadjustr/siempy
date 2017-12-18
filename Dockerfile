FROM python:latest
LABEL maintainer="dexter"

RUN pip install redis pysnmp pysnmp-mibs
CMD ["python3","/mainapp.py"]
