# -*- coding: utf-8 -*-
import io
import re
import subprocess

from intelmq.lib.bot import Bot

class FileOutputBot(Bot):

    def process(self):
        event = self.receive_message()
        event_data = event.to_json(hierarchical=self.parameters.hierarchical_output)
        subprocess.call(['/usr/bin/python','/usr/local/lib/python3.4/dist-packages/intelmq/bots/outputs/dxl/example_test.py', event_data])
        self.acknowledge_message()

BOT = FileOutputBot
