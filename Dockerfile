# Testrunner Slave
# Needs API, Caseworker & Public running in containers
# Needs Chrome & ChromeDriver binary
# Needs trade-remedies-test requirements.txt installed in Python3 (??? Or does this magically work?)

FROM ubuntu:18.04

WORKDIR /testrunner

RUN apt-get update
RUN apt-get install -y python3-pip
COPY ./requirements.txt /testrunner/requirements.txt
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

# Install ChromeDriver
RUN apt-get install -y wget
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get update
RUN apt-get install -y google-chrome-stable
RUN wget --no-cache -N http://chromedriver.storage.googleapis.com/70.0.3538.16/chromedriver_linux64.zip -P ./
RUN apt-get install -y unzip
RUN unzip ./chromedriver_linux64.zip -d ./
RUN chmod +x ./chromedriver
RUN mv -f ./chromedriver /usr/bin/chromedriver

# Install SocketServer
RUN pip3 install --trusted-host pypi.python.org execnet
RUN wget --no-cache -N https://bitbucket.org/hpk42/execnet/raw/2af991418160/execnet/script/socketserver.py -P ./

# Install Docker CLI
RUN wget --no-cache -N https://download.docker.com/linux/static/stable/x86_64/docker-18.09.3.tgz -P ./
RUN tar -xvzf ./docker-18.09.3.tgz -C ./
RUN mv -f ./docker/docker /usr/bin/docker

## Install dockerize https://github.com/jwilder/dockerize
#ENV DOCKERIZE_VERSION v0.6.1
#RUN wget -q https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
#    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz
#
## Wait for application under test to come online
#RUN dockerize -timeout 120s -wait tcp://localhost:8000 -wait tcp://localhost:8001  -wait tcp://localhost:8002

# Expose SocketServer
EXPOSE 8888

CMD ["python3", "socketserver.py"]

# docker build --tag=testrunner .
# docker run -it -v /var/run/docker.sock:/var/run/docker.sock --net=host testrunner
