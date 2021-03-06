FROM python
USER root
VOLUME /data
WORKDIR /data
COPY ./ /data
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN cd /data && pip install --upgrade pip && pip install -r /data/requirements.txt -i https://mirrors.aliyun.com/pypi/simple
EXPOSE 9090
CMD /bin/bash -c 'python /data/app_server.py --monitor=on --port=9090 --log_file_prefix=/data/logs/openTest.log --log-file-max-size=10000000 --log-file-num-backups=3'