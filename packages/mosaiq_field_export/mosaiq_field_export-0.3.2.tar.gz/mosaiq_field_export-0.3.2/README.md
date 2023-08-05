# Mosaiq field export

## Example usage

```python
import numpy as np

from mosaiq_connection import sql_connection, patient_fields
from mosaiq_field_export import pull_sql_data

PATIENT_ID = 'a_patient_id'
CENTRE_NAME = 'centre_name'
SQL_USERS = { CENTRE_NAME: 'mosaiq_database_login' }
SQL_SERVERS = { CENTRE_NAME: 'mosaiq_server_network_hostname' }

with sql_connection(SQL_USERS, SQL_SERVERS) as cursors:
    cursor = cursors[CENTRE_NAME]

    fields_details = patient_fields(cursor, PATIENT_ID)
    latest_version = np.array([
        item[3] for item in fields_details
    ]) == 0
    has_mu = np.array([
        item[4] for item in fields_details
    ]) > 0

    fields = np.array([
        item[0] for item in fields_details
    ])[latest_version & has_mu]

    data = pull_sql_data(cursor, fields)
    print(data)
```