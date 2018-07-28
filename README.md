# Example

```
from profile_function import ProfileFunction, StatsdBackend

pf = ProfileFunction(StatsBackend(statsd))

@pf.profile_function(group="rpc")
def f(x,y):
    s=0
    with pf.profile_block("for-loop"):
        for i in range(x):
           s += i*x + y 

    return s

```