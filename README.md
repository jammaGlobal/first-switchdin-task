##Random Number Stats
Here is the repo for the Python Software Engineer (Embedded, Data Science) skills test. I believe my solution is correct although there are improvements that could be made. 

The schedule python library doesn't feature any way to set priority on jobs and so initially I had a call to calcAndSendAverage every 1 min, every 5 mins, and every 30 mins however the 5min and 30min jobs when run needed to be run in sequence after the 1min job which wasn't guaranteed which the scheduler. If I had more time I would have investigated more into threading or asyncio. 

At one point of the implementation I started to interpret the specs as asking to create stats like a moving time window, analogous to the msg rate stats in the RabbitMQ UI, so the most recent minute, most recent 5 minutes, and most recent 30 minutes were getting averages calculated for both random number values per minute and messages per minute. Some of the variable naming and code bloat is remnants of this interpretation and I would refactor if I had more time. I would also have liked to give the project more structure, like putting the mqtt client, its config and functions to call publish/subscribe in a client class. 

I would say I spent around 15 hours on this and this length was partly due to me not clarifying the spec earlier by email, the level of familiarity I have with python and rusty knowledge of os concepts. I also did not use Ansible. These things I am eager to improve on.
### For EC2 Instance:
In Powershell, login via ssh, replace "jameyb-access.pem" with the name of your private key file. You can use Putty if you want.
```
ssh -i "jameyb-access.pem" ec2-user@ec2-3-25-75-240.ap-southeast-2.compute.amazonaws.com
```

Docker container for rabbitmq instance should be running already, if not use same docker commands that are for local use

Navigate to project folder, "git fetch" and "git pull" to confirm it is up to date.

Activate the existing python virtual env (random-numbers) which has packages already installed
```
cd skills-tests/first-switchdin-task
source random-numbers/bin/activate
```
Set permissions on run script on first time use
```
chmod u+x runapps.sh
./runapps.sh
```
To exit out of the python scripts, run this command
```
ps ax | grep python3 | cut -c1-5 | xargs kill -9
```
### For Local use:
Pre-conditions: Python3 should be installed, Docker should be installed, bash shell should be installed

Clone repo and navigate into the folder

Use the Dockerfile to build and run a rabbitmq instance that has mqtt plugins
```
docker build -t myrabbitmq .
docker run -d -p 1883:1883 -p 15675:15675 -p 15672:15672 --hostname my-rabbit --name some-rabbit myrabbitmq
```
Create python virtual env, activate, and install packages
```
python3 -m venv random-numbers
source random-numbers/bin/activate
pip install paho-mqtt
pip install schedule
pip install prettytable
```
Use the same commands as above to run and exit
```
./runapps.sh
ps ax | grep python3 | cut -c1-5 | xargs kill -9
```
