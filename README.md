# N-Tier Application Generator

Generates n-tier applications from an (implicit) CSV schema or an (explicit) JSON schema.  
The application components (frontend, api) can be run inside docker containers or stand-alone.  
The application database itself is containerized.

## Usage

### First ensure that the toolchain is on the path

```sh
# .bashrc
# toolchain is found at ~/appgen
. ~/appgen/appgen-configure

# or setup manually
```

### Generate an app skeleton using a template

```sh
mkdir testapp
cd testapp
. appgen
```

### Generate an app using a sample configuration inferring the data schema from the CSV

```sh
mkdir todo
cp -R ~/appgen/samples/todo-basic/configure .
./configure/using-csv
```

### Generate an app using a sample configuration using a data schema

```sh
mkdir todo
cp -R ~/appgen/samples/todo-basic/configure .
./configure/using-schema
```

[User Guide](./USER_GUIDE.md)

[Development Guide](./DEVELOPMENT_GUIDE.md)
