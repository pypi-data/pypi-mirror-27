# coding: utf-8
import re
import subprocess


def get_ip4():
    """
    return all ip v4 address of current computer
    :return:
    """
    addresses = []

    shell_cmd = "ifconfig | awk '/inet addr/{print substr($2,6)}'"
    proc = subprocess.Popen([shell_cmd], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    ip_addresses = out.split('\n')
    for addr in ip_addresses:
        if re.match(r'\d{1,4}\.\d{1,4}\.\d{1,4}\.\d{1,4}', addr):
             addresses.append(addr)
    return addresses
