#!/bin/bash
HOME=/root
sudo netstat -ntlp |awk /5000/'{print $7}'| tr -d '/python'| xargs kill -9

ping -c 3 192.168.1.1
if [ $? == 0 ] 
   then
	   echo lol
   /home/martyni/Envs/dancing_lights/bin/python	/home/martyni/Envs/dancing_lights/dancing_lights/app.py &
   /home/martyni/Envs/dancing_lights/bin/python /home/martyni/Envs/dancing_lights/dancing_lights/ser_lib.py
else
  echo sleeping
  sleep 10
  bash /home/martyni/Envs/dancing_lights/dancing_lights/dl.sh	
fi
#sleep 200
