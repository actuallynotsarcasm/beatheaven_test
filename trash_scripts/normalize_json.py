import json
from tempfile import SpooledTemporaryFile

def normalize(json_string: str):
    virtual_file = SpooledTemporaryFile(mode='wr')
    try:
        virtual_file.write(json_string)
        data = json.loads(json_string)
        normal_json = json.dumps(data, indent=4)
        virtual_file.close()
        return normal_json
    except Exception as e:
        virtual_file.close()
        raise e