# Development Guide

## Application and component generation

__APPGEN_HOME__ must be defined and on the path

```sh
# example .bashrc appgen configuration
export __APPGEN_HOME__="$HOME/appgen"
export PATH="$PATH:${__APPGEN_HOME__}"
```

```sh
# to create an appgen python environment

appgen # generates a basic application skeleton in the current directory
```

Sample CSV: Tasks.csv

```csv
task,assignee,due_date,status
Test1,Me,Tomorrow,Open
Test,You,Tomorrow,In Progress
Test,Me,Tomorrow,Completed
```

Create a simple API endpoint using a csv file

- this will also generate a csv seed file
- and any required database scripts

```sh
api-endpoint-crud Tasks.csv
```

To generate a non-schema frontend page component, the API must be running

```sh
./docker/backend-start
# populate the data so that the API can supply it
./docker/db-seed

# (optional) check the API
curl http://localhost:3000/api/Tasks

app-page-table-crud http://localhost:3000/api/Tasks
```

Add a menu/route so that the new page is reachable

```sh
app-menu-add --menu=Tasks
```

Start the application via docker

```sh
./docker/app-start

# UI
http://localhost:4200

# Swagger
http://localhost:3000/api-docs

# database
./docker/db-psql
```

## Error Handling - fatal.txt

If an error is detected during app generation, a file 'fatal.txt' is written to the current directory.  
If this happens, inspect the file and correct the issue, then delete the error file before running the app generation again.

**Code generation will be blocked if this file is present.**

## Dependencies

- docker (for the database)
- mise-en-place (mise)
- python (for app component generation from a code template)
- tmux (if running ./tmux/* scripts)

## Schema Analysis

If a csv column contains the suffix '\_enum', then the column is assumed to be a reference.

A two-column enum can be used to specify column names (entity fields).

```sh
api-endpoint-crud "${CSV_DIR}/Task_Fields_Enum.csv"
api-endpoint-be4fe-paged "${CSV_DIR}/Task.csv" --entity-fields=task_fields_enum.csv
```

Specifying --hide as the prefix for an entity field will hide (mask) that column in the frontend.

```csv
task_fields_enum
--hideId
Task
Assigned To
Due By
Status
```

---

## Template Application Samples

[samples for application generation](./samples/README.md)

---

## Naming Conventions

### database

- use lower case
- snake_case_tables
- snake_case_tables_view

### middleware/api

- CamelCaseApiEndpoints

### javascript/typescript

- kebab-case-file-name.js
- kebab-case-file-name.ts
- kebab-case-with-dot.components (presentation layer)
- kebab-case-with-dot.services (presentation layer)
- PascalCaseTypes
- camelCaseVariables (dromedaryCaseVariables)
