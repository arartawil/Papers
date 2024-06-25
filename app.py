import streamlit as st
import pandas as pd
import os
from glob import glob

# Define the directory containing the CSV files
file_directory = 'Result/'  # replace with the directory where your CSV files are located


# Function to get the file map dynamically from the directory
def get_file_map(directory):
    all_files = glob(os.path.join(directory, "*.csv"))
    file_map = {os.path.splitext(os.path.basename(file))[0]: file for file in all_files}
    return file_map


# Streamlit app
st.title('Scopus Data')

# Refresh the file map each time the app runs
file_map = get_file_map(file_directory)

# User input for file ID
file_id = st.text_input('Enter the file Scopus ID:', '')

# Define the columns to display
columns_to_display = [
    'ï»¿Cites', 'Authors', 'Title', 'Year', 'Source',
    'Type', 'DOI'
]

if file_id:
    # Get the corresponding file path
    file_path = file_map.get(file_id)

    if file_path:
        try:
            # Read the CSV file
            df = pd.read_csv(file_path, encoding='latin1')

            # Display only the specified columns
            df_to_display = df[columns_to_display]

            # Display the data
            st.write(f'Data from file ID {file_id}:')
            st.dataframe(df_to_display)

            # Filter data for the years 2022, 2023, and 2024
            df_filtered = df[df['Year'].isin([2022, 2023, 2024])]

            # Aggregate citations
            citation_data = pd.DataFrame(columns=['Year', 'ï»¿Cites'])
            citations = df_filtered.groupby('Year')['ï»¿Cites'].sum().reset_index()
            citation_data = pd.concat([citation_data, citations])

            # Count number of documents
            document_data = pd.DataFrame(columns=['Year', 'Title'])
            documents = df_filtered.groupby('Year').size().reset_index(name='Title')
            document_data = pd.concat([document_data, documents])

            # Aggregate across all files
            total_citations = citation_data.groupby('Year')['ï»¿Cites'].sum().reset_index()
            total_documents = document_data.groupby('Year')['Title'].sum().reset_index()

            # Display aggregated data
            st.write('Total Citations for 2022, 2023, and 2024:')
            st.bar_chart(total_citations.set_index('Year'))

            st.write('Total Documents for 2022, 2023, and 2024:')
            st.bar_chart(total_documents.set_index('Year'))

        except Exception as e:
            st.error(f'Error reading file {file_path}: {e}')
    else:
        st.error('Invalid file ID. Please enter a valid file ID.')
