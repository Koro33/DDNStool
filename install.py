import os
import platform

pf_info = platform.system()
# path = os.path.join(os.path.dirname(os.path.realpath(__file__)), __file__)
path = os.path.dirname(os.path.realpath(__file__))

sh_filenane = 'DDNStool.sh'


def install_linux():
    cmd_1 = 'cd ' + path + '\n'
    cmd_2 = 'python3 ./DDNStool.py' + '\n'

    with open(sh_filenane, mode='w') as f1:
        f1.write(cmd_1)
        f1.write(cmd_2)

    os.popen('chmod +x '+ sh_filenane) # 添加可执行权限

def install_win():
    cmd_1 = 'cd ' + path + '\n'
    cmd_2 = 'python ./DDNStool.py' + '\n'

    with open(sh_filenane, mode='w') as f1:
        f1.write(cmd_1)
        f1.write(cmd_2)


# res  = os.popen('python -V')

if pf_info == "Linux":
    install_linux()
elif pf_info == "Windows":
    install_win()
else:
    print('Do not support')
    exit()
