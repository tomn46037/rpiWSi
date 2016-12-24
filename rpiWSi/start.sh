#!/bin/sh

echo "Starting loop"

while [ true ]
do

echo 
ip addr | grep "inet "
echo

echo "Starting"
/usr/bin/python ./rpiWSi.py

echo "sleeping"
sleep 2

done

