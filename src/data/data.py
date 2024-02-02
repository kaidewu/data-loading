import pandas as pd
import numpy as np
from os import path
from typing import List, Optional, Union, Tuple
from core.config import settings
from unidecode import unidecode


class DataLoading:
    def __init__(
            self,
            excel_name: str = "",
            transaction: bool = False,
            environment: str = "PRE",
            query: Optional[str] = "",
            audi_query: Optional[str] = ""
    ) -> None:
        """
        :param excel_name: Name of Excel file
        :param transaction: If it is True the transaction has rollback and if it is False commit the transaction
        :param query: SQL Query of Insert, Update or Delete where it must be inserted with %s operator and match with
                      columns of the Excel
        :param audi_query: SQL Query of Insert and Update of AUDITORY table where it must be inserted with %s operator
                           and match with columns of the Excel
        """
        self.excel_name: str = excel_name
        self.transaction: bool = transaction
        self.environment: str = environment
        self.query: str = query
        self.audi_query: str = audi_query

        # Settings variable
        self.input_path: str = settings.input_path
        self.output_result_path: str = settings.output_result_path
        if self.environment == "PRO":
            self.bbdd_excel: str = settings.bbddpro_excel
        else:
            self.bbdd_excel: str = settings.bbddpre_excel

    def _read_excel_pd(self):
        """
        Get DateFrame of Excel file with Pandas
        :return: DateFrame
        """
        return pd.read_excel(path.join(self.input_path, self.excel_name))

    def _get_columns_name(self) -> List[str]:
        """
        Get the columns names
        :return: List[str]
        """
        return self._read_excel_pd().columns.ravel()

    def _list_each_content(self) -> List[List[str]]:
        """
        List content of each row of Excel file
        :return: List[List[str]]
        """
        return [row.tolist() for index, row in self._read_excel_pd().iterrows()]

    def _list_audi_query(self) -> List[List[str]]:
        return [query*2 for query in self._list_each_content()]

    def _results_query(self) -> Union[List[str] | List]:
        """
        Return list of SQL Query
        :return: List[str]
        """
        if self.query == "":
            return []
        return [self.query % tuple(query) for query in self._list_each_content()]

    def _results_audi_query(self) -> Union[List[str] | List]:
        """
        List of AUDITORY query
        :return: List[str]
        """
        if self.audi_query == "":
            return []
        return [self.audi_query % tuple(audi_query) for audi_query in self._list_audi_query()]

    def write_sql_query_file(self) -> None:
        """
        Open and write a sql file with query
        :return: None
        """
        with open(self.output_result_path, "w", encoding="utf-8") as results:
            results.write(
                f"BEGIN TRANSACTION\n"
                f"{'\n'.join(self._results_query())}\n"
                f"{'\n'.join(self._results_audi_query())}\n"
                f"{"COMMIT" if not self.transaction else "ROLLBACK"}\n"
            )

    def _get_zip_results_args(self, arg: str):
        df = pd.read_excel(self.bbdd_excel, sheet_name=arg)
        list_results_id: List[str] = []
        list_results_name: List[str] = []
        for data in self._read_excel_pd()[arg].tolist():
            df_bbdd = df[df[arg].apply(lambda s: unidecode(s)) == unidecode(data)]
            for content in df_bbdd[f"{arg}_ID"].tolist():
                list_results_id.append(content if pd.notna(content) else np.nan)
            for content in df_bbdd[arg].tolist():
                list_results_name.append(content if pd.notna(content) else np.nan)
        return zip(list_results_id, list_results_name)

    def get_data_from_bbdd(self, *args):
        with pd.ExcelWriter(settings.output_bbdd_path) as excel:
            for arg in args:
                df_excel = pd.DataFrame(list(self._get_zip_results_args(arg)), columns=[f"{arg}_ID", arg])
                df_excel.to_excel(excel, sheet_name=arg, index=False)
