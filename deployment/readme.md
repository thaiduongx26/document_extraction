# Deployment guidelines
## Prerequisite
  * docker  
 
## Operations
#### Start aurora for the first time
```shell script
sudo ./aurora init
```

#### Start aurora
    
```shell script
./aurora start
```

#### Stop aurora

```shell script
./aurora stop
```

#### Monitoring
```shell script
./aurora logs
```

## Configuration
To let new settings take effect, aurora must be restarted with:

```shell script
./aurora restart
```

### Config folder mapping
In `env` file, you will find the below default settings:
```shell script
CONFIG_FOLDER="${PWD}/data/config"
LOG_FOLDER="${PWD}/data/log"
INPUT_FOLDER="${PWD}/data/input"
WORKING_FOLDER="${PWD}/data/working"
OUTPUT_FOLDER="${PWD}/data/output"
```

  * `CONFIG_FOLDER` - store configuration file config.yaml
  * `LOG_FOLDER` - store log files: process.log and charge.log
  * `INPUT_FOLDER` - input folder is where the user places the document to be processed.
  * `WORKING_FOLDER` - working folder is where to store intermediate file.
  * `OUTPUT_FOLDER` - output folder is where to output the files.

For example, you want to place the log under `/var/log/cinnamon/aurora`, then update `LOG_FOLDER` value:
```shell script
LOG_FOLDER=/var/log/cinnamon/aurora
```

### Config timezone
Config timezone will affect the time on log entries.
In `env` file, you will find the below default value:
```shell script
TZ=UTC
```

You can change it to `TZ=Asia/Tokyo`, for example.


### Config sensor scan rate
Under `config.yaml` file, `sensor` section, you will find the below default value:
```yaml
sensor:
  schedule: 10 # seconds
```

Change it to 20 minutes with, `schedule: 1200`.

### Config log rotation
There are 2 places corresponding with process log and master log. The same mechanism is applied.

Under `config.yaml` file, `file_handler` and `master_file_handler` sections, you will find the below default value:
```yaml
    file_handler:
      class: logging.handlers.TimedRotatingFileHandler
      formatter: standard
      level: DEBUG
      filename: data/log/process.log
      encoding: utf8
      when: 'midnight'
      backupCount: 60
```

  * `when` - specify when to back up the current log and create new one, default: `midnight`
  * `backupCount` - specify how many backup files to keep, default: 60 So, by default, the log will rotate every 2 months(60 days).


### Config log level
This will adjust the amount of log produced.
In `config.yaml`, you will find the below default value:
```yaml
  loggers:
    ai:
      level: DEBUG
      handlers: [console, file_handler]
      propagate: no

    preprocess:
      level: DEBUG
      handlers: [console, file_handler]
      propagate: no

    master_log:
      level: INFO
      handlers: [master_file_handler]
```

For example, you want to see the warning and error log only, then, set
 ```yaml
      level: WARNING
```
