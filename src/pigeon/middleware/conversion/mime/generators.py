from typing import Any
import json


class Generator:
    """
    Generates a string represenation of the data depending on the mimetype.
    """
    @classmethod
    def generate(cls, data: Any) -> str:
        raise NotImplementedError


class JSONGenerator(Generator):
    """
    Converts application/json data in any format into str.
    """
    @classmethod
    def generate(self, data: Any) -> str:
        # parse data to string representation
        return json.dumps(data)
