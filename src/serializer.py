import json


class Serializer:
    def __init__(self):
        self.data = {}
        self.data_dumped = None

    def convert_data(self, data: dict[tuple[int, int]: bool]):
        data_to_dump = dict()
        for pos, v in data.items():
            data_to_dump[f"{pos[0]} {pos[1]}"] = int(v)

        self.data_dumped = json.dumps(data_to_dump)

    def write_to_json(self, filename: str):
        with open(filename, "w") as file:
            file.write(self.data_dumped)
