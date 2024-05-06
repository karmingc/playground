from ddtrace import patch_all, tracer
import time
import logging

patch_all()

def init_logger():
    logging.basicConfig()

@tracer.wrap()
def print_msg():
    print(f"tracing hi")

def emit_traces():
    while(1):
        print_msg()
        time.sleep(5)

def run():
    init_logger()
    emit_traces()

if __name__ == '__main__':
    run()
