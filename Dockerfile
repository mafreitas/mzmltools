FROM ubuntu:bionic

RUN apt-get update && apt-get install python3-pip procps -y \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install matplotlib pandas numpy psims pyopenms

ADD mzmltools.py /mzmltools/mzmltools.py 

ENV PATH /mzmltools:$PATH






