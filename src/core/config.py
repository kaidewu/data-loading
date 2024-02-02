from os import path


class Settings:
    output_result_path: str = path.abspath(path.join(path.dirname(path.dirname(__file__)), path.join("output", "results.sql")))
    input_path: str = path.abspath(path.join(path.dirname(path.dirname(__file__)), "input"))
    output_bbdd_path: str = path.abspath(path.join(path.dirname(path.dirname(__file__)), path.join("output", "bbdd.xlsx")))
    bbddpre_excel: str = path.abspath(path.join(path.dirname(__file__), path.join("data_excel", "BBDDPREASCIRES.xlsx")))
    bbddpro_excel: str = path.abspath(path.join(path.dirname(__file__), path.join("data_excel", "BBDDPROASCIRES.xlsx")))


settings = Settings()
