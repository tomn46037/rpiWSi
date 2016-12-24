#!/bin/sh

echo "Starting loop"

while [ true ]
do

echo "Starting"
/usr/bin/python ./rpiWSi.py
echo "sleeping"
sleep 2

done

