#!/bin/bash
printf "Apni umar batao: "
read age

if [ $age -ge 18 ]
then 
	printf " Tum vote de sakte ho \n"
else
	printf " Tum abhi vote nahi de sakte \n"
fi
