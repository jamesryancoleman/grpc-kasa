# create create a driver, if needed
# if not needed, comment out.
# DRIVER_ID=$(add -driver.name kasa)
# echo "created driver:$DRIVER_ID"

# create the device
DEVICE_ID=$(mkd -n green-bulb -t brick:Power_Meter -l home)
add -t brick:Luminaire $DEVICE_ID # add second type
# add -driver $DRIVER_ID $DEVICE_ID
add -driver.name kasa $DEVICE_ID # use if kasa already exists
echo "created dev:$DEVICE_ID"

DEVICE_IP="192.168.1.186" # must be provided by user

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