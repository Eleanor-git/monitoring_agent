FROM python:3.13-alpine 

RUN pip install psutil

COPY ./monitoring_agent.py /opt

WORKDIR /opt

ENTRYPOINT ["python", "monitoring_agent.py"]
