#!/usr/bin/env python

'''
    Copyright (c) 2016-2017 Wind River Systems, Inc.
    
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at:
    http://www.apache.org/licenses/LICENSE-2.0
    
    Unless required by applicable law or agreed to in writing, software  distributed
    under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES
    OR CONDITIONS OF ANY KIND, either express or implied.
'''

"""
Simple app that demonstrates the telemetry APIs in the HDC Python library
"""

import argparse
import errno
import random
import signal
import sys
import os
from time import sleep

head, tail = os.path.split(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, head)

import device_cloud as iot

running = True
sending_telemetry = False

# Second intervals between telemetry
TELEMINTERVAL = 4

def sighandler(signum, frame):
    """
    Signal handler for exiting app
    """
    global running
    if signum == signal.SIGINT:
        print("Received SIGINT, stopping application...")
        running = False

def toggle_telem():
    """
    Turns Telemetry on or off (callback)
    """
    global sending_telemetry
    sending_telemetry = not sending_telemetry
    if sending_telemetry:
        client.alarm_publish("alarm_1", 0)
    else:
        client.alarm_publish("alarm_1", 1)
    msgstr = "{} sending telemetry".format("Now" if sending_telemetry else \
                                           "No longer")
    client.info(msgstr)
    client.event_publish(msgstr)
    return (iot.STATUS_SUCCESS, "Turned On" if sending_telemetry \
            else "Turned Off")

def quit_me():
    """
    Quits application (callback)
    """
    global running
    running = False
    return (iot.STATUS_SUCCESS, "")

if __name__ == "__main__":
    signal.signal(signal.SIGINT, sighandler)

    # Parse command line arguments for easy customization
    parser = argparse.ArgumentParser(description="Demo app for Python HDC "
                                     "telemetry APIs")
    parser.add_argument("-i", "--app_id", help="Custom app id")
    parser.add_argument("-c", "--config_dir", help="Custom config directory")
    parser.add_argument("-f", "--config_file", help="Custom config file name "
                        "(in config directory)")
    args = parser.parse_args(sys.argv[1:])

    # Initialize client default called 'python-demo-app'
    app_id = "iot-simple-telemetry-py"
    if args.app_id:
        app_id = args.app_id
    client = iot.Client(app_id)

    # Use the demo-connect.cfg file inside the config directory
    # (Default would be python-demo-app-connect.cfg)
    config_file = "demo-iot-simple-telemetry.cfg"
    if args.config_file:
        config_file = args.config_file
    client.config.config_file = config_file

    # Look for device_id and demo-connect.cfg in this directory
    # (This is already default behaviour)
    config_dir = "."
    if args.config_dir:
        config_dir = args.config_dir
    client.config.config_dir = config_dir

    # Finish configuration and initialize client
    client.initialize()

    # Set action callbacks
    client.action_register_callback("toggle_telemetry", toggle_telem)
    client.action_register_callback("quit", quit_me)

    # Telemetry names (properties for numbers, attributes for strings)
    properties = ["property-1", "property-2"]
    attributes = ["attribute-1", "attribute-2"]

    # Connect to Cloud
    if client.connect(timeout=10) != iot.STATUS_SUCCESS:
        client.error("Failed")
        sys.exit(1)

    counter = 0
    while running and client.is_alive():
        # Wrap sleep with an exception handler to fix SIGINT handling on Windows
        try:
            sleep(1)
        except IOError as err:
            if err.errno != errno.EINTR:
                raise
        counter += 1
        if counter >= TELEMINTERVAL:
            if sending_telemetry:
                # Randomly generate telemetry and attributes to send
                for p in properties:
                    value = round(random.random()*1000, 2)
                    client.info("Publishing %s to %s", value, p)
                    client.telemetry_publish(p, value)
                for a in attributes:
                    value = "".join(random.choice("abcdefghijklmnopqrstuvwxyz")
                                    for x in range(20))
                    client.log(iot.LOGINFO, "Publishing %s to %s", value, a)
                    client.attribute_publish(a, value)

            # Reset counter after sending telemetry
            counter = 0

    client.disconnect(wait_for_replies=True)

