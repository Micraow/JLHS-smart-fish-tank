import os
ds18b20 = ''  # 用于存储序列号，该型号传感器有出厂唯一序列号

""""
编辑/boot/config.text文件。在文件底部添加一行：dtoverlay=w1-gpio

重启树莓派系统。

检查驱动是否装载：
sudo modprobe w1-gpio
sudo modprobe w1-therm
cd /sys/bus/w1/devices/
ls

示例输出：
pi@raspberrypi:/sys/bus/w1/devices $ cd 28-XXXXXXXXXXXX
pi@raspberrypi:/sys/bus/w1/devices/28-XXXXXXXXXXXX $ ls
driver  hwmon  id  name  power  subsystem  uevent  w1_slave
pi@raspberrypi:/sys/bus/w1/devices/28-XXXXXXXXXXXX $ cat w1_slave 
16 01 55 05 7f a5 a5 66 b5 : crc=b5 YES
16 01 55 05 7f a5 a5 66 b5 t=17334

t=...除以1000是温度
crc是校验码，暂时不检验了，一般不会出问题。

"""

def get():
    """使用ds18b20温度传感器，获取数据"""
    global ds18b20
    for i in os.listdir('/sys/bus/w1/devices'):
        # os.listdir(path) 返回path指定的文件夹包含的文件或文件夹的名字的列表

        if i != 'w1_bus_master1':
            # 里面除了文件'w1_bus_master1'，另外一个就是温度数据文件所在的文件夹

            ds18b20 = i
    # 将温度数据文件所在的文件夹名赋值给全局变量ds18b20

    location = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'
    # location是温度数据文件的地址

    tfile = open(location)
    # os.open(file, flags[, mode])打开一个文件
    text = tfile.read()
    #  os.read(fd, n)从文件描述符 fd 中读取最多 n 个字节，返回包含
    #  读取字节的字符串，文件描述符 fd对应文件已达到结尾, 返回一个空字符串。

    tfile.close()
    # os.close(fd)关闭文件描述符 fd

    secondline = text.split("\n")[1]
    #   string.split(str="", num=string.count(str))
    #   以 str 为分隔符切片 string，如果 num 有指定值，则仅分隔 num+ 个子字符串
    # 计算机里序号是从0开始计算，取1即是第二行

    temperaturedata = secondline.split(" ")[9]
    # 以空格为分隔符，取序号为9的字符段，如：t=17375

    temperature = float(temperaturedata[2:])
    # 取字符串（如：t=17375）第2位及以后部分，即数字部分17375

    temperature = temperature / 1000
    return temperature
