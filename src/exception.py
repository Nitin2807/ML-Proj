import sys

def error_msg_details(error, error_detail):
    _, _, exc_tb = error_detail.exc_info()
    
    # Safety check in case traceback is missing
    file_name = "Unknown"
    line_number = 0
    
    if exc_tb is not None:
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno

    error_message = f"Error occurred in script: [{file_name}] line: [{line_number}] message: [{str(error)}]"
    return error_message

class CustomException(Exception):
    def __init__(self, error_message, error_detail):
        # Pass the original message to the base Exception class
        super().__init__(error_message)
        # Store the detailed, formatted message
        self.error_message = error_msg_details(error_message, error_detail=error_detail)

    def __str__(self):
        return self.error_message