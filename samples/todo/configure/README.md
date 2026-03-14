# Configurator

Transformation pipeline

## config/generate-schema

```sh
. appgen-venv
raw-csv-to-schema ./config/csv_raw/PascalCase.csv

./config/csv_raw/PascalCase.csv
-> ./config/schema_csv/snake_case.csv
-> ./config/schema_json/snake_case.json
-> ./backend/database/csv_seed/snake_case.csv
```

