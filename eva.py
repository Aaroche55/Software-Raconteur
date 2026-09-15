import json
from datetime import datetime 
import matplotlib.pyplot as plt

with open("eva-data.json", "r", encoding="utf-8") as file:
    eva_data = json.load(file)

selected_country = input("Enter the country to report: ").strip()
records = []
total_hours = 0

for eva in eva_data:
    if eva.get("country", "").strip().casefold() != selected_country.casefold():
        continue

    date_text = eva.get("date")
    duration_text = eva.get("duration")

    if not duration_text:
        continue

    hours, minutes = map(int, duration_text.split(":"))
    duration_hours = hours + minutes / 60
    total_hours += duration_hours

    if not date_text:
        continue

    date = datetime.fromisoformat(date_text)
    records.append((date, duration_hours))

print(f"Total EVA duration for {selected_country}: {total_hours:.2f} hours")

records.sort(key=lambda record: record[0])

dates = []
cumulative_hours = []
chart_total_hours = 0

for date, duration_hours, in records:
    chart_total_hours += duration_hours
    dates.append(date)
    cumulative_hours.append(chart_total_hours)

plt.plot(dates, cumulative_hours)
plt.xlabel("Year")
plt.ylabel("Cumulative EVA duration (hours)")
plt.tight_layout()
plt.savefig("cumulative_duration.png")
plt.show()