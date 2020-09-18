############################################################################
# Copyright (c) Rapid7, LLC 2019  https://www.rapid7.com/
# All rights reserved. This material contains unpublished, copyrighted
# work including confidential and proprietary information of Rapid7.
############################################################################
#
# abusech_feodo_indicators.ps1
#
# Script version: 2.1.1
# PowerShell Version: 4.0.1.1
# Source: consultant-public
#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY 
# KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS FOR A
# PARTICULAR PURPOSE.
#
# Tags: INSIGHTIDR
# 
# Description:
# This script will download indicators from the location specified, place
# them into a CSV file, and then upload them to the private threat feed
# specified.  This script is intended to be used with the InsightIDR 
# Threat Community threats and uses the InsightiDR REST API v1.
#

#***** VARIABLES TO BE UPDATED *****
$StartMs = (Get-Date).Millisecond
#Change the value below to the threat list that you wish to import.
#$IOCURL = " [ paste in the Target Threat List to import ] "
$IOCURL = "https://feodotracker.abuse.ch/downloads/ipblocklist.txt"

#Enter the Threat Key for the threat that is being modified.  
#Get the threat key by opening your community threat and selecting Threat Key.
#$ThreatKey = " [ paste in your Threat Key from IDR Threats ] "

#$headers = @{}
#Enter in your platform API key.  This can be generated from the Rapid7 Platform home.
#Log into https://insight.rapid7.com and use the API Management section to generate a key.
#$headers["X-Api-Key"] = " [ paste in your Platform API Key ]  "

#***** END OF VARIABLES TO BE UPDATED *****

#These files are used when downloading the indicators and converting them to CSV format.
#They are left in situ on purpose so that you can verify that the script works.  If this bothers you,
#use the sections below to delete these temp files after the indicators are uploaded.
#The first file contains a list of indicators scraped from the $IOCURL website.  It is not cleaned up.
$IOCOutputFileName = "indicators.txt"
#The CSV file is clean and ready to be uploaded.
$CSVOutputFileName = "indicators.csv"
#The JSON file
$JSONOutputFileName = "indicators.json"
# Get the location of the script for the output files.  Output files 
# will be located where script is being run.
$path = Get-Location
$IOCFilePath = "$path\" + "$IOCOutputFileName"
$CSVFilePath = "$path\" + "$CSVOutputFileName"

#This location is where the threats will be uploaded.
#$Url = "https://us.api.insight.rapid7.com/idr/v1/customthreats/key/" + $ThreatKey + "/indicators/replace?format=csv"

#Configure the download to use TLS 1.2
[System.Net.ServicePointManager]::ServerCertificateValidationCallback = {$true}
[Net.ServicePointManager]::SecurityProtocol = 'Tls12'

#delete text download file if it exists already
if (Test-Path $IOCFilePath) {
    Write-Host "Deleting existing indicator file: $IOCFilePath"
    Remove-Item $IOCFilePath
    }

#delete csv file of downloaded indicators if it exists already
if (Test-Path $CSVFilePath) {
    Write-Host "Deleting existing CSV file: $CSVFilePath"
    Remove-Item $CSVFilePath
    }
#Download the indicators from the specified URL.
Write-Host "Downloading indicators from website"
$IOCblocklist = New-Object Net.WebClient
$IOCblocklist.DownloadString($IOCURL) > tempindicators.txt

#checks for blank text file and exits the program if the file is blank
Get-Content tempindicators.txt | Measure-Object -word
if ($word -eq 0){
    Write-Host "Empty Indicators List, Ending Script"
    Break
    }

#Clean up the temp file of downloaded indicators.
#This script pulls out an indicator from the first field in the list of output.  You may need to select a different field.
#Change the Select Field1 line to match whatever field has the indicators in it.
#The rest of this block cleans up the download and adds commas to end of each line (so it will be a CSV file).
	
$IOCblocklist = Import-CSV tempindicators.txt -Header "Field1", "Field2", "Field3", "Field4", "Field5", "Field6" `
	| Select Field1 `
	| ConvertTo-Csv -NoTypeInformation `
	| % {$_ -replace  ` '\G(?<start>^|,)(("(?<output>[^,"]*?)"(?=,|$))|(?<output>".*?(?<!")("")*?"(?=,|$)))' ` ,'${start}${output}'} `
	| %{$_ -replace '$',','}`
	| Out-File $IOCFilePath -fo -en ascii ; 


#You can uncomment the following line to delete blank lines from the output, if there are any.
#(Get-Content $IOCFilePath) | ? {$_.trim() -ne "" } | set-content $CSVFilePath
Write-Host "Clean up the file by removing the header"
#Skip reading the first line of the file, which is a header.
#Delete all of the lines that start with a #, which are also part of the header.
Get-Content $IOCFilePath | Select-Object -Skip 1 | Where { $_ -notmatch '^\#' } | Set-Content $CSVOutputFileName
$Testi = Get-Content $CSVOutputFileName
#Remove duplicating strings from the output and convert to JSON
$Testi -replace "^*?:" -replace ",", "" | ConvertTo-Json | Set-Content $JSONOutputFileName

#Command to emulate curl with PowerShell.
#Write-Host "Starting command to connect to API"
#$ContentType = 'text/csv'
#$Response = Invoke-WebRequest -Uri $url -Headers $headers -InFile $CSVFilePath -Method Post -ContentType $ContentType -UseBasicParsing
$EndMs = (Get-Date).Millisecond
Write-Host "Script has finished running. Check your results. The script took $($EndMs - $StartMs)ms to run, yay"
