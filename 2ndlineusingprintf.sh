#!/bin/bash
date=$(date)
disk=$(df -Th)
ram=$(free -h)
list=$(nmcli con show)
printf "Today date is : %s\n\n Total disk utilization:\n%s\n\n\n Total ram utilization is :\n%s\n\n\n List of Network Adopter :\n%s\n\n\n" "$date" "$disk" "$ram" "$list"
