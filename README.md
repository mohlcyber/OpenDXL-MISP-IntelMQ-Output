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

![34_misp_intelmq](https://cloud.githubusercontent.com/assets/25227268/25070153/fd670904-2296-11e7-82c1-7c30511ca72f.PNG)

## Component Description

**MISP** threat sharing platform is a free and open source software helping information sharing of threat and cyber security indicators.
https://github.com/MISP/MISP

**IntelMQ** is an orchestration solution for IT security teams (CERTs, CSIRTs and abuse departments) for collecting and processing 
security feeds. It's a community driven initiative called IHAP (Incident Handling Automation Project) which was conceptually designed by
European CERTs/CSIRTs. Its main goal is to give to incident responders an easy way to collect & process threat intelligence.
https://github.com/certtools/intelmq

## Prerequisites
Since IntelMQ is supported on Linux only, this solution only runs on Linux. The python dependencies have
to be installed on a linux system.

MISP platform installation ([Link](https://github.com/MISP/MISP)) (tested with MISP 2.4.70)

PyMISP library installation ([Link](https://github.com/CIRCL/PyMISP))or install dependencies
using the requirements.txt file as mentioned below.

IntelMQ installation ([Link](https://github.com/certtools/intelmq))

IntelMQ Manager installation ([Link](https://github.com/certtools/intelmq-manager))

Download the [Latest Release](https://github.com/mohl1/OpenDXL-MISP-IntelMQ-Output/releases)
   * Extract the release .zip file
   
OpenDXL Python installation
1. Python SDK Installation ([Link](https://opendxl.github.io/opendxl-client-python/pydoc/installation.html))
    Install the required dependencies with the requirements.txt file:
    ```sh
    $ pip install -r requirements.txt
    ```
    This will install the dxlclient, pymisp, and intelmq modules.
    The solution has been tested with python intelmq library version 1.0.0.dev6.  
2. Certificate Files Creation ([Link](https://opendxl.github.io/opendxl-client-python/pydoc/certcreation.html))
3. ePO Certificate Authority (CA) Import ([Link](https://opendxl.github.io/opendxl-client-python/pydoc/epocaimport.html))
4. ePO Broker Certificates Export ([Link](https://opendxl.github.io/opendxl-client-python/pydoc/epobrokercertsexport.html))

## Configuration
The IntelMQ Manager can be access via http://ip-address/. It is possible to create under configuration specific Collectors, 
Parsers, Experts and Outputs. 

For this particular use case we will collect data from the Malware Intelligence Sharing Platform (MISP) based on specific tags. 
We will parse the information and use OpenDXL as an output to share information across multiple DXL fabrics and platforms.
OpenDXL as an output is not natively configured. 

### example_test.py

Change the CONFIG_FILE path in the example_test.py file

`CONFIG_FILE = "/path/to/config/file"`

### IntelMQ
To add OpenDXL we first need to create a new BOT in /opt/intelmq/etc/BOTS.

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

Next we need to add / modify the entry point file.

> /usr/local/lib/python3.4/dist-packages/intelmq-1.0.0.dev6.egg-info/entry_points.txt

Add the new BOTS.

e.g. `intelmq.bots.outputs.dxl.outputc1 = intelmq.bots.outputs.dxl.outputc1:BOT.run`

We can start using a simple DXL script to publish collected MISP information on a specific DXL topic. 

> /usr/local/lib/python3.4/distpackages/intelmq/bots/outputs/dxl/example_test.py

Finally we need to create a BOT to execute the OpenDXL python script above.

> /usr/local/lib/python3.4/distpackages/intelmq/bots/outputs/dxl/output1.py

The output1.py script includes a specific part to execute the OpenDXL script.

`subprocess.call(['/usr/bin/python','/usr/local/lib/python3.4/dist-packages/intelmq/bots/outputs/dxl/example_test.py', event_data])`

The subprocess.call is necessary to execute the OpenDXL script with Python 2.7 (IntelMQ uses Python 3.x). 
Please make sure to use the full path name in the dxlclient.config file.

### IntelMQ Manager
1. Add a new MISP collector. Change the following information:
* MISP_Key (MISP automation)
* MISP_tag_proccessed (new tag that should be assigned to the MISP event)
* MISP_tag_to_process (tagged event that should be processed)
* MISP_url
* MISP_verify (optional trusted/untrusted SSL certificates check)

![32_misp_intelmq](https://cloud.githubusercontent.com/assets/25227268/25067469/09c9c9c2-2245-11e7-8a38-f0279eb4f088.PNG)

2. Add the MISP parser to the configuration page.

3. Add the McAfee DXL output and change the module name to the module you want to execute.

4. Link the MISP collector with the parser and the output and safe the configuration.

5. Start the BOTS under the management page.

IntelMQ collect the tagged event and publish this information via DXL. It is also possible to filter the data first before it gets send via DXL (e.g. filter out Hashes, IPs and Domains).

## Summary
MISP contains global, community and locally produced intelligence that can be used with IntelMQ and OpenDXL for automated threat hunting and threat response.

![33_misp_intelmq](https://cloud.githubusercontent.com/assets/25227268/25067556/eb551ed0-2247-11e7-830e-4422655f561c.PNG)

