# FROM python:3
# FROM selenium/standalone-chrome
FROM python:3.7-alpine

# USER root
# RUN wget https://bootstrap.pypa.io/get-pip.py
# RUN sudo python3 get-pip.py
# RUN python3 -m pip install selenium

# install chromium
RUN apk add --no-cache  chromium --repository=http://dl-cdn.alpinelinux.org/alpine/edge/main

ENV CHROME_BIN=/usr/bin/chromium-browser
ENV CHROME_PATH=/usr/lib/chromium/
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=1

RUN apk add unzip nano bash chromium-chromedriver

ADD webscreenshot.py /
ADD takescreenshot.py /
# ADD chromedriver /

# RUN echo "http://dl-8.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories \
#   && apk update \
#   && apk add py3-numpy py3-scipy

# RUN apk add libc-dev
# RUN apk add build-essential

RUN apk --no-cache add musl-dev linux-headers g++
RUN pip install --upgrade pip

RUN pip install numpy
# RUN pip install scipy

# RUN apk add --update py-pip

RUN apk add --no-cache --virtual .pynacl_deps build-base libffi-dev openssl-dev
RUN pip install azure.storage.blob
RUN pip install bson
RUN pip install pymongo
# RUN pip install wheel
RUN pip install urllib3
RUN pip install selenium
# RUN pip install reportlab
# RUN pip install svglib
# RUN pip install scipy

# # Install Chrome
# RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

CMD [ "python", "./takescreenshot.py" ]