# Project Description 
An easy profiling tool which collects elapsed time for functions and code blocks.

## Example
Using Statsd
```python
from profile_function import ProfileFunction, StatsdBackend
import statsd

statsd_client = statsd.StatsClient('localhost', 8125)
pf = ProfileFunction(StatsdBackend(statsd_client))

@pf.profile_function(group="rpc")
def f(x,y):
    s=0
    with pf.profile_block("for-loop"):
        for i in range(x):
           s += i*x + y 

    return s

```

Using logger

```python
from profile_function import ProfileFunction, LoggerBackend
import logging
logger = logging.getLogger(__name__)

pf = ProfileFunction(LoggerBackend(logger,log_level=logging.DEBUG))

@pf.profile_function(group="rpc")
def f(x,y):
    s=0
    with pf.profile_block("for-loop"):
        for i in range(x):
           s += i*x + y 

    return s

```
## Installing

Use pip as below 

```pip install profile_function```

If you are using statsd you need to install it. This project does not mentioned statsd as it own dependency.

## Developments:
You can write your own collector if you need by implementing CollectorBackend.
