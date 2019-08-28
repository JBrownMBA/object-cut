FROM python:3.7
ADD . /srv/object_cut
WORKDIR /srv/object_cut
RUN pip install --upgrade pip
RUN pip3 install -r requirements.lock
CMD uwsgi --ini object_cut.ini