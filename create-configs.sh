#!/bin/sh

cd user
for F in *.conf.example; do 
	cp "$F" "`basename $F .example`"; 
done
	
	
cd ../system
for F in *.conf.example; do
	cp "$F" "`basename $F .example`"; 
done