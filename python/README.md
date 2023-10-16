# NextWheel Python module

To install the Python module:

```
pip install git+https://github.com/felixchenier/NextWheel.git#subdirectory=python
```

To use the module:

```python
>>> from nextwheel import NextWheel

>>> nw = NextWheel("xx.xx.xx.xx")
>>> nw.connect()

>>> print(nw.fetch())
    
>>> nw.close()
```
