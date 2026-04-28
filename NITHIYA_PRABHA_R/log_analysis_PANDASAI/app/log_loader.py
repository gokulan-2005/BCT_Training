import pandas as pd

def load_logs(file_path):
    try:
        df = pd.read_csv(file_path)

        # Convert timestamp
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])

        return df

    except Exception as e:
        print("Error loading logs:", str(e))
        return None