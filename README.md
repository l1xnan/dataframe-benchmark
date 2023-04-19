Pandas 2.0 Benchmark


```bash
                           time(ms)  memory(KB)                                             dtypes
read_csv_by_python()        449.078   42083.356                      object(6),int64(2),float64(1)
read_csv_by_pyarrow()        24.613    8587.263  string[pyarrow](4),int64[pyarrow](2),date32[da...
read_parquet_by_default()   137.162   42962.263               object(6),int64(2),datetime64[ns](1)
read_parquet_by_pyarrow()    15.123    9405.134  string[pyarrow](4),int64[pyarrow](2),date32[da...
```