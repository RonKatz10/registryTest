import winreg as reg

class RegistryHandler:
    def __init__(self):
        self.regPath = r"Software\CyberIsGood\Server\Ips"

        #ensure registry key exists
        try:
            reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, self.regPath)
        except FileNotFoundError:
            reg_key = reg.CreateKey(reg.HKEY_CURRENT_USER, self.regPath)
        finally:
            reg.CloseKey(reg_key)

    def increment_or_create_counter(self, value: str):
        with reg.OpenKey(reg.HKEY_CURRENT_USER, self.regPath, 0, reg.KEY_ALL_ACCESS) as key:
            try:
                current_value, _ = reg.QueryValueEx(key, value)
            except FileNotFoundError: #value doesnt exist for user
                current_value = 0

            new_value = current_value + 1
            reg.SetValueEx(key, value, 0, reg.REG_DWORD, new_value)
            return new_value