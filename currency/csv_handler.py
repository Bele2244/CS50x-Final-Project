import csv

# Load csv file and return it as a list
def load_csv(file):
    with open(file) as f_csv:
        reader_csv = csv.DictReader(f_csv)
        countries_csv = list(reader_csv)
    return countries_csv