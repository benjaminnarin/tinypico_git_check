# tinypico_git_check
TinyPICO micropython code that changes LED color if code has been checked in that day

## Hardware
 * TinyPico

## Software
 * micropython
 * micropy-cli - used to init workspace
 * micropython-esp32-um-tinypico-stubs 1.19.1.post7 - stub for tinypico board
 * mpremote - load and running code on tinypico

 # Config
 Copy config on to device before running running code locally with mpremote

 # urequests install
 In micropython terminal run:

    1. import upip
   
    2. upip.install('micropython-urequests')
    
    3. copy urequests.py over to tinypico

# Current Time
   Micropython time api does not implement timezones, instead of dealing with timezones and day light savings I am using a web api (https://timeapi.io/) that returns the current time for a given timezone. Although not on device it cleanly handles all the logic around timezones and can be used to sync to occasionally to counteract time drift.