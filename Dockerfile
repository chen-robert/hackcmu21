FROM nikolaik/python-nodejs:latest

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

RUN cd static && yarn install --frozen-lockfile && yarn && yarn build && yarn cache clean && rm -rf node_modules

CMD [ "./run.sh" ]
