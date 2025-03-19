import pandas as pd
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename='data_validation.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_message(message, level="info"):
    """Logs a message with a timestamp."""
    if level == "info":
        logging.info(message)
    elif level == "warning":
        logging.warning(message)
    elif level == "error":
        logging.error(message)

def write_findings_to_file(message):
    """Writes validation findings to a file."""
    with open('validation_log.txt', 'a') as file:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        file.write(f"{timestamp} - {message}\n")

def validate_column_names(df, expected_columns):
    """Validates if the DataFrame contains the expected columns."""
    missing_columns = [col for col in expected_columns if col not in df.columns]
    if missing_columns:
        message = f"Missing columns: {missing_columns}"
        log_message(message, level="error")
        write_findings_to_file(message)
        return False
    message = "All expected columns are present."
    log_message(message)
    write_findings_to_file(message)
    return True

def validate_no_missing_values(df):
    """Validates if the DataFrame has any missing values."""
    if df.isnull().values.any():
        message = "Data contains missing values."
        log_message(message, level="error")
        write_findings_to_file(message)
        return False
    message = "No missing values found in the data."
    log_message(message)
    write_findings_to_file(message)
    return True

def validate_data_types(df, expected_types):
    """Validates the data types of the DataFrame columns."""
    for column, expected_type in expected_types.items():
        if column in df.columns:
            if not pd.api.types.is_dtype_equal(df[column].dtype, expected_type):
                message = f"Column '{column}' has incorrect type. Expected: {expected_type}, Found: {df[column].dtype}"
                log_message(message, level="error")
                write_findings_to_file(message)
                return False
    message = "All columns have correct data types."
    log_message(message)
    write_findings_to_file(message)
    return True

def main():
    # Load the data
    try:
        df = pd.read_csv('data.csv')
        message = "Data loaded successfully."
        log_message(message)
        write_findings_to_file(message)
    except Exception as e:
        message = f"Error loading data: {e}"
        log_message(message, level="error")
        write_findings_to_file(message)
        return

    # Define validation rules
    expected_columns = ['Name', 'Age', 'Email']
    expected_types = {'Name': 'object', 'Age': 'int64', 'Email': 'object'}

    # Perform validations
    if not validate_column_names(df, expected_columns):
        return
    if not validate_no_missing_values(df):
        return
    if not validate_data_types(df, expected_types):
        return

    message = "Data validation completed successfully."
    log_message(message)
    write_findings_to_file(message)

if __name__ == "__main__":
    main()