#!/bin/bash
# Bash script that invokes the backup service
# every 16 minutes (16 to avoid potential db write conflicts)

while true
do
    go run backupService.go
    sleep 6m
done