#!/bin/bash
disk=$(df -Th)
ram=$(free -h)
echo -e " Total Disk utilisation $disk \n and Total RAM utilization $ram "
