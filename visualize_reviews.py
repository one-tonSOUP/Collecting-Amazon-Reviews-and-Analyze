## This is a testing file..
## Visualization is done in the "CollectingReviewsfromAmazon.ipynb" file..

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from datetime import datetime

def get_date(text):
    matched_date = re.search(r'\d{2} [a-zA-Z]+ \d{4}', text) or re.search(r'\d{1} [a-zA-Z]+ \d{4}', text)
    if matched_date == None:
        return "No Date found.."
    else:
        date_found = datetime.strptime(matched_date.group(), "%d %B %Y").date()
        return date_found

print(get_date("Reviewed in India 🇮🇳 on 8 October 2022"))
print(type(get_date("Reviewed in India 🇮🇳 on 8 October 2022")))

"Rating(Out of 5)"

def visualize():
    df = pd.read_csv('Xiaomi 12 Pro(Visited on January 31 2023, 15-16-29).csv')
    print(df.head())
    print("\n\n\n\n\n\n\n\n")
    print(df["Date of Review"])
    print(df["Rating(Out of 5)"])

visualize()