from datadog import initialize, statsd
import time
import logging

def init_logger():
    logging.basicConfig()

def init_dstatsd():
    options = {
        "api_key":  "someapikey",
        "app_key": "someappkey",
        "statsd_host": "localhost",
        "statsd_port": 8125
    }
    initialize(**options)

def emit_metrics():
    while(1):
        print(f"increment py.local.example.increment")
        statsd.increment('py.local.example.increment', tags=["environment:kc-dev"])
        time.sleep(5)

def run():
    init_logger()
    init_dstatsd()
    emit_metrics()
    print('Hello, world!')

if __name__ == '__main__':
    run()
