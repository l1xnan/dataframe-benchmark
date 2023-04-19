import os
import time
from functools import wraps
from pathlib import Path

import numpy as np
import pandas as pd
import psutil
from faker import Faker


def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss


def process_cpu():
    """
    Getting cpu_percent in last 2 seconds
    """
    cpu_usage = psutil.cpu_percent(2)
    return cpu_usage


# decorator function mem
def profile_mem(func):
    def wrapper(*args, **kwargs):
        mem_before = process_memory()
        result = func(*args, **kwargs)
        mem_after = process_memory()
        print("Consumed memory: {:,}".format(
            mem_before, mem_after, mem_after - mem_before))

        return result

    return wrapper


# decorator function cpu
def profile_cpu(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        cpu_after = process_cpu()
        print(f"Consumed cpu: {cpu_after}")

        return result

    return wrapper


def generate_test_data(size=100000, force=False):
    if Path("test.csv").exists() and not force:
        return
    fake = Faker()
    data = []
    for i in range(size):
        data.append({
            "id": i,
            "ssn": fake.ssn(),
            "name": fake.name(),
            "sex": np.random.choice(["F", "M"]),
            "age": np.random.randint(18, 60),
            "country": fake.country(),
            # "address": fake.address(),
            "birthday": fake.date_of_birth(),
            "datetime": fake.date_time(),
            "decimal": fake.pydecimal(right_digits=4, min_value=-10000, max_value=10000),
            # "detail": fake.text(),
        })

    df = pd.DataFrame.from_records(data)
    df.to_csv("test.csv", index=False, sep="\t")
    df.to_parquet("test.parquet", index=False)


stats_df = pd.DataFrame(columns=["time(s)", "memory(KB)"])


def profile(func):
    @wraps(func)
    def inner(*args, **kwargs):
        start_time = time.perf_counter()
        df = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        param = ",".join(args)
        if kwargs:
            param += "," + ",".join([f"{k}={v}" for k, v in kwargs.items()])
        memory = df.memory_usage(index=False, deep=True).sum() / 1024
        idx = f"{func.__name__}({param})"
        stats_df.loc[idx] = [total_time, memory]
        return df

    return inner


@profile
def read_csv_by_python():
    df = pd.read_csv("test.csv", sep="\t", engine="python")
    return df


@profile
def read_csv_by_pyarrow():
    df = pd.read_csv("test.csv", sep="\t", engine="pyarrow", dtype_backend="pyarrow")
    return df


@profile
def read_parquet_by_default():
    df = pd.read_parquet("test.parquet")
    return df


@profile
def read_parquet_by_pyarrow():
    df = pd.read_parquet("test.parquet", engine="pyarrow", dtype_backend="pyarrow")
    return df


if __name__ == '__main__':
    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", None)
    pd.set_option("display.width", 1000)
    generate_test_data(force=False)
    read_csv_by_python()
    read_csv_by_pyarrow()
    read_parquet_by_default()
    read_parquet_by_pyarrow()
    print(stats_df)
