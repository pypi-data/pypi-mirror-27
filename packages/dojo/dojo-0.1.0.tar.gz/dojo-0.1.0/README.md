A data framework encapsulating common data warehousing patterns and best practices, including defining and scheduling jobs using Apache Beam on Google Cloud Dataflow, and versioned datasets with schema integrity on inputs and outputs.

[![pipeline status](https://gitlab.com/dataup/dojo/badges/master/pipeline.svg)](https://gitlab.com/dataup/dojo/commits/master) 
[![coverage report](https://gitlab.com/dataup/dojo/badges/master/coverage.svg)](https://gitlab.com/dataup/dojo/commits/master) [![PyPI](https://img.shields.io/pypi/v/nine.svg)](pypi.python.org/pypi/dojo)


# Getting started

```
source script/env
script/up
script/test
```

##### Run a dataset job

```
dojo run <dataset_module>
```

```
dojo --help
```

# TODO:
 - [ ] Validate schema with `jsonschema`
 - [ ] Support other input and output types other than JSON (i.e. CSV, Avro, TFExample)
 - [ ] Contrib datasets for `email`, `mysql`, and `ftp`