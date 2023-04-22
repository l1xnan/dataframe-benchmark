import random

import pandas as pd

strings = [str(random.random()) for i in range(1_000_000)]
strings = ["" for i in range(1_000_000)]


def print_mem(type_, s: pd.Series):
    print(type_, str(round(s.memory_usage(deep=True) / 1024 ** 2, 2)).rjust(6, " ") + " MB", sep="\t")


# The default dtype, object:
object_dtype = pd.Series(strings)
print_mem("object", object_dtype)

# A normal Pandas string dtype:
standard_dtype = pd.Series(strings, dtype="string")
print_mem("string", standard_dtype)

# The new Arrow string dtype from Pandas 1.3:
arrow_dtype = pd.Series(strings, dtype="string[pyarrow]")
print_mem("arrow", arrow_dtype)

import random

import pandas as pd


def print_mem(s: pd.Series):
    print(str(s.dtype), str(round(s.memory_usage(deep=True) / 1024 ** 2, 2)).rjust(6, " ") + " MB", sep="\t")


nums = [random.randint(-128, 127) for _ in range(1_000_000)]
print_mem(pd.Series(nums))
print_mem(pd.Series(nums, dtype="int8"))
print_mem(pd.Series(nums, dtype="int8[pyarrow]"))
print_mem(pd.Series(nums, dtype="int16"))
print_mem(pd.Series(nums, dtype="int16[pyarrow]"))
