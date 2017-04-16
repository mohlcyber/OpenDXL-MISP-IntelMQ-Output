import logging
import os
import sys
import time
from threading import Condition

from dxlclient.callbacks import EventCallback
from dxlclient.client import DxlClient
from dxlclient.client_config import DxlClientConfig
from dxlclient.message import Event

# Configure local logger
logging.getLogger().setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

# The topic to publish to
EVENT_TOPIC = "/intelmq/customer1/test"

# Condition/lock used to protect changes to counter
event_count_condition = Condition()

# Create DXL configuration from file
CONFIG_FILE = "/path/to/config/file"
config = DxlClientConfig.create_dxl_config_from_file(CONFIG_FILE)

# Create the client
with DxlClient(config) as client:

    # Connect to the fabric
    client.connect()

    # Create and add event listener
    class MyEventCallback(EventCallback):
        def on_event(self, event):
            with event_count_condition:
                # Print the payload for the received event
                print "Received event: " + event.payload.decode()

    # Register the callback with the client
    client.add_event_callback(EVENT_TOPIC, MyEventCallback())

    # Loop and send the events
    event = Event(EVENT_TOPIC)
    event.payload = str(sys.argv[1]).encode()
    client.send_event(event)
