from data.data import DataLoading


def main():
    data_loading = DataLoading(
        excel_name="250124 Carga CI.xlsx",
        transaction=True,
        query="INSERT INTO FOIN_CONF_CONFIGURATIONS VALUES ('%s', 3, 40, '%s', 2, '%s', '%s', '%s', '%s', '%s', '%s')",
        audi_query="INSERT INTO AUDI_FOIN_CONF_CONFIGURATIONS VALUES (("
                   "SELECT COCO_ID FROM FOIN_CONF_CONFIGURATIONS WHERE COCO_TITLE = '%s' AND CENTER_NAME = '%s'"
                   "AND AMBIT_NAME = '%s' AND SERVICE_NAME = '%s' AND SPECIALITY_NAME = '%s' "
                   "AND PRESTATION_NAME = '%s' AND FORM_NAME = '%s' AND LANGUAGE = '%s'"
                   "), 1, NULL, NULL, '%s', 3, 40, '%s', 2, '%s', "
                   "'%s', 1, '%s', '%s', '%s', '%s')"
    )

    data_loading.write_sql_query_file()


if __name__ == "__main__":
    main()
