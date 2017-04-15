# -*- coding: utf-8 -*-
import io
import re
import subprocess

from intelmq.lib.bot import Bot

class FileOutputBot(Bot):

    def process(self):
        event = self.receive_message()
        event_data = event.to_json(hierarchical=self.parameters.hierarchical_output)
        sha1 = re.findall('([a-f0-9]{40})', event_data)[0]
        #id = re.findall('.*view\x2f(\d+)', event_data)[0]
        #ip = re.findall('((?:[0-9]{1,3}\.){3}[0-9]{1,3})', event_data)[0]
        subprocess.call(['/usr/bin/python','/usr/local/lib/python3.4/dist-packages/intelmq/bots/outputs/dxl/example_test.py', sha1])
        self.acknowledge_message()

BOT = FileOutputBot
