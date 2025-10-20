import pandas as pd

# Define the input and output file names
input_file = 'loads.csv'
output_file = 'loads_cleaned_sorted.csv'

# Define the columns we need to work with
sort_column_name = 'Average Latency (cycles)'
extra_col_to_remove = 'Source File'

try:
    # 1. Read the tab-separated file
    df = pd.read_csv(input_file, sep='\t')
    print(f"Successfully read '{input_file}'.")

    # 2. Find all "Efficient-core (E-core)" columns
    ecore_cols = [col for col in df.columns if 'Efficient-core (E-core)' in col]
    
    # 3. Create the full list of columns to remove
    all_cols_to_remove = ecore_cols
    
    # Check if 'Source File' column exists before adding it
    if extra_col_to_remove in df.columns:
        all_cols_to_remove.append(extra_col_to_remove)
    else:
        print(f"Warning: Column '{extra_col_to_remove}' not found, skipping its removal.")

    if not all_cols_to_remove:
        print("No columns to remove.")
    else:
        print(f"Removing the following {len(all_cols_to_remove)} columns:")
        for col in all_cols_to_remove:
            print(f"  - {col}")

    # 4. Drop all identified columns
    df_cleaned = df.drop(columns=all_cols_to_remove)

    # 5. Sort the rows w.r.t. average latency
    # Check if the sort column exists
    if sort_column_name in df_cleaned.columns:
        # First, convert the column to a numeric type to ensure correct sorting
        df_cleaned[sort_column_name] = pd.to_numeric(df_cleaned[sort_column_name])
        
        # Now, sort the DataFrame in descending order
        df_sorted = df_cleaned.sort_values(by=sort_column_name, ascending=False)
        print(f"\nSorting rows by '{sort_column_name}' (descending).")
    else:
        print(f"Warning: Sort column '{sort_column_name}' not found. Skipping sort.")
        df_sorted = df_cleaned # Continue without sorting

    # 6. Save the final DataFrame to a new tab-separated file
    df_sorted.to_csv(output_file, sep='\t', index=False)

    print(f"\n✅ Successfully created '{output_file}'.")

except pd.errors.EmptyDataError:
    print(f"Error: The file '{input_file}' is empty.")
except FileNotFoundError:
    print(f"Error: The file '{input_file}' was not found in the same directory.")
except KeyError:
    print(f"Error: A required column was not found. Please check file contents.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
