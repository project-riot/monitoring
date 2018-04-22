#!/bin/sh
set -e

### Configuration
#
# List of IPs to account
IPS="192.168.1.223 192.168.1.19"
# Directory where to store statistics
DIR=/mnt/sda1

start() {	
	iptables -N BANDWIDTH-ACCT
	iptables -I FORWARD -j BANDWIDTH-ACCT
        for IP in $IPS
        do
		iptables -A BANDWIDTH-ACCT -d $IP
		iptables -A BANDWIDTH-ACCT -s $IP
        done
	logger Started bandwidth-accounting log
}

stop() {
	RULE_NUM=$(iptables -L FORWARD -n --line-numbers | grep BANDWIDTH-ACCT | awk '{print $1}')
	iptables -D FORWARD $RULE_NUM

	iptables -F BANDWIDTH-ACCT

	iptables -X BANDWIDTH-ACCT
}

account_ip() {
        IP=$1

	TOTAL_BW=`iptables -L BANDWIDTH-ACCT -n -v -x | grep $IP | awk '{print $2}' | awk 'BEGIN { sum=0 } { sum+= $1 } END { print sum }'`
	TOTAL_PKTS=`iptables -L BANDWIDTH-ACCT -n -v -x | grep $IP | awk '{print $1}' | awk 'BEGIN { sum=0 } { sum+= $1 } END { print sum }'`
}

reset_counter() {
	iptables -Z BANDWIDTH-ACCT
}

write_out() {
        test -d $DIR || mkdir -p $DIR
        for IP in $IPS
        do
                FILE=$DIR/BW$(date +%Y-%m-%d)_$IP.csv
                account_ip $IP
                echo "$(date "+%Y-%m-%d %H:%M:%S"),$TOTAL_BW,$TOTAL_PKTS" >> $FILE
        done
	logger Updated bandwidth-accounting log
}

ACTION=$1
case $ACTION in
        start)
                start
        ;;
        stop)
                write_out
                stop
        ;;
        write)
                write_out
                reset_counter
esac

