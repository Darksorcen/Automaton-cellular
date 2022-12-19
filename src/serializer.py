import json


class Serializer:
    def __init__(self):
        self.data = {}
        self.data_dumped = None

    def convert_data(self, data: dict[tuple[int, int]: bool], rsize: int):
        """
        Serialize the data
        ex : (60, 78) -> "60 78"
        """
        data_to_dump = dict()

        data_to_dump["square_size"] = rsize
        data_to_dump["size"] = max(data.keys())
        data_to_dump["positions"] = dict()

        for pos, v in data.items():
            data_to_dump["positions"][f"{pos[0]} {pos[1]}"] = int(v)

        self.data_dumped = json.dumps(data_to_dump, indent=4)

    def write_to_json(self, filename: str):
        """
        Write to a json file
        """
        with open(filename, "w") as file:
            file.write(self.data_dumped)
