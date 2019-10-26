# Project Description 
A simple profiling tool which collects elapsed time for functions and code blocks.

## Usage

Using `statsd`:
```python
from profile_function import ProfileFunction, StatsdBackend
import statsd

statsd_client = statsd.StatsClient('localhost', 8125)
pf = ProfileFunction(StatsdBackend(statsd_client))

@pf.profile_function(group="rpc")
def f(x, y):
    s = 0
    with pf.profile_block("for-loop"):
        for i in range(x):
           s += i * x + y 
    return s
```

Using logger:
```python
from profile_function import ProfileFunction, LoggerBackend
import logging

logger = logging.getLogger(__name__)
pf = ProfileFunction(LoggerBackend(logger, log_level=logging.DEBUG))

@pf.profile_function(group="rpc")
def f(x, y):
    s = 0
    with pf.profile_block("for-loop"):
        for i in range(x):
           s += i * x + y 
    return s
```

## Install

You can install `profile_function` using pip: 
```bash
$ pip install profile-function
```

If you are using `statsd` you need to install it first. This project does not mentioned `statsd` as it own dependency. This command may be useful then:
```bash
$ pip install statsd
```

## Development:
You can write your own collector if you need by implementing `CollectorBackend`.