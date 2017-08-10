# Auto-RITA

                     _              _____  _____ _______       
          /\        | |            |  __ \|_   _|__   __|/\    
         /  \  _   _| |_ ___ ______| |__) | | |    | |  /  \   
        / /\ \| | | | __/ _ \______|  _  /  | |    | | / /\ \  
       / ____ \ |_| | || (_) |     | | \ \ _| |_   | |/ ____ \ 
      /_/    \_\__,_|\__\___/      |_|  \_\_____|  |_/_/    \_

Welcome to Auto-RITA. This utility can be used to automate performance
monitoring while running [Offensive CounterMeasures' RITA
(Real Intelligence Threat Analytics)](https://github.com/ocmdev/rita) 
platform. Data is collected in [Splunk (running in Docker)](https://github.com/splunk/docker-splunk/tree/master/enterprise) and 
data is reported by [collectd](https://github.com/collectd/collectd).

Auto-RITA can be configured to import and analyze bro logs between any
two dates. Start and stop time for each RITA import and analyze are 
logged. Outputs time values to CSV when finished. 

Auto-RITA provides options to collect system metrics via
collectd, while RITA is running. System metrics will be logged
in a local instance of Splunk. Also it can collect a base system load
benchmark before running its RITA processes.

Currently splunk data must be manually analyzed or exported.

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
Select option [1] to install dependencies. 

#### Usage
```
(Interactive) 		python3 auto-rita.py
(Cron Automation)	python3 auto-rita.py yesterday

Note: For testing purposes calls to RITA import/analyze are commented out. 
```

### TODO

* Implement Splunk Python SDK to automate export of data
* Implement collectd frequency as a variable.
* External config for ease of use
* Record log dir size (add to CSV)
* Fix Known Issues...

### Known Issues

* Docker container may not be running and initialized before program continues with execution.
** Docker is launched in background
** Program currently waits 30 sec before proceeding

* RITA path must be included as a source in .bashrc
