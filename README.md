# MES-Data-Collectors
A python project I developed in the context of industry 4.0


## Introduction
A data collector written in Python that interfaces with an MQTT broker to access data from CNCS of industrial plants. I created this project as part of a training internship for a HORIZON 2020 project owned by a manufacturing company.

The project has been deliberately simplified compared with the original one. This simplified release just implements only the basic functionalities of the architecture presented in the following diagram. Many features, such as authentication and security, were intentionally omitted.

## Architecture description (simplified)
Below is a prototype diagram of an industrial environment to explain the roles of the Python services I developed.

The diagram shows a basic production line composite of 3 work machines. For each machine, its CNC is also shown. 

Connected to each CNC is a custom C# Service (data collector)  that reads the CNC variables and posts them to an MQTT Broker. An example of this kind of service is [here](https://github.com/rcarvello/montronix_data_collectors)

Then, the  Python Service I developed is subscribed to the Broker and acts as a data receiver. It processes the received data by using external and configurable Python sub-modules, acting as plug-ins. There is one Python plugin for processing data regarding each CNC. Each Python plugin stores data in the MySQL database. Finally, a MES web application is connected to the DB to read data. 

![enter image description here](https://github.com/domcimino/MES-Data-Collectors/blob/main/resources/architecture.png)




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
├── cnc_service_emulator.py     # A very simple C# service emulator sending data to the broker
├── plugins/                    # CNC classes (plugins implementation. Theuìy are loaded dynamically)
│   ├── __init__.py
│   ├── cnc_plugin_interface.py # Plugin Interface (all custom plugins must iplements it)
│   ├── CNCTypeA.py             # Prototype of class impementing plugin handling CNC001
│   └── CNCTypeB.py             # Prototype of class impementing plugin handling CNC000

```

## Requiremets
1. Python installed into your PC.
2. A MySQL server access

## Install and setup
1. Unzip the package into a folder and prompt on it
2. Modify **db_config.json** according to your DB configuration
3. Execute **database,sql** to create the DB schema

Optionaly modify **main.py** if you need to use a differnt Broker. By default a free one is used

Finally go into the project directory and execute:

```
pip install paho-mqtt 
```

## Optional Settings
Depending on your MySQL and Python configuration, you may get the following error on MySQL authentication:

**caching_sha2_password** cannot be loaded

To resolve it, you need to log in to MySQL as root and run

```
cd "C:\Program Files\MySQL\MySQL Server 8.0\bin"

C:\Program Files\MySQL\MySQL Server 8.0\bin> mysql -u root -p
Enter password: *********
```

and run
```
mysql> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'newrootpassword';

Query OK, 0 rows affected (0.10 sec)

mysql> exit
```
For Python:

```
pip install mysql-connector-python
```


## Run and the application
To test the application, you need to send the following data to the broker:

```
{"cnc_id": "CNC001","part_program": "program_01","timestamp": "1747379028","payload":{"status": "running","spin":200,"X-Axis":30,"Y-Axis":80}}

```
Sample and valid data are in **sample_data.json**

In a real Industry 4.0 scenario, data was sent to the Broker from C# services connected to the CNC for variable retrieval.
Nevertheless, it is possible to send data to the broker manually using a simple MQTT client such as mqttx.app (https://mqttx.app).

I also provide you with a very simple **cnc_service_emulator.py** you can run to automatically send data from **sample_data.json** to the broker.

So to run the application, first run the Python Service


```
python main.py

```

Then start the emulator to send sample CNC data to the broker


```
python cnc_service_emulator.py

```

You should see:
1. Python service successfully connected to MySQL and Broker
2. It receives data
3. For each data it calls the appropriate Plugin to store it into the database
4. DataBase is populated with the data received

If you try to send not allowed data you should also see the service raise an exception because data must be in a valid JSON format containing 4 fields: 

**cnc_id**, **part_program**, **timestamp**, and **payload**. 

Since there are CNCS with different characteristics and that handle different variables, the field payload is itself a valid JSON with arbitrary keys/values ​​(containing values ​​from a specific CNC).

## Benefits 
Main benefits are:
1. The architecture can be easily scaled to many work machines by adding, for each work node, a custom C# service and Python plugin.
2. It is evident how the application is strongly decoupled from the hardware.
