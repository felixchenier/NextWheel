# NextWheel Python module

This folder will contain a `nextwheel` Python module to fetch streamed data from the instrumented wheel. It may contain a `NextWheel` class with the following methods:

- NextWheel.init(ip : str, max_length : int=10) -> NextWheel
- NextWheel.connect() -> bool
- NextWheel.fetch() -> list[dict[str, numpy.array]]
- NextWheel.close() -> None


>>> from nextwheel import NextWheel

>>> nw = NextWheel("xx.xx.xx.xx")
>>> nw.connect()

>>> print(nw.fetch()
    
>>> nw.close()
