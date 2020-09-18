#!/bin/bash
#--dest-dir is a must, else it will print it to screen
taxii-poll --path https://otx.alienvault.com/taxii/poll --collection user_AlienVault --username 'username' --password foo --begin 2020-09-01 --dest-dir /path/to/somewehere/
