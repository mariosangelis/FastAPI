FROM python:3


COPY Service_Class.py /
COPY Skeleton.py /


RUN pip3 install Pyro4
RUN pip3 install pymongo
RUN pip3 install netifaces

#Give receiver_port by command line
#ENTRYPOINT ["python3", "./Skeleton.py"]
