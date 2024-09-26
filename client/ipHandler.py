import winreg as reg
import re
from exceptions import IPMissingError, InvalidRegistry

class IPHandler:
    def __init__(self, reg_path: str) -> None:
        self.reg_path = reg_path
        
    def extract_from_registry(self):
        try:
            with reg.OpenKey(reg.HKEY_CURRENT_USER, self.reg_path) as key:
                server_ip, _ = reg.QueryValueEx(key, "server_ip")
                server_port, _ = reg.QueryValueEx(key, "server_port")

                if (not server_ip) or (not server_port):
                    raise IPMissingError
                
                return (server_ip, int(server_port))
        
        except FileNotFoundError as e:
            print(e)
            raise InvalidRegistry

    def is_valid_ip(self, ip_string: str):
        pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        return re.match(pattern, ip_string) is not None
    
    def is_valid_port(self, port_string: str):
        try: 
            port = int(port_string)
        except ValueError:
            return False
        else:
            return 0 <= port <= 65535

    def update_ip_port(self, ip_address: str, port: str):
        if not self.is_valid_ip(ip_address) or not self.is_valid_port(port):
            raise ValueError("Invalid ip or port")
        
        try:
            with reg.OpenKey(reg.HKEY_CURRENT_USER, self.reg_path, 0, reg.KEY_SET_VALUE) as key:
                reg.SetValueEx(key, "server_ip", 0, reg.REG_SZ, ip_address)
                reg.SetValueEx(key, "server_port", 0, reg.REG_SZ, port)
                
        except Exception as e:
            raise ValueError("Error writing ip and port")