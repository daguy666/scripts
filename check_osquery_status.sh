#!/bin/sh

# This needs to be ran with sudo, so that it can log
# properly and scan the paths.
 
if [ "$EUID" -ne 0 ]
    then echo "[?] Please run as root."
    exit
fi

# Setup some vars. 
OSQi='/usr/local/bin/osqueryi'
OSQd='/usr/local/bin/osqueryd'
OSQ_LOGPATH='/var/log/osquery'
OSQ_STATUS_PATH='/var/log/osquery_status.log'
OWNED_BY=$(stat -f '%Su' "$OSQd")

# This block will check that the osquery default log path exists. 
# If it does not, it will create it. After it creates the directory,
# osquery should auto start. 

if [ ! -d "$OSQ_LOGPATH" ]
    then
        # create it
        /bin/mkdir -p "$OSQ_LOGPATH"
        echo "$(date +"%Y-%m-%d_%H-%M-%S")"  Created "$OSQ_LOGPATH" directory.  >> "$OSQ_STATUS_PATH"
else
    echo "$(date +"%Y-%m-%d_%H-%M-%S")" "$OSQ_LOGPATH" already exists. >> "$OSQ_STATUS_PATH"
fi


# If block for binary ownership

if [ "$OWNED_BY" == 'root' ]
    then
        echo "$(date +"%Y-%m-%d_%H-%M-%S")" Binary is owned by root. >> "$OSQ_STATUS_PATH"
else
    /usr/sbin/chown root /usr/local/sbin/osqueryd
    echo "$(date +"%Y-%m-%d_%H-%M-%S")" Changing owner of "$OSQd" to root. >> "$OSQ_STATUS_PATH"
fi

# Check the version of osqueryi and osqueryd. 
echo "$(date +"%Y-%m-%d_%H-%M-%S")" "$("$OSQi" --version)" >> "$OSQ_STATUS_PATH" "$("$OSQi" --version)"
echo "$(date +"%Y-%m-%d_%H-%M-%S")" "$("$OSQd" --version)" >> "$OSQ_STATUS_PATH" "$("$OSQi" --version)"

