# Item Catalog Application

## Overview
This is a web application written in Python for Listing Modern Architecture in World Cities.

## Features
It shows and stores data of cities and architectures.  
You can do below in this appliction.
* See Cities and Architectures in each cities.
* Register new city and architecture.

![Sample Screen1](https://user-images.githubusercontent.com/24450194/44352992-b7517a80-a4e0-11e8-85c2-03380aeb77dd.png)
![Sample Screen2](https://user-images.githubusercontent.com/24450194/44353014-c801f080-a4e0-11e8-83e8-565e04a726ba.png)


## Requirement
* Python
* [Vagrant](https://www.vagrantup.com/downloads.html)
* [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)  
(Recommended to install 5.1, Newer versions are not yet compatible with Vagrant.)

## How to Use
1. Start up Vagrant.
1. In the command line, switch to `item_catalog_application/` directory.
1. To setup (or recreate) database, Run: `python database_setup.py`
1. (optional) To populate database by dummy data, Run: `python lotsofcities.py`
1. Run: `python project.py`, then it starts up.
1. Access `http://localhost:8000/`.

## License
This project is licensed under the MIT License.
