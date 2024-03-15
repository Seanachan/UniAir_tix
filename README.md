# 立榮航空搶票機器人

2024/03/13

For the purpose of getting tickets during busy season.

**This bot has been only been tested on Mac M1 Pro**

# How to set up

Step 1 : run this

`python3 settings.py`

Step 2 : Just follow the instructions in command line

Step 3: The desired settings will be stored in settings.json file


**Keep the .json file to be stored under the same category**

> You can check where category it is located at by running `pwd`

# How to Execute Source Code

Step 1 : get the source code

`git clone https://github.com/Seanachan/UniAir_tix.git`

Step 2 : Go to this file

`cd UniAir_tix`

Step 3 : Download required packages

`python3 pip install -r pip-req.txt`

Step 4 : Run the code

`python3 main.py <date to book> <total number of passengers> <number of adults(non residents)> <number of adult residents>`

> Example:
>
> python3 main.py 2024/03/14 3 2 1

# Problems

### What to do when encouter Package Not Found

Try this:

`echo "export PATH=/opt/[Name Of Package]/bin:$PATH" >> ~/.zshrc`
