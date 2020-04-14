from config.config import pa_user, scream_exec_path, scream_shm_path
import subprocess

import os, time, atexit

process = None

def killer():
    if process:
        if process.poll() is None:
            process.terminate()
        print('Scream exit code', process.wait())

def start():
    global process

    if process is None:
        if pa_user:
            # Impersonate pa_user to avoid issues with local PA servers
            print('Starting scream as uid={}'.format(pa_user))
            cmd = 'su $(id -un {}) -c "{} {}"'.format(
                pa_user,
                scream_exec_path,
                scream_shm_path
            )
            process = subprocess.Popen([cmd],shell=True)
        else:
            print('Starting scream')
            process = subprocess.Popen([scream_exec_path, scream_shm_path])

        print('Started scream')

    # make sure scream dies
    atexit.register(killer)
