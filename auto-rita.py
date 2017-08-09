#!/usr/bin/python

import sys, getopt, datetime, string, time, random, subprocess, os

rita_path = '~/rita/'
bro_path = '/var/log/bro/'
default_baseline = 30 #in seconds

def main():
  mode = -1
  while(mode < 0):

    print ("                     _              _____  _____ _______       \n          /\        | |            |  __ \|_   _|__   __|/\    \n         /  \  _   _| |_ ___ ______| |__) | | |    | |  /  \   \n        / /\ \| | | | __/ _ \______|  _  /  | |    | | / /\ \  \n       / ____ \ |_| | || (_) |     | | \ \ _| |_   | |/ ____ \ \n      /_/    \_\__,_|\__\___/      |_|  \_\_____|  |_/_/    \_ \n\n######################################################################\n\nWelcome to Auto-RITA. This utility can be used to automate performance\nmonitoring while running Offensive CounterMeasures' RITA\n(Real Intelligence Threat Analytics) platform. Data is collected in\nSplunk (running in Docker) and data is reported by collectd.\n\n######################################################################\n\n[1] Install/Reinstall Dependencies\n[2] Run and monitor RITA input & analyze (with baseline measurement)\n[3] Run and monitor RITA input & analyze\n[4] Run RITA input & analyze\n[5] Exit\n")

    mode = input("Enter your choice: ")

    #print ("You have selected " + mode)
    if(mode == "1" or mode == "[1]"):
      install()
      mode = -1
    elif(mode == "2" or mode == "[2]"):
      mode = 2
      baseline = baseline_prompt()
      range = range_prompt()

      print ("Going to run baseline for " + str(baseline) + " seconds. \nRITA will run from " + str(range['start_date']) + " to " + str(range['end_date']) + ". Performance will be monitored")
      start_monitoring(baseline)
      run_rita(range['start_date'], range['end_date'])
      stop_monitoring()

    elif(mode == "3" or mode == "[3]"):
      mode = 3
      range = range_prompt()
      print ("No baseline will be collected. \nRITA will run from " + str(range['start_date']) + " to " + str(range['end_date']) + ". Performance will be monitored")
      start_monitoring()
      run_rita(range['start_date'], range['end_date'])
      stop_monitoring()
    elif(mode == "4" or mode == "[4]"):
      mode = 3
      range = range_prompt()
      print ("RITA will run from " + str(range['start_date']) + " to " + str(range['end_date']) + ".")
      run_rita(range['start_date'], range['end_date'])
    elif ("exit" in mode or mode == "5" or mode == "[5]"):
      print( "Exiting!")
      sys.exit()
    else:
      print( "Invalid Input!\n\n")
      mode = -1

def install():

  print ("\n######################################################################\n\nSelected:\n[1] Install/Reinstall Dependencies\n")

  print('Welcome to Auto-RITA. We need to install a few dependencies.\nThis will install collectd, docker, docker-compose, and git.\n ')
  user = input("Press [Enter] to proceed...")
  print ("\nInstalling your stuff!")
  runCommand('sudo apt update')
  runCommand('sudo apt-get install collectd collectd-utils docker docker-compose git')
  print('\nDependencies installed!!')

  print('We now need to configure our configs.')
  user = input("Press [Enter] to proceed...")

  runCommand('sudo rm /etc/collectd/collectd.conf')
  
  ln_command = 'sudo ln -sf '+ os.getcwd() + '/configs/collectd.conf /etc/collectd/collectd.conf'
  #print(ln_command)
  runCommand(ln_command)
  runCommand('sudo service collectd stop')
  runCommand('git clone https://github.com/Nexinto/collectd.git docker-splunk/splunk/etc/apps/collectd')

def range_prompt():
  yesterday = (datetime.date.today() - datetime.timedelta(days=1))
  start_date = input("Please enter your start date (yyyy-mm-dd) [" + str(yesterday) + "]: ")
  if not start_date:
    start_date = yesterday
  else:
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()

  end_date = input("Please enter your end date (yyyy-mm-dd) [" + str(yesterday) + "]: ")
  if not end_date:
    end_date = (datetime.date.today() - datetime.timedelta(days=1))
  else:
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

  return {'start_date':start_date, 'end_date':end_date}

def baseline_prompt():
  time = -1
  while (time < 0):
    time = input("How long (in seconds) do you want to collect system baseline metrics? ["+str(default_baseline) +"] ")
    if not time:
      time = default_baseline
    else:
      try: 
          time = int(time)
      except ValueError:
        print("Please enter an integer!")
        time = -1
  #print(type(time))
  #print("Run baseline for " + str(time) + " seconds.")
  return time;

