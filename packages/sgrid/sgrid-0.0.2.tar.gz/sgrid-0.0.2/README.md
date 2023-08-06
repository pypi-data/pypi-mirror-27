# grid

Python class / context manager for starting a headless [Seleneium Grid][1].

Useful for making distributed requests that require a browser, without requiring a GUI. 

```python-docs
>>> from grid import SeleniumGrid
>>> from multiprocessing import Threadpool
>>> links = ['https://www.google.com', ... , 'https://www.yahoo.com']

>>> n_workers = 4
>>> pool = ThreadPool(n_workers)
>>> with SeleniumGrid(num_nodes=n_workers, shutdown_on_exit=True):
        pool.map(grid_request, links)
```

[1]: https://github.com/SeleniumHQ/selenium/wiki/Grid2
