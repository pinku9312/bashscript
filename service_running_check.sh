#!/bin/bash
systemctl is-active --quiet httpd

if [ $? -eq 0 ]
then 
	printf " httpd service chal rahi hai \n"
else
	printf "httpd service band hai , restart karrahe hai....\n"
	systemctl restart httpd	
fi
