# NextWheel Python module

This folder will contain a `nextwheel` Python module to fetch streamed data from the instrumented wheel. It may contain a `NextWheel` class with the following methods:

- NextWheel.connect(ip_address: str) -> bool
- NextWheel.fetch() -> dict[str, numpy.array]
- NextWheel.close() -> None

