# cpu monitor
Another Cpu monitoring tool

## Install
Tested on Ubunutu 14.04LTS and Ubunutu 16.04LTS
### With virtualenv (recommened)
~~~~
virtualenv my_env
source my_env/bin/activate
pip install cpu_monitor
~~~~
### Without virtualenv
~~~~
sudo pip install cpu_monitor
~~~~

## Usage
~~~~
cpu_monitor --help
  -h, --help            show this help message and exit
  --no_display          programm run without displaying and can still log
  --version             show program's version number and exit
  --load LOAD_NB_THREADS
                        Define the number of threads to load during the
                        monitoringIf not used the cpu won't be loaded
  --load_standalone     Does not monitor the CPU usage but only launch load
                        the N threads provided by the --load option, if --load
                        option is not provided only one thread will have
                        workload.
  --display_operations_per_second
                        display number of operation per second if
                        --loadstandalone option is used.
  --cpu_info            Display informations about the CPU used and exit.
  --cpu_info_detailed   Display extended informations about the CPU used and
                        exit.
  --monitoring_freq MONITORING_FREQ
                        Monitoring frequency in Hz
  --log_to_file FILENAME
                        Log gathered results to a file
  --graph_from_log LOGFILE
                        Draw graph for each core and on for the whole cpu from
                        the LOGFILE argument
  --fancy               Display fancy percent color bars during cpu
                        monitoring.
  --log_size LOG_SIZE   Define the maximum number of lines to keep in the log
                        file
~~~~
NB: The following options do not work
~~~~
--load
--load_standalone
~~~~
