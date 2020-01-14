from aioparse import AIOParse, OpenVpn, HideRandomizer

if __name__ == '__main__':
    vpn = OpenVpn()
    vpn.load_config_files("/home/powersemmi/Downloads/privatevpn")
