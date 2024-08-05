import pandas as pd
import pyarrow
from pyarrow import csv
import random
from random import sample 


columns_nonculled = ["ID",
                    "Severity",
                    "State",
                    "Temperature(F)",
                    "Humidity(%)",
                    "Visibility(mi)",
                    "Wind_Speed(mph)",
                    "Precipitation(in)"
                    ]

def sample_table(table: pyarrow.Table, n_sample_rows: int = None) -> pyarrow.Table:
    if n_sample_rows is None or n_sample_rows >= table.num_rows:
        return table

    indices = random.sample(range(table.num_rows), k=n_sample_rows)

    return table.take(indices)

source_df = csv.read_csv("US_Accidents_March23.csv").select(columns_nonculled)

car_safety = sample_table(source_df, 500_000)

csv.write_csv(car_safety, "crash_data_prepped.csv")
