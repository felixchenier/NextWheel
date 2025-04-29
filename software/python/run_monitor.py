#!/usr/bin/env python3

import nextwheel
import sys
import time

if __name__ == "__main__":
    ip = sys.argv[-1]
    nw = nextwheel.NextWheel(ip)
    nw.start_streaming()
    nw.monitor()
    nw.stop_streaming()
