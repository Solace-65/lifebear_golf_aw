# -*- coding: utf-8 -*-
"""Copy of LifeBearAW.

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1fe2Vgu9SXLiX4-y07944kwfEra2qdwPw
"""

import pandas as pd
import re
import os

# Define the input file path
input_file_path = "/content/3.6M-Japan-lifebear.com-Largest-Notebook-App-UsersDB-csv-2019.csv"

# Define the output directories
in_folder = "in"
csv_file_path = os.path.join(in_folder, "input.csv")
before_cleaning_folder = "before_cleaning"
cleaned_chunks_folder = "cleaned_chunks"
garbage_folder = "garbage"

# Create the output directories if they don't exist
for folder in [in_folder, before_cleaning_folder, cleaned_chunks_folder, garbage_folder]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Define the chunk size (adjust according to your system's memory)
chunk_size = 10000

# Define the essential columns
essential_columns = ["login_id", "mail_address", "password"]

# Define the columns of interest
columns_of_interest = ["login_id", "mail_address", "password", "birthday_on", "gender"]

# Initialize DataFrames to hold merged cleaned and garbage data
merged_cleaned_data = pd.DataFrame(columns=columns_of_interest)
merged_garbage_data = pd.DataFrame(columns=columns_of_interest)

# Read the CSV file in chunks
for chunk in pd.read_csv(input_file_path, chunksize=chunk_size, sep=';', low_memory=True, on_bad_lines='skip'):
    # Filter the chunk to only include the columns of interest
    chunk_filtered = chunk[columns_of_interest]

    # Capture rows with missing essential data
    missing_essential_data = chunk_filtered[chunk_filtered[essential_columns].isnull().any(axis=1)]

    # Remove rows with missing essential data
    chunk_filtered = chunk_filtered.dropna(subset=essential_columns)

    # Remove invalid records (NaN) from birthday_on and gender columns
    invalid_records = chunk_filtered[chunk_filtered[["birthday_on", "gender"]].isnull().any(axis=1)]
    chunk_filtered = chunk_filtered.dropna(subset=["birthday_on", "gender"])

    # Remove duplicated data from the columns of interest
    duplicated_data = chunk_filtered[chunk_filtered.duplicated(subset=columns_of_interest, keep=False)]
    chunk_filtered = chunk_filtered.drop_duplicates(subset=columns_of_interest)

    # Combine removed data into a garbage DataFrame
    garbage_data = pd.concat([missing_essential_data, invalid_records, duplicated_data], ignore_index=True)

    # Append the cleaned and garbage DataFrames to the merged DataFrames
    merged_cleaned_data = pd.concat([merged_cleaned_data, chunk_filtered], ignore_index=True)
    merged_garbage_data = pd.concat([merged_garbage_data, garbage_data], ignore_index=True)

# Print the merged cleaned and garbage data
print("Merged Cleaned Data:")
print(merged_cleaned_data.head(15))  # Print the first few rows of the merged cleaned data
print("\nMerged Garbage Data:")
print(merged_garbage_data.head(15))  # Print the first few rows of the merged garbage data

# Save the merged cleaned and garbage data to new CSV files
output_file_path = os.path.join(cleaned_chunks_folder, "merged_cleaned_data.csv")
merged_cleaned_data.to_csv(output_file_path, encoding='utf-8', index=False)

output_file_path = os.path.join(garbage_folder, "merged_garbage_data.csv")
merged_garbage_data.to_csv(output_file_path, encoding='utf-8', index=False)