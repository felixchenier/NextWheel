#!/usr/bin/env python3
"""
Main file for the Python-CGI version of the wheel's html interface.

Author : Felix Chenier
Date : October 2019
"""

#---------------------------------
# IMPORTS
#---------------------------------
from subprocess import check_output, Popen, PIPE, STDOUT
from os import listdir
import cgi, cgitb
from config import config  # Specific configuration for this device.
import random

#---------------------------------
# HELPER FUNCTIONS
#---------------------------------
def get_git_changeset():
    """Get current branch as a string."""
    output = check_output(['git', '-C', config['HTMLPath'], 'rev-parse', 'master'])
    output = output.decode('ascii')
    return output[0:6]

def get_available_space():
    """Get available space as a string."""
    output = check_output(['df', '-h', '/'])
    output = output.decode('ascii')
    output = output.split('\n')
    output = output[1].split()    
    return output[3]

def get_available_battery():
    """Get available battery as an int."""
    output = check_output(['sudo', '-u', 'pi', config['HTMLPath'] + 'battery.py'])
    return max(int(output.decode('ascii')), 0)
    
def get_recording():
    """Return True if we are recording."""
    try:
        fid = open(config['HTMLPath'] + 'files/RECORDING', 'r')
    except:
        return False
    fid.close()
    return True


#---------------------------------
# SECTIONS
#---------------------------------
def begin_section(title, full=False):
    """Begin a <div> section with a <h2> title and <pre> formatting."""
    if full is False:
        print('<div class="section"><h2>' + title + '</h2><p class="section">')
    else:
        print('<div class="fullsection"><h2>' + title + '</h2><p class="section">')


def end_section():
    """End the <div> section started with begin_section."""
    print('</p></div>')


def print_header():
    # Tell the web server what follows.
    print("Content-type:text/html\r\n\r\n")

    # Header Section
    print("""
        <!DOCTYPE HTML PUBLIC " -//W3C//DTD HTML 4.01 Transition//EN">
        <html><head>
        <title>Instrumented wheel</title>
        <link rel="stylesheet" href="styles.css">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body>
        <div class="title">
        <h1>Instrumented Wheel</h1>
        <p class="title"><i>Adaptive Sports Biomechanics Lab,
              F&eacute;lix Ch&eacute;nier, UQAM</i></p>
        </div>
        <div class="row">
        """)
        
        
def print_system_state():
    begin_section('System state')
    available_battery = get_available_battery()
    if available_battery < 5:
        print('===============================<br/>')
        print('!!!!!!!!!!! WARNING !!!!!!!!!!!<br/>')
        print('!  BATTERY IS CRITICALLY LOW  !<br/>')
        print('===============================<br/>')
    elif available_battery < 10:
        print('=========================<br/>')
        print('!!!!!!! WARNING !!!!!!!!!<br/>')
        print('!  BATTERY IS VERY LOW  !<br/>')
        print('=========================<br/>')
    elif available_battery < 20:
        print('+==== WARNING =====+<br/>')
        print('|  BATTERY IS LOW  |<br/>')
        print('+==================+<br/>')
    print(f'Battery left: {available_battery}%<br/>')
    print('Space left: ' + get_available_space() + '<br/>')
    print('Firmware changeset: ' + get_git_changeset() + '<br/>')
    
    print("""
        <form action="index.py" method="post">
        <input type="hidden" name="action" value="shutdown">
        <input type='submit' value='Shutdown'>
        </form>
        """)    
    end_section()


def print_record(recording_time, trial_name):
    begin_section('Record')
    
    # Check if it's recording, and allow stopping recording.
    if get_recording():
        print('Currently recording.<br/>')
        print(f'This page will auto-reload after {recording_time+10} seconds.')
        print("""
                <form action="index.py" method="post">
                <input type="hidden" name="action" value="stop_recording">
                <input type='submit' value='Cancel recording'>
                </form>
                """)

    else:
        print(f"""
            <form action="index.py" method="post">
            <input type="hidden" name="action" value="start_recording">
            Trial name:
            <input type="text" name="trial_name" value="{trial_name}"><br/>      
            Length:&nbsp;&nbsp;&nbsp;&nbsp;
            <input type="text" name="recording_time" value="{recording_time}">
            seconds<br/>
            <input type='submit' value='Start'>
            </form>
            """)
    end_section()


