# OpenDXL-MISP-IntelMQ-Output
This use case is focusing on the automated real-time threat sharing with MISP (Malware Intelligence Sharing Platform), 
orchestration tool (IntelMQ) and OpenDXL.
IntelMQ is used to collect data from the Malware Intelligence Sharing Platform (MISP), to parse and push intelligence via OpenDXL 
to e.g. 

* run multiple McAfee Active Response searches across multiple DXL fabrics. ([Link]())
* update McAfee TIE Server (Malicious Hashes) ([Link]())
* update McAfee Web Gateways (IP subscribed Lists) ([Link]())
* update Forcepoint Firewalls ([Link]())
* update Check Point Firewalls ([Link]())

## Component Description

**MISP** threat sharing platform is a free and open source software helping information sharing of threat and cyber security indicators.
https://github.com/MISP/MISP

**IntelMQ** is an orchestration solution for IT security teams (CERTs, CSIRTs and abuse departments) for collecting and processing 
security feeds. It's a community driven initiative called IHAP (Incident Handling Automation Project) which was conceptually designed by
European CERTs/CSIRTs. Its main goal is to give to incident responders an easy way to collect & process threat intelligence.
https://github.com/certtools/intelmq

## Prerequisites
MISP platform installation ([Link](https://github.com/MISP/MISP)) (tested with MISP 2.4.70)

PyMISP library installation ([Link](https://github.com/CIRCL/PyMISP))

IntelMQ installation ([Link](https://github.com/certtools/intelmq))

IntelMQ Manager installation ([Link](https://github.com/certtools/intelmq-manager))

OpenDXL Python installation
1. Python SDK Installation ([Link](https://opendxl.github.io/opendxl-client-python/pydoc/installation.html))
2. Certificate Files Creation ([Link](https://opendxl.github.io/opendxl-client-python/pydoc/certcreation.html))
3. ePO Certificate Authority (CA) Import ([Link](https://opendxl.github.io/opendxl-client-python/pydoc/epocaimport.html))
4. ePO Broker Certificates Export ([Link](https://opendxl.github.io/opendxl-client-python/pydoc/epobrokercertsexport.html))

## Configuration
The IntelMQ Manager can be access via http://ip-address/. It is possible to create under configuration specific Collectors, 
Parsers, Experts and Outputs. 

For this particular use case we will collect data from the Malware Intelligence Sharing Platform (MISP) based on specific tags. 
We will parse the information and use OpenDXL as an output to share information across multiple DXL fabrics and platforms.
OpenDXL as an output is not natively configured. To add OpenDXL we first need to create a new BOT in /opt/intelmq/etc/BOTS.

Add under Output the new DXL item e.g:

``"McAfee DXL": {
 "description": "This output will generate a DXL message.",
 "module": "intelmq.bots.outputs.dxl.output",
 "parameters": {
 "file": "/opt/intelmq/var/lib/bots/file-output/dxl_events.txt",
 "hierarchical_output": false
 }
 },``

![31_misp_intelmq](https://cloud.githubusercontent.com/assets/25227268/25067193/e737ca0c-223b-11e7-8a5a-6eaa5c47a228.PNG)

Next we need to generate a bot output file in the /usr/local/bin library. This output file is for one OpenDXL output.
If more outputs are needed just duplicate the file and change the intelmq output target.

``#!/usr/bin/python3.4
#EASY-INSTALL-ENTRY-SCRIPT:
'intelmq==1.0.0.dev6','console_scripts','intelmq.bots.outputs.dxl.outputc1'
__requires__ = 'intelmq==1.0.0.dev6'
import sys
from pkg_resources import load_entry_point
if __name__ == '__main__':
 sys.exit(
 load_entry_point('intelmq==1.0.0.dev6', 'console_scripts', 'intelmq.bots.outputs.dxl.outputc1')()
 )``

Next we need to modify the entry point file.

> vim.tiny /usr/local/lib/python3.4/dist-packages/intelmq-1.0.0.dev6.egg-info/entry_points.txt

Add the new BOTS.

`intelmq.bots.outputs.dxl.outputc1 = intelmq.bots.outputs.dxl.outputc1:BOT.run`

We can start using a simple DXL script to publish collected MISP information on a specific DXL topic. 
Best starting point is the event_example.py file in the OpenDXL sample folder.

> cp /dxlclient-python-sdk-3.0.1.203/sample/basic/event_example.py /usr/local/lib/python3.4/distpackages/intelmq/bots/outputs/dxl/example_test.py

Finally we need to create a BOT to execute the OpenDXL python script.

> vim.tiny /usr/local/lib/python3.4/distpackages/intelmq/bots/outputs/dxl/output1.py

The output1.py script includes a specfic row to execute the OpenDXL script.

'subprocess.call(['/usr/bin/python','/usr/local/lib/python3.4/dist-packages/intelmq/bots/outputs/dxl/example_test.py', event_data])'

The subprocess.call is necessary to execute the OpenDXL script with Python 2.7 (IntelMQ uses Python 3.x). 
Please make sure to use the full path name in the dxlclient.config file.

