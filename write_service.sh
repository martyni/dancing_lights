DESCRIPTION="Dancing lights hue listener service"
PYTHON=$(which python)
PWD=$(pwd)
EXECUTABLE="/dl.sh"
EXECUTABLE_PATH="${PWD}${EXECUTABLE}"

echo [Unit]
echo Description=Dancing lights service
echo After=network-online.target
echo 
echo [Service]
echo Type=simple
echo ExecStart=$EXECUTABLE_PATH
echo 
echo StandardInput=tty-force
echo 
echo [Install]
echo WantedBy=multi-user.target