def print_files():
    """Print a 'Files List' section contents."""
    begin_section('Files')
    
    # List of files
    file_count = 0
    
    for file in sorted(listdir(config['HTMLPath'] + 'files/')):
        if file[0] != '.' and ('.png' not in file) and ('latest' not in file):
            file_count += 1
            print(f"""
                    <a href="files/{file}">[CSV]</a> 
                    <a href="files/{file + '.png'}">[PNG]</a>
                    {file}<br/>
                    """)
                  
    if file_count == 0:
        print('No recorded file.')
        
    # Files buttons
    print("""
        <form action="index.py" method="post">
        <input type="hidden" name="action" value="confirm_delete_all">
        <input type='submit' value='Delete all files'>
        </form>
        """)

    end_section()
    

def print_figure():
    # Check if a figure exists
    try:
        fid = open(config['HTMLPath'] + 'files/latest.png', 'r')
    except:
        return
    fid.close()
    begin_section('Last acquisition', full=True)
    print(f"""
            <a href="files/latest.png">
            <img src="files/latest.png?nocache={random.randint(0,1E10)}" class="figure"/></a>
            """)
    end_section()
    
    
def print_footer():
    print('</div></body></html>', flush=True)


def print_wait_and_refresh(refresh_time, recording_time, trial_name):
    """Print a script that refreshes the browser after 'time' seconds."""
    print("""
            <script>
            var timer = setTimeout(function() {
               window.location='index.py?recording_time=%s&trial_name=%s'}, %s);
            </script>
            """ % (recording_time, trial_name, 1000*refresh_time))


#---------------------------------
# MAIN
#---------------------------------
def main():

    cgitb.enable()
    
    # LOGIC
    form = cgi.FieldStorage()
    
    if 'recording_time' in form:
        recording_time = int(form['recording_time'].value)
    else:
        recording_time = 10

    if 'trial_name' in form:
        trial_name = form['trial_name'].value.encode('ascii', errors='ignore').decode()  
    else:
        trial_name = ''
    
    
    if 'action' in form:
        action = form['action'].value

        if action == 'start_recording':
        
            # Launch recording
            path = config['HTMLPath']
            Popen([f'sudo -u pi {path}record.py {recording_time} "{trial_name}"&'],
                    shell=True, stdout=PIPE, stderr=STDOUT)
            output = check_output(['sleep 1'], shell=True)

            print_header()
            print_figure()
            print_record(recording_time, trial_name)
            print_wait_and_refresh(recording_time + 10, recording_time, trial_name)
            print_footer()
            return
        
        elif action == 'confirm_delete_all':
        
            print_header()
            begin_section('Confirmation')
            print('Please confirm that you want to delete all files.')
            print("""
                <form action="index.py" method="post">
                <input type="hidden" name="action" value="delete_all">
                <input type='submit' value='Delete all files'>
                </form>
                """)
            print("""
                <form action="index.py" method="post">
                <input type="hidden" name="action" value="">
                <input type='submit' value='Cancel'>
                </form>
                """)
            end_section()
            print_system_state()
            print_footer()
            return
        
        elif action == 'delete_all':
        
            # Do delete
            print_header()
            output = Popen(['sudo -u pi rm ' + config['HTMLPath'] + 'files/*'],
                           shell=True)
            print_wait_and_refresh(0, recording_time, trial_name)
            print_footer()
            return

        elif action == 'shutdown':
        
            # Do delete
            print_header()
            begin_section('Shutdown...')
            print('Please wait 10 seconds, then turn the power switch off.')
            end_section()
            print_wait_and_refresh(0, recording_time, trial_name)
            print_footer()
            output = Popen(['sudo halt'],
                           shell=True)
            return
            
        elif action == 'stop_recording':

            print_header()
            path = config['HTMLPath']
            print_wait_and_refresh(0, recording_time, trial_name)
            print_footer()
            output = Popen([f'sudo rm {path}files/RECORDING'],
                           shell=True)                           
            output = Popen(['sudo killall record.py'],
                           shell=True)            

    # Default
    print_header()
    print_figure()
    print_record(recording_time, trial_name)
    print_system_state()
    print_files()
    print_footer()


#--------------
main()
