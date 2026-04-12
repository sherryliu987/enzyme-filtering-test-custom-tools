#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8

import os
import pandas as pd

print("New verion!!")
print("version2")

# Load Excel file containing Enzyme Miner results into a DataFrame
file_path = "inputs/inputExcelFile.xlsx"
full_data = pd.read_excel(file_path, sheet_name=1)
full_data.info()

# Display the first ten rows
full_data.head(10)

# Function to filter the 'First seen' column by date - default value is the pre-Nagoya period
def filter_first_seen(df, cutoff_date='2014-10-01'):
    df['First seen'] = pd.to_datetime(df['First seen'], errors='coerce')
    return df[df['First seen'] < pd.to_datetime(cutoff_date)]

# Function to show available Kingdom values
def show_kingdom_options(df):
    print("Available Kingdom values with counts:")
    print(df['Kingdom'].value_counts(dropna=False))

# Function to filter the 'Kingdom' column by kingdom(s)
def filter_by_kingdom(df, kingdom_values):
    return df[df['Kingdom'].isin(kingdom_values)]

# Function to filter the 'Transmembrane' column to include only rows with value "o" = exclude any transmembrane proteins
def filter_transmembrane(df):
    return df[df['Transmembrane'] == 'o']

# Function to filter 'Solubility' column to values >= user-defined threshold - default value is >=0.4
def filter_solubility(df, threshold=0.4):
    return df[df['Solubility'] >= threshold]

# Function to retain only enzymes without 'Extra domains' - i.e. that row is empty
def filter_empty_extra_domains(df):
    return df[df['Extra domains'].isna() | (df['Extra domains'].astype(str).str.strip() == '')]

# Function to remove non-empty rows from 'Swiss-Prot' - i.e. remove characterized proteins that are not novel and IP-free (likely)
def remove_non_empty_swiss_prot(df):
    return df[df['Swiss-Prot'].isna() | (df['Swiss-Prot'].astype(str).str.strip() == '')]

# Function to show available salinity values
def show_salinity_options(df):
    print("Available Salinity values with counts:")
    print(df['Salinity'].value_counts(dropna=False))

# Function to filter by salinity
def filter_by_salinity(df, salinity_value):
    return df[df['Salinity'] == salinity_value]

# Function to show available temperature range values
def show_temprange_options(df):
    print("Available Temperature Range values with counts:")
    print(df['Temp. range'].value_counts(dropna=False))

# Function to filter by temperature range
def filter_by_temprange(df, temprange_value):
    return df[df['Temp. range'] == temprange_value]

# Drop columns that are not needed - apply in all cases
full_data.drop(columns=[
    'Annotation', 'Source databases', 'Biotic relationship', 'Disease', 'Closest known', 'Identity closest known', 'ER template', 'Essential residues', 'GI'
], inplace=True)
print(f"After dropping columns: {len(full_data)} rows")
full_data.head(10)

# Filter by date - default is pre-Nagoya. The date can be changed if needed.
cutoff_date = os.getenv('cutoff_date', '2014-10-01')
full_data = filter_first_seen(full_data, cutoff_date=cutoff_date)
print(f"After date filter: {len(full_data)} rows")
full_data.head()

# Show Kingdom options 
show_kingdom_options(full_data)

# Filter by Kingdom if needed- default is Archaea (A) and Bacteria (B).
kingdom_values_raw = os.getenv('kingdom_values', 'A,B')
kingdom_values = [k.strip() for k in kingdom_values_raw.split(',')]  # Strip whitespace from each value
print(f"Filtering by Kingdom values: {kingdom_values}")
full_data = filter_by_kingdom(full_data, kingdom_values)
print(f"After Kingdom filter: {len(full_data)} rows")
full_data.head()

# Filter out transmembrane proteins
full_data = filter_transmembrane(full_data)
print(f"After transmembrane filter: {len(full_data)} rows")
full_data.head()

# Filter by solubility threshold - the default is equal to and above 0.4
solubility_threshold = float(os.getenv('solubility_threshold', 0.4))
full_data = filter_solubility(full_data, threshold=solubility_threshold)
print(f"After solubility filter: {len(full_data)} rows")
full_data.head()

# Retain only enzymes without 'Extra domains'
full_data = filter_empty_extra_domains(full_data)
print(f"After extra domains filter: {len(full_data)} rows")
# Remove enzymes with a 'Swiss-Prot' ID
full_data = remove_non_empty_swiss_prot(full_data)
print(f"After Swiss-Prot filter: {len(full_data)} rows")

full_data.head()

# Show salinity options
show_salinity_options(full_data)

# Filter by salinity (optional - only if provided)
salinity_value = os.getenv('salinity_value')
if salinity_value:
    print(f"Filtering by salinity: {salinity_value}")
    full_data = filter_by_salinity(full_data, salinity_value)
    full_data.head()
else:
    print("Skipping salinity filter (not provided)")

# Show temperature range options
show_temprange_options(full_data)

# Filter by temperature range (optional - only if provided)
temprange_value = os.getenv('temprange_value')
if temprange_value:
    print(f"Filtering by temperature range: {temprange_value}")
    full_data = filter_by_temprange(full_data, temprange_value)
else:
    print("Skipping temperature range filter (not provided)")

# Display final Data Frame dimensions, and the first and last 10 rows
full_data = full_data.reset_index(drop=True)
print("Final DataFrame shape:", full_data.shape)

# Save the processed data to a new CSV
full_data.to_csv("out/filtered_data.csv", index=False)

full_data.head(10)
full_data.tail(10)