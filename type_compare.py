"""
https://arrow.apache.org/docs/python/api/datatypes.html
"""
import numpy as np
import pandas as pd
from faker import Faker

SIZE = 10000

fake = Faker()


def print_mem(s: pd.Series):
    print(str(s.dtype).ljust(20, " "), s.memory_usage(deep=True))


def benchmark():
    s = pd.Series([np.random.randint(-128, 127) for _ in range(SIZE)])
    print_mem(s)
    print_mem(s.astype(np.int8))
    print_mem(s.astype("int8[pyarrow]"))
    print_mem(s.astype("int16[pyarrow]"))
    print_mem(s.astype("int32[pyarrow]"))
    print_mem(s.astype("int64[pyarrow]"))

    s = pd.Series(fake.address() for _ in range(SIZE))
    print_mem(s)
    print_mem(s.astype("string"))
    print_mem(s.astype("string[pyarrow]"))

    s = pd.Series([np.random.choice([True, False]) for _ in range(SIZE)])
    print_mem(s)
    print_mem(s.astype(np.bool_))
    print_mem(s.astype("bool[pyarrow]"))

    s = pd.Series([np.random.random() for _ in range(SIZE)])
    print_mem(s)
    print_mem(s.astype(np.float_))
    print_mem(s.astype("float32[pyarrow]"))
    print_mem(s.astype("float64[pyarrow]"))

    s = pd.Series(list(pd.date_range("20230420", SIZE)))
    print_mem(s)
    print_mem(s.astype("datetime64[ns]"))
    print_mem(s.astype("date64[pyarrow]"))

    s = pd.Series([[1, 2, 3, 4] for _ in range(SIZE)])
    print_mem(s)


if __name__ == '__main__':
    benchmark()
