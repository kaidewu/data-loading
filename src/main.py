from os import path
from data.data import Data
from core.config import settings


def main():
    data_loading = Data(
        excel_name="250124 Carga CI.xlsx",
        query="INSERT INTO FOIN_CONF_CONFIGURATIONS VALUES ('%s', 3, 40, '%s', 2, '%s', '%s', '%s', '%s', '%s', '%s')",
        audi_select_id="SELECT COCO_ID FROM FOIN_CONF_CONFIGURATIONS WHERE COCO_TITLE = '%s' AND CENTER_NAME = '%s'"
                       "AND AMBIT_NAME = '%s' AND SERVICE_NAME = '%s' AND SPECIALITY_NAME = '%s' "
                       "AND PRESTATION_NAME = '%s' AND FORM_NAME = '%s' AND LANGUAGE = '%s'",
        audi_query="INSERT INTO AUDI_FOIN_CONF_CONFIGURATIONS VALUES ((%s), 1, NULL, NULL, '%s', 3, 40, '%s', 2, '%s', "
                   "'%s', 1, '%s', '%s', '%s', '%s')"
    )

    with open(path.join("output", "results.sql"), "w", encoding="utf-8") as results:
        for query, audi_query in zip(data_loading.results_query(), data_loading.results_audi_query()):
            results.write(
                f"{query}\n{audi_query}\n"
            )


if __name__ == "__main__":
    main()
