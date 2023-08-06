# CubesWriter

A tool that converts [http://cubes.databrewery.org/](Cubes) JSON models into usable, write-layer SQLAlchemy models.


## Installation

```
$ pip install cubeswriter
```

Note: The only addition that Cubes model configs need in order to work with `CubesWriter`, is a object of columns to their types.

For examples, look at the model fixture in  `tests/data/hello_world.json`
