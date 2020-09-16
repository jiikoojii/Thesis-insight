#!/bin/bash

#date1=$(date -Iseconds)
#echo $date1

taxii-poll --path https://otx.alienvault.com/taxii/poll --collection user_AlienVault --username 0f9645cdc183e55ab622272962ff596f9663c0815bc92eb2807d7ba565967e43 --password foo --begin 2020-09-01 --dest-dir /home/janij/testi/
