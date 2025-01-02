# create the device
DEVICE_ID=$(mkd -n red-bulb -t brick:Power_Meter -l lab)
add -t brick:Luminaire $DEVICE_ID
add -driver.name kasa $DEVICE_ID
echo "created dev:$DEVICE_ID"

DEVICE_IP="192.168.13.110" # must be provided by user

# add its points 
PT1=$(mkd -p -n status -t brick:On_Off_Status $DEVICE_ID)
PT2=$(mkd -p -n on -t brick:On_Command $DEVICE_ID)
PT3=$(mkd -p -n off -t brick:Off_Command $DEVICE_ID)
PT4=$(mkd -p -n voltage -t brick:Voltage_Sensor $DEVICE_ID)
PT5=$(mkd -p -n current -t brick:Current_Sensor $DEVICE_ID)
PT6=$(mkd -p -n power -t brick:Power_Sensor $DEVICE_ID)

# add xrefs
add -xref kasa://$DEVICE_IP/status $PT1
add -xref kasa://$DEVICE_IP/on $PT2
add -xref kasa://$DEVICE_IP/off $PT3
add -xref kasa://$DEVICE_IP/voltage $PT4
add -xref kasa://$DEVICE_IP/current $PT5
add -xref kasa://$DEVICE_IP/power $PT6

echo "created dev:$DEVICE_ID/pts/$PT1"
echo "created dev:$DEVICE_ID/pts/$PT2"
echo "created dev:$DEVICE_ID/pts/$PT3"
echo "created dev:$DEVICE_ID/pts/$PT4"
echo "created dev:$DEVICE_ID/pts/$PT5"
echo "created dev:$DEVICE_ID/pts/$PT6"