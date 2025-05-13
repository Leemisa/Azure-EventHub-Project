import subprocess
import sys
import os

def run_script(script_name):
    """Launch a Python script as a separate process."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script_name)
    return subprocess.Popen([sys.executable, path])

if __name__ == '__main__':
    global_script = 'GlobalStocks.py'
    local_script  = 'LocalStocks.py'

    print('Launching both stock streams...')
    proc_global = run_script(global_script)
    proc_local  = run_script(local_script)

    print(f'Global stream PID: {proc_global.pid}, Local stream PID: {proc_local.pid}')

    try:
        proc_global.wait()
        proc_local.wait()
    except KeyboardInterrupt:
        print('Stopping both streams...')
        proc_global.terminate()
        proc_local.terminate()
        proc_global.wait()
        proc_local.wait()
        print('Both streams stopped.')
