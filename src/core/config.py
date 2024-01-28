from os import path
from typing import List


class Settings:
    output_result_path: str = path.join(path.dirname(path.dirname(__file__)), path.join("output", "results.sql"))
    input_path: str = path.join(path.dirname(path.dirname(__file__)), "input")


settings = Settings()
