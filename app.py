import pandas as pd
from datetime import datetime

def log_message(message):
    """Writes validation findings to a file."""
    with open('validation_log.txt', 'a') as file:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        file.write(f"{timestamp} - {message}\n")

def validate_column_names(df, expected_columns):
    """Validates if the DataFrame contains the expected columns."""
    missing_columns = [col for col in expected_columns if col not in df.columns]
    if missing_columns:
        log_message(f"Missing columns: {missing_columns}")
        return False
    log_message("All expected columns are present.")
    return True

def validate_no_missing_values(df):
    """Validates if the DataFrame has any missing values."""
    if df.isnull().values.any():
        log_message("Data contains missing values.")
        return False
    log_message("No missing values found in the data.")
    return True

def main():
    # Load the data into the DataFrame
    try:
        df = pd.read_csv('data.csv')
        log_message("Data loaded successfully.")
    except Exception as e:
        log_message(f"Error loading data: {e}")
        return

    # Define validation rules
    expected_columns = ['Name', 'Age', 'Email']

    # Perform validations
    if not validate_column_names(df, expected_columns):
        return
    if not validate_no_missing_values(df):
        return

    log_message("Data validation completed successfully.")

if __name__ == "__main__":
    main()