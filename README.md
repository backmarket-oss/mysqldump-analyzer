# mysqldump-analyzer

`mysqldump-analyzer` is a tool to analyze and compare the output of `mysqldump`.


## Install

```sh
make install
```

## Usage

```sh
mysqldump-analyzer diff tests/assets/*.sql
```

## How to contribute?

Install the requirements and the module in editable mode to be able to be able to see the impact of your local changes:
```sh
make init
```

To run the tests:
```sh
make test-unit
```

The SQL dumps in `tests/assets` are generated using `tests/assets/seed.sh`. To alter them, just edit the seed script: they
will be generated again the next time you run `make tests` using Docker.
