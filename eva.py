import json
from datetime import datetime 
import matplotlib.pyplot as plt

with open("eva-data.json", "r", encoding="utf-8") as file:
    eva_data = json.load(file)

first_country = input("Enter the first country to report: ").strip()
second_country = input("Enter the second country to report: ").strip()
selected_countries = (first_country.casefold(), second_country.casefold())
records = []
country_totals = {first_country.casefold(): 0, second_country.casefold(): 0}
category_counts = {
    country: {"Short": 0, "Standard": 0, "Long": 0}
    for country in selected_countries
}

for eva in eva_data:
    country = eva.get("country", "").strip()
    country_key = country.casefold()
    if country_key not in selected_countries:
        continue

    date_text = eva.get("date")
    duration_text = eva.get("duration")

    if not duration_text:
        continue

    hours, minutes = map(int, duration_text.split(":"))
    duration_hours = hours + minutes / 60
    country_totals[country_key] += duration_hours

    if duration_hours < 4:
        category_counts[country_key]["Short"] += 1
    elif duration_hours < 7:
        category_counts[country_key]["Standard"] += 1
    else:
        category_counts[country_key]["Long"] += 1

    if not date_text:
        continue

    date = datetime.fromisoformat(date_text)
    records.append((date, duration_hours))

first_total = country_totals[first_country.casefold()]
second_total = country_totals[second_country.casefold()]
print(f"Total EVA duration for {first_country}: {first_total:.2f} hours")
print(f"Total EVA duration for {second_country}: {second_total:.2f} hours")

for country_name in (first_country, second_country):
    country_key = country_name.casefold()
    counts = category_counts[country_key]
    total_evas = sum(counts.values())
    print(f"EVA duration categories for {country_name}:")
    for category, count in counts.items():
        percentage = count / total_evas * 100 if total_evas else 0
        print(f"  {category}: {count} ({percentage:.2f}%)")

if first_total > second_total:
    print(f"{first_country} has the greater total EVA duration.")
elif second_total > first_total:
    print(f"{second_country} has the greater total EVA duration.")
else:
    print("Both countries have the same total EVA duration.")

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