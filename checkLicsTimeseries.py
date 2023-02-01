import os
from datetime import datetime
import re
import matplotlib.pyplot as plt
import numpy as np

# Finds all the dates available from the lics ifg directory. Gaps of 12 days are highlighted in blue while gaps greater than 12 are highlighted in red.

url = input("Paste url to index on lics portal: ")

os.system(f"wget {url}")

with open("index.html") as file:
    lines = file.readlines()

os.system("rm -f index.html")

dates_between06 = []
dates_between12 = []
dates = []

for line in lines:
    if 'alt="[DIR]"' in line:
        date1, date2 = re.findall(r"\d+", line)[:2]
        date1_dt = datetime.strptime(date1, "%Y%m%d")
        date2_dt = datetime.strptime(date2, "%Y%m%d")

        if date1_dt not in dates:
            dates.append(date1_dt)

        diff = (date2_dt - date1_dt).days

        if diff == 6:
            dates_between06.append(date2_dt)
        if diff == 12:
            dates_between12.append(date2_dt)

dates_between = [(dates[i] - dates[i + 1]).days for i in np.arange(len(dates) - 1)]

ix_grt12 = np.where(abs(np.array(dates_between)) > 12)[0]
ix_12 = np.where(abs(np.array(dates_between)) == 12)[0]

fig, ax = plt.subplots()

ax.scatter(dates, np.ones(len(dates)), color="green", s=1)

for i in ix_grt12:
    ax.axvspan(dates[i], dates[i + 1], color="red", alpha=0.3)
for i in ix_12:
    ax.axvspan(dates[i], dates[i + 1], color="blue", alpha=0.3)

ax.set_xlabel("Date")
ax.set_title(url, fontsize=8)
plt.show()
