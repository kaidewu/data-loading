import pandas as pd
from os import path
from typing import List, Optional, Any
from core.config import settings


class DataLoading:
    def __init__(
            self,
            excel_name: str,
            transaction: bool,
            query: str,
            audi_query: str
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
        self.query: str = query
        self.audi_query: Optional[str] = audi_query

        # Settings variable
        self.input_path: str = settings.input_path
        self.output_result_path: str = settings.output_result_path

    def _read_excel_pd(self) -> Any:
        """
        Get DateFrame of Excel file with Pandas
        :return: DateFrame
        """
        return pd.read_excel(path.join(self.input_path, self.excel_name))

    def _get_columns_name(self) -> Any:
        """
        Get the columns names
        :return: I guess Index. Better go to the Pandas documents to read it
        """
        return self._read_excel_pd().columns

    def _list_each_content(self) -> List[List[str]]:
        """
        List content of each row of Excel file
        :return: List[List[str]]
        """
        return [row.tolist() for index, row in self._read_excel_pd().iterrows()]

    def _list_audi_query(self) -> List[List[str]]:
        return [query*2 for query in self._list_each_content()]

    def _results_query(self) -> List[str]:
        """
        Return list of SQL Query
        :return: List[str]
        """
        return [self.query % tuple(query) for query in self._list_each_content()]

    def _results_audi_query(self) -> List[str]:
        """
        List of AUDITORY query
        :return: List[str]
        """
        return [self.audi_query % tuple(audi_query) for audi_query in self._list_audi_query()]

    def write_sql_query_file(self) -> None:
        """
        Open and write a sql file with query
        :return: None
        """
        with open(self.output_result_path, "w", encoding="utf-8") as results:
            for query, audi_query in zip(self._results_query(), self._results_audi_query()):
                if not self.transaction:
                    results.write(
                        f"BEGIN TRANSACTION\n"
                        f"{query}\n"
                        f"{audi_query}\n"
                        f"COMMIT\n"
                    )
                else:
                    results.write(
                        f"BEGIN TRANSACTION\n"
                        f"{query}\n"
                        f"{audi_query}\n"
                        f"ROLLBACK\n"
                    )

