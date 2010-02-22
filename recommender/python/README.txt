
SETUP ON MAC OS

install tornado
---------------
sudo easy_install setuptools pycurl==7.16.2.1 simplejson
wget http://www.tornadoweb.org/static/tornado-0.2.tar.gz
tar xvzf tornado-0.2.tar.gz
cd tornado-0.2
python setup.py build
sudo python setup.py install

install amqp
------------
sudo port install rabbitmq-server
sudo easy_install -U amqplib

run demo
--------

1. open a terminal and run
sudo rabbitmq-server

2. open another terminal and run
python webserver.py

3. open another terminal and run
python stupid_client.py

4. point a web browser to
http://localhost:8888/search?q=UMMAGUMMA
(it will sit there and do nothing)

In terminal 3 you should see something like:
received message {"body": {"web-query": "UMMAGUMMA"}, "message_id": "1266598119.42"}
your answer?

If you enter some text and press enter, you should see
your answer appear in the browser window


Notes:
------

Example google graph api 'otherme' call:
curl 'http://socialgraph.apis.google.com/otherme?pretty=1&q=http://www.google.com/profiles/matteo.caprari'

Testing:
========

End to end system test, also verifies that clients receive the correct response

python webserver.py
python query_expander.py --social_graph_api_url=http://localhost:1234
python random_responder.py
python bogus_graph_api.py
python brute.py
