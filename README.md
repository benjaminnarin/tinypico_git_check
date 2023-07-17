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