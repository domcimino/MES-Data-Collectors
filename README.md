# MES-Data-Collectors
A python project I developed in the context of industry 4.0


## Introduction
A data collector written in Python that interfaces with an MQTT broker to access data from CNCS of industrial plants.
I created this project as part of a training internship.

## Architecture 
Below is an example of an industrial production line of 3 work machines. For each machine, its CNC is shown. Connected to each CNC is a custom C# Service (data collector)  that reads the CNC variables and posts them to an MQTT Broker. Then, the  Python Service I developed is subscribed to the Broker and acts as a data receiver. It processes the received data by using external and configurable Python sub-modules, acting as plug-ins. There is one Python plugin for processing data regarding each CNC. Each Python plugin stores data in the Mysql database. Finally, a MES web application is connected to the DB to read data. 

![enter image description here](https://github.com/domcimino/MES-Data-Collectors/blob/main/resources/architecture.png)

## Benefits 
This architecture can be scaled to many different industrial CNC (and machines) simply by writing ad hoc C# services and Python plug-ins.





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


# Install and Run
```
pip install
python data_collector.py

```
