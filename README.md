# Script for data loading
Python script for data massive loading of Excel file into your database. 
Instead of write the insert, update or delete by hand, 
with this script it will be automatically passing your query as parameter.
### Example
Excel file

```
| Name         | Address    | City       |
|--------------|------------|------------|
| Joze         | Gran via   | Madrid     |
| Jhonny       | Street Down| London     |
|...           |...         |...         |
```

SQL Query

```sql
INSERT INTO {Your table name} VALUES (%s, %s, %s)
```

Python Data class
```python
data = Data(
    excel_name="excel_name.xlsx",
    query="INSERT INTO {Your table name} VALUES (%s, %s, %s)"
)
data.results_query()
```

Result:
```
INSERT INTO {Your table name} VALUES (Joze, Gran via, Madrid)
INSERT INTO {Your table name} VALUES (Jhonny, Street Down, London)
```

### Setting up the project:
1. Clone the GitHub repository:

```bash
git clone https://github.com/kaidewu/data-loading
```

1. Navigate to the project directory:

```bash
cd data-loading
```

2. (Recommended) Create a Python virtual environment: You can follow the Python official documentation for virtual environments.

```bash
python3 -m venv venv
```

3. Activate the virtual environment:
  
  - On Windows:

    ```
    .\venv\Scripts\activate
    ```

  - On MacOS and Linux:
  
    ```bash
    source venv/bin/activate
    ```

4. Install the required Python packages from requirements.txt:

```bash
pip install -r requierements.txt
```
