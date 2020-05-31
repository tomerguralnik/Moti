FROM python:3.8-slim-buster
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY moti moti
COPY scripts/wait-for-it.sh wait-for-it.sh
RUN apt-get update
RUN apt-get install -y npm
RUN npm install -g npm@latest
WORKDIR moti/moti_web
RUN npm install react bootstrap react-dom react-scripts react-router-dom jquery
RUN npm run build
WORKDIR /