FROM python:3

COPY API_endpoint.py /


RUN pip3 install Pyro4
RUN pip3 install fastapi
RUN pip3 install "uvicorn[standard]"
RUN pip3 install pymongo

#Give receiver_port by command line
#CMD ["uvicorn", "API_endpoint:app", "--host", "0.0.0.0", "--port", "8000"]
