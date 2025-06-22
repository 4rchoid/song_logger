import signal
import sys
import logging
import time
from django.db import connections
from django.db.utils import OperationalError

def graceful_shutdown_handler(signal_num, frame):
    print(f"Received shutdown signal: {signal_num}")
    
    # Close all open DB connections
    try:
        for conn in connections.all():
            if conn and not conn.closed_in_transaction:
                conn.close()
                (f"Closed DB connection: {conn.alias}")
    except OperationalError as e:
        print(f"DB connection close failed: {e}")

    print("Graceful shutdown complete.")
    sys.exit(0)

def setup_graceful_shutdown():
    signal.signal(signal.SIGINT, graceful_shutdown_handler) 
    signal.signal(signal.SIGTERM, graceful_shutdown_handler)