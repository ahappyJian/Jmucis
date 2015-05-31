#!/bin/bash

mailaddr='jzhu.k.r@qq.com'
proc="./bin/jmusic_main.py"
mlog_prefix="monitor.log"
log_prefix="jmusic.log"


Checking ()
{
	local cnt=`ps aux | grep "$1" | grep -v grep | wc -l` 
	return $cnt;
}
LOG()
{
	if [ $debug -eq 1 ]; then
		echo $1
	else
		local cur_ymd=`date -u '+%Y-%m-%d'`
		local mlog="$mlog_prefix.$cur_ymd"
		echo "$1" >> $mlog
	fi
}
debug=0
if [ "$1" = '-d' ]; then
	debug=1
	echo "DEBUG Mode"
fi

web_max=6
web_cnt=6
while true; do
	if [ $web_cnt -eq $web_max ]; then
		web_cnt=0
		# checking 
		LOG "checking $proc"
		Checking $proc
		ret=$?
		if [ $ret -eq 0 ]; then
			LOG "Service is down. Restart now:$proc" 
			cur_t=`date -u '+%Y%m%d%H%M%S'`
			log="$log_prefix.$cur_t"
			nohup $proc > $log 2>&1 &
			cur_t=`date -u '+%Y-%m-%d %H:%M:%S'`
			LOG "Restart $proc at UTC time:$cur_t" 
			#echo "Restart $proc at UTC time:$cur_t" | mail -s "J Alert" $mailaddr
		fi
	fi

	# count one 
	web_cnt=$(($web_cnt+1));
	sleep 1
done
