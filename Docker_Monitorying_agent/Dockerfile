FROM python:3

RUN pip install psutil

COPY . /opt

WORKDIR /opt

ENTRYPOINT ["python", "monitoring_agent.py"]
