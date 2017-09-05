#!/bin/sh

echo "Get data before updates:"
curl http://localhost:8000/stats
echo
echo

echo "Update data:"
curl -H "Content-Type: application/json" -d '{"type": "log","payload": "System rebooted for hard disk upgrade"}' http://localhost:9000/log
curl -H "Content-Type: application/json" -d '{"type": "warning","payload": "Unable to open /dev/sr1 read-write"}' http://localhost:9000/log
curl -H "Content-Type: application/json" -d '{"type": "error","payload": "/dev/sr1: unrecognised disk label"}' http://localhost:9000/log
echo
echo

echo "Get data after updates:"
curl http://localhost:8000/stats
echo

