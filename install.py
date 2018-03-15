import os
import platform

from crontab import CronTab

platform_type = platform.system()

sh_file_name = 'DDNStool.sh'
dir_path = os.path.dirname(os.path.realpath(__file__))
sh_file_path = os.path.join(dir_path, sh_file_name)


def install_linux():
    cmd_1 = 'cd ' + dir_path + '\n'
    cmd_2 = 'python3 ./ddnstool.py' + '\n'

    with open(sh_file_name, mode='w') as f1:
        f1.write(cmd_1)
        f1.write(cmd_2)
    # 添加可执行权限
    os.popen('chmod +x ' + sh_file_name)

    # 添加 CronTab 任务
    DDNS_cron = CronTab(user=True)
    DDNS_cron.remove_all(comment='DDNS Job')
    job = DDNS_cron.new(command=('bash ' + sh_file_path))
    job.minute.every(10) # 若要更改启动间隔时间，可更改此值
    job.set_comment("DDNS Job")
    job.enable(enabled=True)
    DDNS_cron.write()


def install_win():
    cmd_1 = 'cd ' + dir_path + '\n'
    cmd_2 = 'python ./ddnstool.py' + '\n'

    with open(sh_file_name, mode='w') as f1:
        f1.write(cmd_1)
        f1.write(cmd_2)


# res  = os.popen('python -V')

if platform_type == "Linux":
    install_linux()
elif platform_type == "Windows":
    # install_win()
    print('Currently not support!')
else:
    print('Do not support!')
    exit()
