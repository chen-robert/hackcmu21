FROM tiangolo/uwsgi-nginx:python3.9

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -
RUN DEBIAN_FRONTEND=noninteractive apt-get install -qy nodejs

RUN curl -sL https://dl.yarnpkg.com/debian/pubkey.gpg | gpg --dearmor | tee /usr/share/keyrings/yarnkey.gpg >/dev/null && \
	echo "deb [signed-by=/usr/share/keyrings/yarnkey.gpg] https://dl.yarnpkg.com/debian stable main" | tee /etc/apt/sources.list.d/yarn.list && \
	apt-get update && apt-get install yarn && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY static static

RUN cd static && yarn install --frozen-lockfile && yarn && yarn build && yarn cache clean && rm -rf node_modules

COPY . .

RUN mv /entrypoint.sh /uwsgi-nginx-entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]

CMD [ "./run.sh" ]
