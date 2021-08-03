# Ticketing-System-On-Raspberry-PI
## Table of Contents

* [Introduction](#Introduction)
* [Installation](#Installation)
* [Usage](#Usage)
* [Users hierarchy](#Users-hierarchy)
* 
## Introduction
Ticketing system developed on raspberry pi to provide an embedded solution to track tickets used in different vehicles.
This system support two types of tickets if there is special services provided. I used two types of tickets: civilian and military.
Users hierarchy is provided as many roles, each role contains its own premission to perform predefined tasks.
Any USB devices can be assigned as a key for specific user and role.
This system supports arabic typography using arabic reshaper module and courier font.


## Installation
### Steps :
1. Download Raspbian OS.
2. Update and upgrade OS using
   ` sudo apt-get update 
     sudo apt-get upgrade
   ` commands.
3. Set up hardware ciruit as shown in [link](https://maker.pro/raspberry-pi/tutorial/how-to-add-an-rtc-module-to-raspberry-pi).
4. Install python3 using ` sudo apt-get install python `.
5. Install usb python module ` sudo pip install pyusb `.
6. Install I/O access module in Raspbian ` sudo apt-get install rpi.gpio `.
7. Install arabic-supporting module [Arabic Reshaper](https://pypi.org/project/arabic-reshaper/).
8. Install the proper module for your thermal printer.
9. Install 'wand' module in python to draw our ticket.
10. Download 'courier.ttf' if you want to use arabic language.
11. Specify an image, logo for example, to draw ticket on it.
  
## Users hierarchy
There are four main roles:
### Admin
responsible for updating files and get automatic backup on usb specifice devices.
specified USB device needed to use this role.
### User
responsible for ticketing for passengers.
Default user role, no special key needed.
### Shift
responsible for opening and closing diferent shifts.
specified USB device needed to use this role.
### Supervisor
responsible for checking different shits and tickets for any illegal act.
specified USB device needed to use this role.
