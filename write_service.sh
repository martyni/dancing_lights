DESCRIPTION="Dancing lights hue listener service"
DESCRIPTION="Dancing lights hue listener service"
PYTHON=$(which python)
PWD=$(pwd)
EXECUTABLE="/ser_lib.py"
EXECUTABLE_PATH="${PWD}${EXECUTABLE}"

echo [Unit]
echo Description=Dancing lights service
echo After=multi-user.target
echo 
echo [Service]
echo Type=simple
echo ExecStart=$PYTHON $EXECUTABLE_PATH
echo 
echo StandardInput=tty-force
echo 
echo [Install]
echo WantedBy=multi-user.target
