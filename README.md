# Auto-RITA

                     _              _____  _____ _______       
          /\        | |            |  __ \|_   _|__   __|/\    
         /  \  _   _| |_ ___ ______| |__) | | |    | |  /  \   
        / /\ \| | | | __/ _ \______|  _  /  | |    | | / /\ \  
       / ____ \ |_| | || (_) |     | | \ \ _| |_   | |/ ____ \ 
      /_/    \_\__,_|\__\___/      |_|  \_\_____|  |_/_/    \_

Welcome to Auto-RITA. This utility can be used to automate performance
monitoring while running [Offensive CounterMeasures' RITA
(Real Intelligence Threat Analytics)](https://github.com/ocmdev/rita) platform. Data is collected in
Splunk (running in Docker) and data is reported by collectd.

Auto-RITA can be configured to import and analyze bro logs between any
two dates. While RITA is running information collected via collectd 
will be logged in a local instance of Splunk. It can also collect a 
base system load benchmark before running its RITA processes. 

Currently data must be manually analyzed or exported from Splunk.

Supports hosts running Ubuntu 16.04 LTS.

If python3 is installed then Auto-RITA can install all of the
necessary dependencies.

## Getting Started

### Dependencies
```
collectd
collectd-utils
docker
docker-compose
git
```
       
### Install

Execute: python3 auto-rita.py
Select option "1" to install dependencies. 

#### Usage
```
(Interactive) 		python3 auto-rita.py
(Cron Automation)	python3 auto-rita.py yesterday
```

### TODO

* Implement Splunk Python SDK to automate export of data
* Implement collectd frequency as a variable.
* External config for ease of use
* Fix Known Issues...

### Known Issues

* Docker container may not be running and initialized before program continues with execution.
** Docker is launched in background
** Program currently waits 30 sec before proceeding
