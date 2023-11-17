import os
import json
import re
import time
import signal

# Flag to control the main loop
running = True

def parse_filename(filename):
    # Use regular expression to extract isd, base, and serial
    match = re.match(r'ISD(\d+)-B(\d+)-S(\d+)\.trc', filename)
    if match:
        return {
            'id': {
                'isd': int(match.group(1)),
                'base_number': int(match.group(2)),
                'serial_number': int(match.group(3))
            }
        }
    return None

def create_trcs_json(directory):
    trcs = []
    # List all files in the directory
    for filename in os.listdir(directory):
        # Parse each filename
        trc_info = parse_filename(filename)
        if trc_info:
            trcs.append(trc_info)

    # Write the JSON array to a file
    with open('/etc/scion/bootstrap-server/trcs.json', 'w') as json_file:
        json.dump(trcs, json_file, indent=4)

def signal_handler(signum, frame):
    global running
    print("Shutdown signal received. Exiting...")
    running = False

# Directory containing the TRC files
directory_path = '/etc/scion/certs'

# Time interval (in seconds)
interval = 5 * 60  # 5 minutes

# Register the signal handlers
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

while running:
    print("Updating trcs.json...")
    create_trcs_json(directory_path)
    print("Update complete. Waiting for next interval...")
    time.sleep(interval)

print("Script terminated.")