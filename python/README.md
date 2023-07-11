# NextWheel Python module

This folder will contain a `nextwheel` Python module to fetch streamed data from the instrumented wheel. It may contain a `NextWheel` class with the following methods:

- NextWheel.init(ip : str) -> NextWheel
- NextWheel.connect(max_imu_samples : int=1000, max_analog_samples : int=1000, max_encoder_samples : int=100, max_power_samples: int=10) -> bool
- NextWheel.fetch() -> dict[dict[str, numpy.array]]
- NextWheel.close() -> None


```
>>> from nextwheel import NextWheel

>>> nw = NextWheel("xx.xx.xx.xx")
>>> nw.connect()

>>> print(nw.fetch())
    
>>> nw.close()
```
