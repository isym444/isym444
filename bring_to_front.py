import pyautogui
import subprocess

def activate_window_with_title(title):
    # Use osascript to bring the window with the given title to the front
    script = f'''
    tell application "Google Chrome"
        repeat with w in windows
            repeat with t in tabs of w
                if title of t is "{title}" then
                    set index of w to 1
                    set active tab index of w to index of t
                    return
                end if
            end repeat
        end repeat
    end tell
    '''
    osa_command = ['osascript', '-e', script]
    subprocess.run(osa_command)

# Use this function to bring the window with the desired title to the front
activate_window_with_title("Desired Tab Title")
