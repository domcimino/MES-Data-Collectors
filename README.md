# MES-Data-Collectors
A python project I developed in the context of industry 4.0


## Introduction
A data collector written in Python that interfaces with an MQTT broker to access data from CNCS of industrial plants.
I created this project as part of a training internship.

The project has been deliberately simplified compared to the original one, currently used at a manufacturing company. It implements only the basic functionality of the architecture presented in the following diagram.
Below is a prototype industrial environment for running the Python services I developed

## Architecture description (simplified)
Below is a prototype of an industrial environment for running the Python services I developed.

Is an industrial production line of 3 work machines. For each machine, its CNC is shown. Connected to each CNC is a custom C# Service (data collector)  that reads the CNC variables and posts them to an MQTT Broker. Then, the  Python Service I developed is subscribed to the Broker and acts as a data receiver. It processes the received data by using external and configurable Python sub-modules, acting as plug-ins. There is one Python plugin for processing data regarding each CNC. Each Python plugin stores data in the Mysql database. Finally, a MES web application is connected to the DB to read data. 

![enter image description here](https://github.com/domcimino/MES-Data-Collectors/blob/main/resources/architecture.png)

## Benefits 
This architecture can be scaled to many different industrial CNC (and machines) simply by writing ad hoc C# services and Python plug-ins.



# Install, setup, run and test 

## Folder Layout

```
project root directory/
├── main.py                     # Main program (modify parameter according MQTT broker ypu want to use). Implements Python Service in the diagram above
├── mqtt_reader.py              # MQTTReader class manager
├── cnc_classes.json            # Mapping of cnc_id to class_name. Each class acts as plugin for handling CNC values
├── db_config.json              # MySQL connection configuration (modify according your MySQL parameter)
├── mysql_db_manager.py         # MySqlDbManager class
├── database,sql                # DB creation scriptt (run it agaist your MySQL to create the db)
├── plugins/                    # CNC classes (plugins implementation. Theuìy are loaded dynamically)
│   ├── __init__.py
│   ├── CNCTypeA.py             # Prototype of class impementing plugin handling CNC001
│   └── CNCTypeB.py             # Prototype of class impementing plugin handling CNC000

```

## Requiremets
1. Python installed into your PC.
2. A MySQL server access

## Install, setup, and run
1. Unzip the package into a folder and prompt on it
2. Modify **db_config.json** according to your DB configuration
3. Execute **database,sql** to create the DB schema

Optionaly modify **main.py** if you need to use a differnt Broker. By default a free one is used

Finally:


```
pip install paho-mqtt (only once)
python main.py

```


## Test the application
To test the application, you need to send the following data to the broker:

{"cnc_id": "CNC001","part_program": "program_01","timestamp": "1747379028","payload":{"status": "running","spin":200,"X-Axis":30,"Y-Axis":80}}

Sample and valid data are in **sample_data.json**

In a real scenario, data was submitted by the C # Service.

Note: Data must be in a valid JSON format containing 4 fields: **cnc_id**, **part_program**, **timestamp**, and **payload**. Since there are CNCS with different characteristics and that handle different variables, the field payload is itself a valid JSON with arbitrary keys/values ​​(containing values ​​from a specific CNC).

