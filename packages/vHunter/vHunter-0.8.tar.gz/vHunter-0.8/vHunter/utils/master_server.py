import logging
import time
import json

from tornado.web import RequestHandler
from tornado.template import Template
from singleton_decorator import singleton

from vHunter.workers import agregate


@singleton
class SlavesContainer:
    def __init__(self):
        self.slaves = {}

    def set_slave(self, name, ip):
        if self.slaves.get(name) is None:
            self.slaves[name] = {}
        self.slaves[name]['ip'] = ip
        self.slaves[name]['update_time'] = time.time()

    def set_last_notify(self, name, data):
        self.slaves[name]['notify_time'] = time.time()
        self.slaves[name]['data'] = data

    def get_slaves(self):
        return self.slaves


class PingServer(RequestHandler):

    async def get(self):
        template = Template("""
        <html>
        <head>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css" integrity="sha384-rwoIResjU2yc3z8GV/NPeZWAv56rSmLldC3R/AZzGRnGxQQKnKkoFVhFQhNUwEyJ" crossorigin="anonymous">
            <script src="https://code.jquery.com/jquery-3.1.1.slim.min.js" integrity="sha384-A7FZj7v+d/sdmMqp/nOQwliLvUsJfDHW+k9Omg/a/EheAdgtzNs3hpfag6Ed950n" crossorigin="anonymous"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/tether/1.4.0/js/tether.min.js" integrity="sha384-DztdAPBWPRXSA/3eYEEUWrWCy7G5KFbe8fFjk5JAIxUYHKkDx6Qin1DkWx51bBrb" crossorigin="anonymous"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/js/bootstrap.min.js" integrity="sha384-vBWWzlZJ8ea9aCX4pEW3rVHjgjt7zpkNpZk+02D9phzyeVkE+jo0ieGizqPLForn" crossorigin="anonymous"></script>
        </head>
        <body>
            <table class="table">
        <thead>
        <tr>
            <th>#</th>
            <th>name</th>
            <th>ip</th>
            <th>Last update</th>
            <th>Last notify</th>
            <th>Last data</th>
        </tr>
        </thead>
            {% set i = 1 %}
            {% for slave_name, slave_dict in slaves.items() %}
            <tr>
                <th scope="row">{{ i }}</td>
                <td>{{ slave_name }}</td>
                <td>{{ slave_dict['ip'] }}</td>
                <td>{{ datetime.datetime.fromtimestamp(slave_dict['update_time']) }}</td>
                <td>{{ datetime.datetime.fromtimestamp(slave_dict['notify_time']) if 'notify_time' in slave_dict else 'Not yet send' }}</td>
                <td>{{ slave_dict.get('data') or 'Not yet send' }}</td>
            </tr>
            {% set i = i + 1 %}
            {% end %}
            </table>
    </body>
        </html>
        """)
        self.write(template.generate(slaves=SlavesContainer().get_slaves()))

    async def post(self):
        name = self.request.uri.split("/")[2]
        ip = self.request.remote_ip
        SlavesContainer().set_slave(name, ip)
        logging.info("%s is pinging from %s, ponging right away" % (name, ip))
        self.write("pong")


class AgregateServer(RequestHandler):

    async def post(self):
        name = self.request.uri.split("/")[2]
        data = json.loads(self.request.body)
        SlavesContainer().set_last_notify(name, data)
        agregate(data["notifier_class"], data["receivers"], data["vulnerabilities"])
