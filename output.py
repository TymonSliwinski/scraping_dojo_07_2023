import abc
import json

class BaseOutput(abc.ABC):
    @abc.abstractmethod
    def write(self, data: dict):
        return NotImplemented


class JSONOutput(BaseOutput):
    def __init__(self, output_file):
        self.output_file = open(output_file, 'a', encoding='utf-8')
    
    def __del__(self):
        self.output_file.close()

    def write(self, data: dict):
        self.output_file.write(json.dumps(data) + ',\n')
        self.output_file.flush()
