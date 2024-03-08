import pandas as pd
from datetime import timedelta

def process_employee_data(input_file_path, output_file_path):
    """
    Reads employee data from a CSV, transforms it into a historical format, and saves the output.

    Args:
        input_file_path (str): Path to the input CSV file.
        output_file_path (str): Path to save the transformed output CSV file.
    """

    # Read the data from the CSV file
    df = pd.read_csv(input_file_path)

    # Sort the DataFrame by employee code and date
    df['Date of Joining'] = pd.to_datetime(df['Date of Joining'])
    df['Date of Exit'] = pd.to_datetime(df['Date of Exit'])
    df.sort_values(['Employee Code', 'Date of Joining'], inplace=True)

    # Function to derive end dates
    def derive_end_dates(group):
        # Handle potential missing 'Date of Joining' values
        group['End Date'] = group['Date of Joining'].fillna(method='ffill') - timedelta(days=1)

        # Assign '2100-01-01' for the latest record, excluding the grouping column
        group.iloc[-1, -1] = pd.to_datetime('2100-01-01')
        return group

    # Apply the function to calculate end dates within each employee group
    df = df.groupby('Employee Code', as_index=False, group_keys=False).apply(derive_end_dates)

    # Create a list to store rows for the transformed data
    rows_to_append = []

    # Function to process each employee's data
    def process_employee(row):
        # Append the first record with 'End Date' as 'Date of Exit' or default
        rows_to_append.append({
            'Employee Code': row['Employee Code'],
            'Manager Employee Code': row['Manager Employee Code'],
            'Last Compensation': '',
            'Compensation': row['Compensation'],
            'Last Pay Raise Date': '',
            'Variable Pay': 0,
            'Tenure in Org': 0,
            'Performance Rating': '',
            'Engagement Score': 0,
            'Effective Date': row['Date of Joining'],
            'End Date': row['Date of Exit'] if not pd.isnull(row['Date of Exit']) else pd.to_datetime('2100-01-01')
        })

        # Append subsequent records, handling potential missing values or inconsistencies
        if not pd.isnull(row['Compensation 1 date']):
            rows_to_append.append({
                'Employee Code': row['Employee Code'],
                'Manager Employee Code': row['Manager Employee Code'],
                'Last Compensation': row['Compensation'],
                'Compensation': row['Compensation 1'],
                'Last Pay Raise Date': row['Compensation 1 date'],
                'Variable Pay': 0,
                'Tenure in Org': 0,
                'Performance Rating': row['Review 1'],
                'Engagement Score': row['Engagement 1'],
                'Effective Date': row['Compensation 1 date'],
                'End Date': pd.to_datetime(row['Compensation 2 date']) - timedelta(days=1) if not pd.isnull(row['Compensation 2 date']) else pd.to_datetime('2100-01-01')
            })

        if not pd.isnull(row['Compensation 2 date']):
            rows_to_append.append({
                'Employee Code': row['Employee Code'],
                'Manager Employee Code': row['Manager Employee Code'],
                'Last Compensation': row['Compensation 1'],
                'Compensation': row['Compensation 2'],
                'Last Pay Raise Date': row['Compensation 2 date'],
                'Variable Pay': 0,
                'Tenure in Org': 0,
                'Performance Rating': row['Review 2'],
                'Engagement Score': row['Engagement 2'],
                'Effective Date': row['Compensation 2 date'],
                'End Date': pd.to_datetime('2100-01-01')
            })

    # Apply the process_employee function to each row
    df.apply(process_employee, axis=1)

    # Create the output DataFrame from the list of rows
    output_df = pd.DataFrame(rows_to_append, columns=[
        'Employee Code', 'Manager Employee Code', 'Last Compensation', 'Compensation', 'Last Pay Raise Date',
        'Variable Pay', 'Tenure in Org', 'Performance Rating', 'Engagement Score', 'Effective Date', 'End Date'
    ])

    # Save the output DataFrame to a CSV file
    output_df.to_csv(output_file_path, index=False)

# Example usage
process_employee_data("C:/Users/Usurk/Downloads/input.csv", "C:/Users/Usurk/Downloads/output.csv")
