# Backlog

## Done

- architecture: overall
  - complete homogenous stack per layer (ng-mui, ...)
  - implement completely scripted database-middleware-presentation pipeline
  - paging support
    - pagination extension to endpoints
    - see: <https://apisyouwonthate.com/blog/api-design-basics-pagination/>
- separate configuration from seeding
  - read data config
  - generate tables
  - generate api
  - generate frontend
  - enables generation without relying on endpoint parsing
- architecture: ng-mui
  - move generator functions to separate files
  - implement pipeline
  - add sidepanel
- architecture: express-js-postgres
  - move generator functions to separate files
  - implement pipeline
  - create be4fe API generator
  - export sql to file to enable better control of sql changes
  - fix enum reference constraint to use id rather than field to allow enum name changes
  - brute-force work-around for table dependencies using CASCADE
- confirm csv-based generation: -basic-csv
  - add README in sample explaining steps
  - add sample configuration script
  - add appgen-sample script to copy files
- confirm csv-based generation: -basic-schema
  - add README in sample explaining steps
  - add sample configuration script
  - add appgen-sample script to copy files
- confirm csv-based generation: -advanced-schema
  - add README in sample explaining steps
  - add sample configuration script
  - add appgen-sample script to copy files
- implement separate stacks with domain-specific tasks, but using common jobs
- simplified sourcing requirements for scripts - now only required when selecting an environment
- Replaced XX-init shell scripts with python
- Added springboot + postgres backend

## In Progress

## ToDo

- Implement AuthN/AuthZ
- Integrate GraphQL (e.g. for enrichment)
- Dockerize generation
- Simplify generation dependencies and virtual envs using mise
- Integrate mise into runtime images
- Replace parsing with argparse and add --help
  - https://grp-bio-it-workshops.embl-community.io/intermediate-python/04-argparse/index.html
- Integrate field reference into schema?

---

## Parked

- Workflow concept
  - invert actions on files
  - files contain code execution metadata - e.g.
    - include (x)
    - foreach (y)
    - ...
  - filewatcher
  - drop url on a folder
  - generates component(s), css and html

- architecture: overall
  - containerize appgen

- architecture: ng-mui
  - add dirty check to enum crud similar to "enum-_ru_"
  - add "no data" icon to tables
  - more shared code - eg services, forms
  - fix column name feature via field table (removed from backend)
  - use standard column pattern (indexes, as in be4fe)
  - add FE type info and regexes and validators to schema
    - review validation: <https://danielk.tech/home/angular-material-form-validation>
    - numeric type eg: matInput type="text" inputmode="numeric" pattern="^-?\d\*"

- architecture: express-js-postgres
  - more elegant way to handle table dependencies - with table groups?

- architecture: pipeline
  - add ability to single-step and inspect variables
    - implement a web ui to monitor and control the engine?

- docker
  - internal network to prevent port clashes but with exposure of UI
  - multiple profiles?
