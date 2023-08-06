import re
import os
import sys
import glob
import subprocess
import argparse


def powershell(ps_script, car_return=False):
    ps_path = "C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe"
    result = subprocess.check_output([ps_path, ps_script])
    result = result.decode('windows-1252')
    
    if car_return:
        return result
    
    else:
        # Remove carriage returns.
        result = re.sub('\r', '', result, re.X)
        return result


def find_win_exe(application_name=None):
    ps_script = """
    $loc = Get-ChildItem HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall

    $names = $loc |foreach-object {Get-ItemProperty $_.PsPath}

    foreach ($name in $names)
    {
    Write-Host $name.DisplayName, '|',$name.UninstallString
    }
    """
    result = powershell(ps_script).split('\n')
    result = list(map(lambda x:x.split('|'), result))
    # Remove all the extra white space.
    result = list(map(lambda x:[i.strip().strip('"') for i in x], result))
    
    result = list(filter(lambda x: application_name in x[0], result))
    
    result = list(map(lambda x: [x[0],os.path.split(x[-1])[0]], result))
    
    return result

	
def find_python_distro(distro_name=None):
    exe_list = find_win_exe(distro_name)
    
    if len(exe_list) > 0:
        exe_dir = exe_list[0][-1]
        
        python_dir = os.path.join(exe_dir, 'Python.exe')
        
        if os.path.exists(python_dir):
            scripts_dir = os.path.join(exe_dir, 'Scripts')
        
            dirs = [exe_dir, scripts_dir]
        
            if all(list(map(os.path.exists, dirs))):
                return dirs
    

#distro_dirs = find_python_distro('Anaconda')

def find_distro_exe(distro_name, exe):
	distro_dirs = find_python_distro(distro_name)
	
	top_level = glob.glob(os.path.sep.join([distro_dirs[0], '*{}*.exe'.format(exe)]))
	script_level = glob.glob(os.path.sep.join([distro_dirs[-1], '*{}*.exe'.format(exe)]))
	
	if len(top_level) > 0:
		return top_level[0]
		
	if len(script_level) > 0:
		return script_level[0]
	
	

# Commandline interface
parser = argparse.ArgumentParser()

parser.add_argument("-d", "--distro",
                    type=str,
                    nargs='?',
                    const="",
                    default="Anaconda3")
					
parser.add_argument("executable", # "-x", "--executable",
                    type=str,
                    nargs='?',
                    const="",
                    default="")
					
parser.add_argument("-c", "--command",
                    type=str,
                    nargs='?',
                    const="",
                    default="")
					
args = parser.parse_args()

def main():

	cmd = find_distro_exe(args.distro, args.executable)
	
	if len(args.command) == 0:
		print(powershell(cmd))
	else:
		cmd = ' '.join([cmd, args.command])
		print(powershell(cmd))
