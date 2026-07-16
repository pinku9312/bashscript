#!/bin/bash
usage=$(df / | tail -1 | awk '{print $5}' | tr -d '%')

if [ $usage -ge 80 ]
then
	printf "Warning: Root partition %d%% fullhai \n" "$usage"
else
	printf "Root partition sahi hai: %d%%\n" "$usage"
fi
