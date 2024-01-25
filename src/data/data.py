import pandas as pd
from os import path
from typing import List


class Data:
    def __init__(
            self,
            excel_name: str,
            query: str,
            audi_select_id: str,
            audi_query: str
    ) -> None:
        """
        :param excel_name: Name of Excel file
        :param query: SQL Query of Insert, Update or Delete where it must be inserted with %s operator and match with
                      columns of the Excel
        :param audi_select_id: SQL Query of Select to get the ID of the insert of query to insert into AUDITORY table
        :param audi_query: SQL Query of Insert and Update of AUDITORY table where it must be inserted with %s operator
                           and match with columns of the Excel
        """
        self.excel_name: str = excel_name
        self.query: str = query
        self.audi_select_id = audi_select_id
        self.audi_query = audi_query

    def _read_excel_pd(self):
        """
        Get DateFrame of Excel file with Pandas
        :return: DateFrame
        """
        return pd.read_excel(path.join(path.dirname(path.dirname(__file__)), path.join("input", self.excel_name)))

    def _get_columns_name(self):
        """
        Get the columns names
        :return: I guess Index. Better go to the Pandas documents to read it
        """
        read_excel = self._read_excel_pd()
        return read_excel.columns

    def _list_each_content(self) -> List[List[str]]:
        """
        List content of each row of Excel file
        :return: List[List[str]]
        """
        return [row.tolist() for index, row in self._read_excel_pd().iterrows()]

    def _query_select_id(self) -> List[str]:
        return [self.audi_select_id % tuple(data) for data in self._list_each_content()]

    def results_query(self) -> List[str]:
        """
        Return list of SQL Query
        :return: List[str]
        """
        return [self.query % tuple(data) for data in self._list_each_content()]

    def results_audi_query(self) -> List[str]:
        return [self.audi_query % (select_id, *data)
                for select_id, data in zip(self._query_select_id(), self._list_each_content())]

