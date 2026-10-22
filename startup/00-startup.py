import time as ttime

from databroker.v0 import Broker

import bluesky
from packaging.version import Version
from datetime import datetime

import sys
import os
import signal
from pathlib import Path
from timeit import default_timer as timer
import shlex, subprocess

import bluesky.plan_stubs as bps
import numpy as np
import pandas as pd
import time as ttime
import matplotlib.pyplot as plt
plt.ion()

from ophyd import (ProsilicaDetector, SingleTrigger, Component as Cpt, Device,
                   EpicsSignal, EpicsSignalRO, ImagePlugin, StatsPlugin, ROIPlugin,
                   DeviceStatus)

def time_now_str():
    return datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S.%f')

# def print_to_gui(msg, tag='', add_timestamp=False, ntabs=0, stdout=sys.stdout):
def print_to_gui(msg, tag='', add_timestamp=False, ntabs=0, stdout_alt=sys.stdout):
    # print('THIS IS STDOUT', stdout, stdout is xlive_gui.emitstream_out)
    try:
        stdout = xlive_gui.emitstream_out
    except NameError:
        stdout = stdout_alt

    msg = '\t'*ntabs + msg
    if add_timestamp:
        msg = f'({time_now_str()}) {msg}'
    if tag:
        msg = f'[{tag}] {msg}'

    print(msg, file=stdout, flush=True)


db_archiver = Broker.named('iss-archiver')
arch_iss  = db_archiver.event_sources_by_name['arch_iss']

# args = shlex.split('python /home/xf08id/.ipython/profile_sample-environment/iocs/ioc_ramping.py')
# args = shlex.split('conda activate collection-2021-1.2; gnome-terminal -e "python /home/xf08id/.ipython/profile_sample-environment/iocs/ioc_ramping.py"')
# args = shlex.split('"python /home/xf08id/.ipython/profile_sample-environment/iocs/ioc_ramping.py"')
# ioc_args = shlex.split('gnome-terminal -- python /home/xf08id/.ipython/profile_sample-environment/iocs/ioc_ramping.py')
ioc_args = shlex.split('gnome-terminal -- python /nsls2/data/iss/shared/config/bluesky/profile_sample-environment/iocs/ioc_ramping.py')

ioc_process = subprocess.Popen(ioc_args)


def get_pid(input_args):
    input = ['pidof'] + input_args
    return list(map(int, subprocess.check_output(input).split()))[0]

def kill_pid_ioc():
    pid_ioc = get_pid(ioc_args)
    os.kill(pid_ioc, 9)


if Version(bluesky.__version__) < Version('1.6'):
    OLD_BLUESKY = True
else:
    OLD_BLUESKY = False


###############################################################################
# TODO: remove this block once https://github.com/bluesky/ophyd/pull/959 is
# merged/released.
from ophyd.signal import EpicsSignalBase, EpicsSignal#, DEFAULT_CONNECTION_TIMEOUT
DEFAULT_CONNECTION_TIMEOUT = 10
def wait_for_connection_base(self, timeout=DEFAULT_CONNECTION_TIMEOUT):
    '''Wait for the underlying signals to initialize or connect'''
    if timeout is DEFAULT_CONNECTION_TIMEOUT:
        timeout = self.connection_timeout
    # print(f'{print_now()}: waiting for {self.name} to connect within {timeout:.4f} s...')
    start = ttime.time()
    try:
        self._ensure_connected(self._read_pv, timeout=timeout)
        # print(f'{print_now()}: waited for {self.name} to connect for {time.time() - start:.4f} s.')
    except TimeoutError:
        if self._destroyed:
            raise DestroyedError('Signal has been destroyed')
        raise

def wait_for_connection(self, timeout=DEFAULT_CONNECTION_TIMEOUT):
    '''Wait for the underlying signals to initialize or connect'''
    if timeout is DEFAULT_CONNECTION_TIMEOUT:
        timeout = self.connection_timeout
    # print(f'{print_now()}: waiting for {self.name} to connect within {timeout:.4f} s...')
    start = ttime.time()
    self._ensure_connected(self._read_pv, self._write_pv, timeout=timeout)
    # print(f'{print_now()}: waited for {self.name} to connect for {time.time() - start:.4f} s.')

EpicsSignalBase.wait_for_connection = wait_for_connection_base
EpicsSignal.wait_for_connection = wait_for_connection
###############################################################################

from ophyd.signal import EpicsSignalBase
if not OLD_BLUESKY:
    EpicsSignalBase.set_defaults(timeout=10, connection_timeout=10)




#test


from bluesky import RunEngine

from bluesky.utils import get_history
RE = RunEngine({})
