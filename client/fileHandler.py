import os
import winreg as reg
from datetime import datetime, timedelta

class FileHandler:
    def __init__(self, file_name: str, reg_path: str):
        self.file_name = file_name
        self.reg_path = reg_path

    def write_number(self, number: int):
        reset_needed = self.check_if_reset_needed()
        if reset_needed:
            self.save()
            self.reset()

        with open(self.file_name, 'a') as f:
            f.write(f'\n{number}')

    def check_if_reset_needed(self):
        with open(self.file_name, 'r') as f:
            datehour_str = f.readline().strip()

            if not datehour_str:
                self.reset()
                return False

            try:
                time_created = datetime.strptime(datehour_str, "%Y-%m-%d %H")
            except ValueError:
                self.reset()
                return False
            current_time = datetime.now()

            return current_time - time_created >= timedelta(hours=1)
        
    def save(self):
        index = self.update_registry_index()
        temp_dir = os.environ.get('TEMP') or os.environ.get('TMP')
        print(temp_dir)
        
        with open(self.file_name, 'r') as original_file:
            file_content = original_file.read()

        with open(os.path.join(temp_dir, 'CyberIsGood', f'{index}.tmp'), 'w') as temp_file:
            temp_file.write(file_content)

    def reset(self):
        now = datetime.now()
        datehour_str = now.strftime('%Y-%m-%d %H')
        with open(self.file_name, 'w') as original_file:
            original_file.truncate(0)
            original_file.write(datehour_str)

    def update_registry_index(self):
        with reg.OpenKey(reg.HKEY_CURRENT_USER, self.reg_path, 0, reg.KEY_ALL_ACCESS) as key:
            current_index, _ = reg.QueryValueEx(key, "temp_file_index")
            next_index = current_index + 1
            reg.SetValueEx(key, "temp_file_index", 0, reg.REG_DWORD, next_index)
            
            return next_index