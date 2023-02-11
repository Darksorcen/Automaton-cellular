import json


class Deserializer:
    def __init__(self):
        self.data_deserialized = {}
        self.data_to_deserialize = {}

    def deserialize(self):
        """
        Deserialize the data
        ex : "60 78" -> (60, 78)
        """
        for pos, v in self.data_to_deserialize.get("positions", {}).items():
            self.data_deserialized[tuple(map(int, pos.split()))] = v

        rsize = self.data_to_deserialize.get("square_size", 0)

        return self.data_deserialized, rsize

    def read_json(self, filename: str):
        """
        Read json file
        """
        try:
            with open(filename, "r") as file:
                self.data_to_deserialize = json.load(file)
        except json.decoder.JSONDecodeError:
            print("Loading file : Failed !")
            print("The json file is invalid")
