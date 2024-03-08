Employee Data Transformation

This Python script reads employee data from a CSV file, transforms it into a historical format, and saves the output as a new CSV file.

Table of Contents

Overview

Methodology

Assumptions

Usage

Example

Overview

The script takes employee data in a specific CSV format as input. It sorts the data by employee code and date of joining and calculates end dates for each employee's record. It then processes each employee's data, including compensation changes, and creates a historical record for each change. Finally, it saves the transformed data to a new CSV file.

Methodology

Reading Data: The script reads the input CSV file into a pandas DataFrame.

Sorting: It sorts the DataFrame by 'Employee Code' and 'Date of Joining'.

Deriving End Dates: End dates for each employee's record are calculated based on the joining dates. If the 'Date of Exit' is available, it's used as the end date. Otherwise, it's set to '2100-01-01'.

Processing Employee Data: The script processes each employee's data row by row. It appends records for each compensation change, handling missing values or inconsistencies appropriately.

Output Creation: The transformed data is stored in a DataFrame and then saved to a new CSV file.

Assumptions

The input CSV file contains columns such as 'Employee Code', 'Date of Joining', 'Date of Exit', 'Compensation', 'Compensation 1', 'Compensation 2', etc., in the expected format.

Missing values in certain columns are handled by the script.

The end date for each employee's record is calculated based on the next employee's joining date or set to '2100-01-01' if the employee is the last one in the group.

Usage

To use the script, call the process_employee_data function with the input CSV file path and the desired output CSV file path.

process_employee_data("input.csv", "output.csv")

Example

process_employee_data("input.csv", "output.csv")

This will read employee data from "input.csv", transform it, and save the transformed data to "output.csv".
