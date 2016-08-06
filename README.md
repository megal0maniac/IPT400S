# IPT400S
## Remote weather station
This repository forms the software portion of my B-Tech project.
The aim is to build a remote weather station, with many features lacking in consumer weather stations. In practice, there will be a remote unit (located with the sensors) and a local unit (server) in some safe location.

## Principle of operation
The remote unit will record data, save it to databases and occasionally back-up to non-volatile storage (micro SD card).
At some pre-determined interval, the remote unit will connect to the local unit and synchronise the databases.
The local unit will read the databases and present the data to the user through a web-based interface. Data will be presented using various graphs and charts with configurable granularity and time-windows.

## Main technologies used
Microcontroller for interfacing with sensors
Single-board computer for reading data from microcontroller and pushing it to the server
Standard desktop computer as the server
Python for most of the logic
Rsync for synchronisation
CherryPy for API web-server (reading databases, data manipulation)
Lighttpd as main and proxying web-server
