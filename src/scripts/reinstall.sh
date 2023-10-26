echo "UNINSTALLING"
python3 -m pip uninstall protofire -y --break-system-packages
clear
echo "INSTALLING"
python3 -m pip install . --break-system-packages