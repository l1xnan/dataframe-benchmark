Pandas 2.0 Benchmark


```bash
                           time(ms)  memory(KB)                         dtypes
read_csv_by_python()       7728.652  420809.795  object(6),int64(2),float64(1)
read_csv_by_pyarrow()       122.807   85848.857  string[pyarrow](4),int64[p...
read_parquet_by_default()  1955.169  429598.857  object(6),int64(2),datetim...
read_parquet_by_pyarrow()    86.691   94027.568  string[pyarrow](4),int64[p...
read_csv_by_polars()       1170.595           -                              -
```