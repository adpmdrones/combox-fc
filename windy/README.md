# combox-fc
COMBOX with Flight Control Hardware

```bash
https://api.windy.com/point-forecast/docs
```

This Python code is  a script for collecting telemetry data from a drone using the MAVLink protocol and sending it to a remote ThingsBoard dashboard. It uses the "requests" library to make HTTP requests to the drone and send telemetry data to the dashboard.

The script defines several functions for reading MAVLink data from the drone, sending it to the dashboard, and handling errors during execution. It also includes a "telemetry" class representing the drone's telemetry data and a logger to log events and errors during script execution.

To run the script, the ThingsBoard device token and the drone ID must be specified, as well as endpoint variables for the drone and dashboard. The script then makes periodic requests to the drone for MAVLink data and sends telemetry data to the dashboard via HTTP POST requests.

