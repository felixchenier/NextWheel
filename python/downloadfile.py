# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 15:26:41 2024

@author: MOSA
"""

import nextwheel
from nextwheel import read_dat

dat_filename = "log_2000-12-31_19-00-31.dat"
IP = "192.168.0.130"

if __name__ == "__main__":
    nw = nextwheel.NextWheel(IP)
    nw.file_download(dat_filename)
data = read_dat(dat_filename)
