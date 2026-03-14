# Application Generator

Generates n-tier applications from an (implicit) CSV schema or an (explicit) JSON schema.  
The application components (frontend, api) can be run inside docker containers or stand-alone.  
The application database itself is containerized.

## Application and component generation

__APPGEN_HOME__ must be defined and ${__APPGEN_HOME__}/scripts on the path

```sh
# example .bashrc appgen configuration
export __APPGEN_HOME__="$HOME/appgen"
export PATH="$PATH:${__APPGEN_HOME__}/scripts"
```

```sh
# to create an appgen python environment

appgen # generates a basic application skeleton in the current directory
```

Generate an app skeleton using a template

```sh
mkdir testapp
cd testapp
appgen
```

Generate an app using a sample configuration inferring the data schema from the CSV

```sh
mkdir todo
cp -R $__APPGEN_HOME__/samples/todo-basic/configure .
./configure/using-csv
```

Generate an app using a sample configuration using a data schema

```sh
mkdir todo
cp -R $__APPGEN_HOME__/samples/todo-basic/configure .
./configure/using-schema
```

## Schema Analysis

If a csv column contains the suffix \_enum, then the column is assumed to be a reference.

A two-column enum can be used to specify column names (entity fields).

```sh
api-endpoint-crud "${CSV_DIR}/Task_Fields_Enum.csv"
api-endpoint-be4fe-paged "${CSV_DIR}/Task.csv" --entity-fields=task_fields_enum.csv
```

specifying --hide as the prefix for an antity field will hide (mask) that column in the frontend.

```csv
task_fields_enum
--hideId
Task
Assigned To
Due By
Status
```

## How to use a generated app

[User Guide](./samples/README.md)

## Error Handling - fatal.txt

If an error is detected during app generation, a file 'fatal.txt' is written to the current directory.  
If this happens, inspect the file and correct the issue, then delete the error file before running the app generation again.

**Code generation will be blocked if this file is present.**

## Dependencies

- docker (for the database)
- mise-en-place (mise)
- python (for app component generation from a code template)
- tmux (if running ./tmux/* scripts)

**Code generation dependencies are installed via mise.**
