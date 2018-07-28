# Example

```
from profile_function import ProfileFunction, StatsdBackend
import statsd

statsd_client = statsd.StatsClient('localhost', 8125)
pf = ProfileFunction(StatsBackend(statsd_client))

@pf.profile_function(group="rpc")
def f(x,y):
    s=0
    with pf.profile_block("for-loop"):
        for i in range(x):
           s += i*x + y 

    return s

```