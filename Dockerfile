# Use an official Python runtime as a parent image
FROM ubuntu:22.04
FROM python:3.10

# Set the working directory in the container
WORKDIR /usr/src/app

# Включаем видимость видеокарты
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility

# Copy the dependencies file to the working directory
COPY r.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install -r r.txt

RUN apt-get update && apt-get install -y wget && \
    wget http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.0g-2ubuntu4_amd64.deb && \
    dpkg -i libssl1.1_1.1.0g-2ubuntu4_amd64.deb && \
    rm libssl1.1_1.1.0g-2ubuntu4_amd64.deb
RUN apt-get install ffmpeg libsm6 libxext6  -y

# Copy the current directory contents into the container at the working directory
COPY . .