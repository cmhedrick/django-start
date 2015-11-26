# Django Start

An open source automation tool to help build the perfect enviroment for a Django Project. By using a series of prompts it accomplishes this by:

+ Creating a Virtual enviroment using `virtualenv` (conventionally named 'env')
+ Installing the latest version of `django` into 'env'
+ Creating both the Site Directory & App Directory
+ Has a flag to switch between Production and Development settings
+ Creates a **production ready** settings file (settings_pro.py)
+ Creates a requirements.txt for development and requirements_pro.txt for production requirements. *(Conventionally django is used with postgresql so the plugin for it is already in the requirements_pro.txt)*

### Requirements Before Use:
1. `python3` (or `python2`)
2. `virtualenv`

### Work Flow

Ideally in the manor of steps:
1. You have cloned this repo or downloaded the script.
2. Create your project directory 
 ```sh 
$ mkdir yourproject 
```
3. change into that directory
```sh 
$ cd yourproject 
```
4. copy the `django-start.py` file into your project directory
```sh 
$ cp [path to]/django-start.py .
```
5. Run the script

### Running The Script:

Running the script is really easy and can be done one of two ways.

Method 1:
```sh
$ python django-start.py
```

Method 2:
```sh
$ ./django-start.py
```

### Maintenance/Bug Tracking/Enhancements

Please fill free to submit bugs or enhancements through the issue tracker!
I will be maintaining this project for some time as I'm a big fan and developer using django. Feel free to make contributions by submitting Pull Requests as well!
Thanks!
