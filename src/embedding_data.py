import json
import logging

def load_json_from_file(file_path):
    """
    Load data from JSON file 
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:  # Thêm mã hóa='utf-8'
            data = json.load(f)
            return data
    except FileNotFoundError:
        logging.error(f"File not found at '{file_path}'")
        return None
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON format in file '{file_path}'")
        return None
    except UnicodeDecodeError as e: # Thêm ngoại lệ cụ thể hơn
        logging.error(f"UnicodeDecodeError occurred: {e} in file '{file_path}'")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return None