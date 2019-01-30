# CENTRALIZED LOGGING USING FILEBEAT AND LOGSTASH 

## Introduction 
:::info
Logs are stored for each and every request made by the user. For each request, one server is assigned. To check for any event we need to search the particular server. This is where the Central  Logging System comes to play.
:::

## Using Filebeat and Logstash 
:::info
Filebeat is one of the best log file shippers out there today — it’s lightweight, supports SSL and TLS encryption, supports back pressure with a good built-in recovery mechanism, and is extremely reliable. It cannot, however, in most cases, turn your logs into easy-to-analyze structured log messages using filters for log enhancements. That’s the role played by Logstash.

Logstash acts as an aggregator — pulling data from various sources before pushing it down the pipeline.

The relationship between the two log shippers can be better understood in the following diagram

![](https://i.imgur.com/IVlO2sr.png)

:::

## Installation


### Filebeat
:::warning
To download and install Filebeat, use the commands that work with your system.

deb:
```
curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-6.5.4-amd64.deb
sudo dpkg -i filebeat-6.5.4-amd64.deb
```

mac:
```
curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-6.5.4-darwin-x86_64.tar.gz
tar xzvf filebeat-6.5.4-darwin-x86_64.tar.gz
```
linux
```
curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-6.5.4-linux-x86_64.tar.gz
tar xzvf filebeat-6.5.4-linux-x86_64.tar.gz
```

Windows:

1. Download the Filebeat Windows zip file from the [downloads page](https://www.elastic.co/downloads/beats/filebeat).
1. Extract the contents of the zip file into ***C:\Program Files***.
1. Rename the ***filebeat-<version>-windows*** directory to ***Filebeat***.
1. Open a PowerShell prompt as an Administrator (right-click the PowerShell icon and select ***Run As Administrator***).
1. From the PowerShell prompt, run the following commands to install Filebeat as a Windows service:
```
PS > cd 'C:\Program Files\Filebeat'
PS C:\Program Files\Filebeat> .\install-service-filebeat.ps1
```
Try [official_page](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-installation.html#filebeat-installation) in need for more info.
:::


### Logstash
:::warning

Logstash requires Java 8. Java 9 is not supported. Use the official Oracle distribution or an open-source distribution such as OpenJDK.

To check your Java version, run the following command:
```
java -version
```
On systems with Java installed, this command produces output similar to the following:

```
java version "1.8.0_65"
Java(TM) SE Runtime Environment (build 1.8.0_65-b17)
Java HotSpot(TM) 64-Bit Server VM (build 25.65-b01, mixed mode)
```


Download and install the Public Signing Key:

```
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
```
You may need to install the ***apt-transport-https*** package on Debian before proceeding:
```
sudo apt-get install apt-transport-https
```
Save the repository definition to ***/etc/apt/sources.list.d/elastic-6.x.list***:
```
echo "deb https://artifacts.elastic.co/packages/6.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-6.x.list
```
Run sudo apt-get update and the repository is ready for use. You can install it with:
```
sudo apt-get update && sudo apt-get install logstash
```

Try [official_page](https://www.elastic.co/guide/en/logstash/current/installing-logstash.html#installing-binary) for installation using Yum,Docker,etc.

:::

## Working
 
### Step 1: Configure Filebeat
:::danger
To configure Filebeat, you need to edit the configuration file. The default configuration file is called ***filebeat.yml***. The location of the file varies by platform. To locate the file, see Directory layout.

There’s also a full example configuration file called ***filebeat.reference.yml*** that shows all non-deprecated options.

----
***filebeat.yml***
```
#----------- filebeat prospectors ----------
filebeat.prospectors:
- type: log
  paths:
    - /path/to/log/file
    - /other/path/to/file
  
  fields:
     app_id: xyz_apps
     
# Closes file handler when a file gets rotated
  file_renamed: true 
  close_inactive: 10m
  scan_frequency: 30s

max_procs: 2 #limit CPU usage to 200%

#-------------- Filebeat modules -------------
filebeat.config.modules:
   # Glob pattern for configuration loading
   path: ${path.config}/modules.d/*.yml
   # Set to true to enable config reloading
   reload.enabled: false

 #--------------- Logstash output ------------
output.logstash:
   hosts: ["127.0.0.1:5046"]
   protocol: "http"
```
Try [configure_filebeat](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-configuration.html) for more info
:::

### Step 2: Configure Logstash
:::danger
To configure Logstash, you create a config file that specifies which plugins you want to use and settings for each plugin. You can reference event fields in a configuration and use conditionals to process events when they meet certain criteria. When you run logstash, you use the ***-f*** to specify your config file.
A Logstash config file has a separate section for each type of plugin you want to add to the event processing pipeline.

----
***logstash.conf***
```
# Input Here
input {
    beats {
        port => 5046
          }
      }

# Manipulate Input
filter {
   if "xyz.log" in [source] {
        mutate {
           replace => ["[fields][app_id]", "xyz"]
         }
       }
    }

#Output Here 
output {
   # xyz logs
    if "xyz.log" in [source] {
        file {
            path => "/path/to/central_logs/%{[fields][env]}/%{[beat][name]}/%{[fields][app_id]}/xyz.%{+dd-MM-YYY}.log"
            codec => line{format => "%{message}"}
         }
     }
}
```

Try [configure_logstash](https://www.elastic.co/guide/en/logstash/current/configuration.html) for more info 

:::

### Step 3: Run Commands
:::success
To avoid missing any logs, we start with logstash.

1. Run Logstash
```
/usr/share/logstash/bin/logstash -f /path/to/configation_file.conf
```
2. Check Status
```
sudo service logstash status
```
3.  Running service should look like this![](https://i.imgur.com/bOj4q3k.png)


- There are many other [options](https://www.elastic.co/guide/en/logstash/current/running-logstash-command-line.html) available to run logsatash 
---

We can now run filebeat to send the logs.

1. Start filebeat
```
sudo service filebeat start
```

2. Check  Status
```
sudo service filebeat status
```
3. Running filebeat should look like this
    ![](https://i.imgur.com/V3N6eCZ.png)

- Try [start_filebeat](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-starting.html) for more info on starting filebeat 
:::

## Deployment using Ansible
:::info
We can use 'Ansible' to deploy 'Filebeat' and 'Logstash' to designated servers.

- Deploying filebeat 

```
---
- hosts: servers
  gather_facts: false
  become: yes

  tasks:
    - name: Copying filebeat package
      command: src=config_files/filebeat-6.5.4-amd64.deb dest=/tmp/filebeat-6.5.4-amd64.deb

    - name: Downloading filebeat package
      command: curl -L -o /tmp/filebeat-6.5.4-amd64.deb "https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-6.5.4-amd64.deb"

    - name: Installing filebeat
      command: dpkg -i /tmp/filebeat-6.5.4-amd64.deb

    - name: Copying filebeat config
      template: src=config_files/filebeat.yml dest=/etc/filebeat/filebeat.yml

    - name: Stoping Filebeat
      command: service filebeat stop

    - name: Starting Filebeat
      command: service filebeat start

# vim:ft=ansible:

```
- Deploying logstash
- download the public key using ```wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch```
```
---
- hosts: all 
  gather_facts: false
  become: yes 

  tasks:                                                                                                                                              
    - name: "Copying key"
      copy: src=/path/to/key/GPG-KEY-elasticsearch dest=/path/to/copy/GPG-KEY-elasticsearch owner=root group=root mode=0644
      
    - name: "Adding key"
      command: apt-key add /copied/path/of/GPG-KEY-elasticsearch
      
    - name: "Installing transport package"
      command: apt-get install apt-transport-https
      
    - name: "Saving repository"
      command: echo "deb https://artifacts.elastic.co/packages/6.x/apt stable main" | tee -a /etc/apt/sources.list.d/elastic-6.x.list
      
    - name: "Installing logstash"
      command: apt-get update 
      
    - name: "Installing logstash..."
      command: apt-get install logstash
      
    - name: "Copying configuration files"
      copy: src=/path/to/logstash.conf dest=/etc/logstash/conf.d/logstash.conf owner=root group=root mode=0644
      
    - name: "Starting logstash"
      command: /usr/share/logstash/bin/logstash -f /path/to/configation_file.conf


# vim:ft=ansible:
```
:::
