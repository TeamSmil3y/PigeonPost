echo "UNINSTALLING"
python3 -m pip uninstall pigeon -y --break-system-packages
clear
echo "INSTALLING"
python3 -m pip install . --break-system-packages