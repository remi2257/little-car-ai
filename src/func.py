def get_screen_infos(ratio_screen_window):
    import subprocess

    cmd = ['xrandr']
    cmd2 = ['grep', '*']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    p2 = subprocess.Popen(cmd2, stdin=p.stdout, stdout=subprocess.PIPE)
    p.stdout.close()

    resolution_string, junk = p2.communicate()
    resolution = resolution_string.split()[0].decode('utf8')
    width, height = resolution.split('x')
    # print(width,height)
    return int(int(width) // ratio_screen_window), int(int(height) // ratio_screen_window)
