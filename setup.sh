
set -e

pip3 install pyinotify --user

# create symbolic link to the controller, that is to be set up as a service 
#echo "Removing old link to i3 grid controller (if it exists)"
#rm /usr/local/bin/i3GridController
echo "Link controller"
ln -sf $(pwd)/src/controller.py /usr/local/bin/i3GridController
ln -sf $(pwd)/bash/i3Grid /usr/local/bin/i3Grid
ln -sf $(pwd)/bash/starti3Grid.sh /usr/local/bin/starti3Grid.sh