def start_monitoring(baseline = 0):
  print("Starting the monitoring process.")
  runCommand("sudo docker-compose -f ./docker-splunk/docker-compose.yml up -d")
  time.sleep(30)
  runCommand("sudo service collectd start")

  print("Monitoring has started.\nView progress at http://localhost:8000/")
  
  if (baseline > 0):
    print("Collecting baseline.")
    #time.sleep(baseline)
    items = list(range(0,baseline))
    l = len(items)

    printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 42)
    for i, item in enumerate(items):
        # Do stuff...
        time.sleep(1)
        # Update Progress Bar
        printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 42)

    print("Baseline collected.")
  
def stop_monitoring():
  print("Stopping the monitoring process.")
  runCommand("sudo service collectd stop")

  time.sleep(3)
  print("Monitoring has stop.\n\n\n##############################################\n### View results at http://localhost:8000/ ###\n##############################################\n") 
  user = input("Press [Enter] to quit and stop splunk...")
  print("Closing Splunk...\n") 
  runCommand("sudo docker-compose -f ./docker-splunk/docker-compose.yml down")
  time.sleep(3)

def run_rita(start_date, end_date):
  """
    Call to run RITA import and analyze on all logs from start_date to end_date
    @params:
        start_date  - Required  : day to start processing logs (datetime.date)
        end_date    - Required  : day to stop processing logs (datetime.date)
    """
  print('Starting RITA!')

  if (start_date == datetime.date.today()):
    print ('Today\'s logs are (likely) not ready for import')
    sys.exit()
  elif (end_date == (datetime.date.today() - datetime.timedelta(days=1)) and start_date > end_date):
    print ('The start date must be before today\'s date!')
    sys.exit()
  elif (end_date > datetime.date.today()):
    print ('The end date must be before today\'s date!')
    sys.exit()
  elif (start_date > end_date):
    print ('The start date must be before the end date!')
    sys.exit()

  print ('Start date is ', start_date.strftime('%Y-%m-%d'))
  print ('End date is ', end_date.strftime('%Y-%m-%d'))
  print ('\n')

  dates = [];

  d = start_date
  delta = datetime.timedelta(days=1)
  while d <= end_date:
    #print d.strftime("%Y-%m-%d")
    dates.append(d.strftime("%Y-%m-%d"))
    d += delta

  #print(dates[0:])
  csv_output = 'day_of_logs,import_start_time,import_finish_time,analyze_start_time,analyze_finish_time\n'
  for i in dates:
    ### Import
    command = rita_path + 'rita import -i ' + bro_path + i + '/ -d ' + i
    time_t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    csv_output = csv_output + i + ',' + time_t + ','

    print ('Import on ' + i + ' is starting at ' + time_t)
    print ('  ' + command)
    ### RUN command
    time.sleep(random.randint(0,5))
    #runCommand(command)
    ### Command finished
    time_t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    csv_output = csv_output + time_t + ','

    print ('Import on ' + i + ' finished at ' + time_t)



    ### Analyze
    command = rita_path + 'rita analyze -d ' + i
    time_t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    csv_output = csv_output + time_t + ','

    print ('Analyze on ' + i + ' is starting at ' + time_t)
    print ('  ' + command)
    ### RUN command
    time.sleep(random.randint(0,5))
    #runCommand(command)
    ### Command finished
    time_t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    csv_output = csv_output + time_t + '\n'

    print ('Analyze on ' + i + ' finished at ' + time_t + '\n')


  print ('CSV output:\n' + csv_output)
  file_name = "./output/times_" + datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + ".csv"
  text_file = open(file_name, "w")
  text_file.write("%s" % csv_output)
  text_file.close()

def runCommand (command):

  command_list = command.split()
  #print(command_list)

  try:
    # Will requier user to input sudo password. They should be shown the command
    # that will run
    if 'apt' in command:
      print (command)

    subprocess.run(command_list, check=True)
    
  except subprocess.CalledProcessError as err:
    print('ERROR:', err)


def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()


if __name__ == "__main__":
  if(len(sys.argv[0:]) > 1):
    if(sys.argv[1] == 'yesterday'):
      mode = 3
      yesterday = (datetime.date.today() - datetime.timedelta(days=1))
      print ("RITA will process yesterday's logs.")
      run_rita(yesterday, yesterday)
      exit(0)
    else:
      print('Unknown Parameter! Ignoring!')
  main()



