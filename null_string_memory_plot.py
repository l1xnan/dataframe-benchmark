import matplotlib.pyplot as plt
import pandas as pd

mem0 = []
mem1 = []
for i in range(1, 1000):
    strings = ["" for _ in range(i)]
    mem0.append(pd.Series(strings, dtype="string[pyarrow]").memory_usage(deep=True))
    mem1.append(pd.Series(strings, dtype="string").memory_usage(deep=True))

df = pd.DataFrame({
    'string': mem0,
    'arrow': mem1
})
print("mem0", mem0[:5])
print("mem1", mem1[:5])
df.plot.line()
plt.show()
