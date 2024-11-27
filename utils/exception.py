"""本文件主要用来处理可能遇到的各种报错"""


class CustomError(Exception):
    """基础的自定义异常类，用于处理多种不同的错误情况。"""

    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"{self.message}"



class TypeError(Exception):
    """当期望的数据类型不匹配时抛出。"""
    def __init__(self, key, expected_type, actual_type, message=None):
        super().__init__(message)
        self.message = message
        self.key = key
        self.expected_type = expected_type
        self.actual_type = actual_type
    def __str__(self):
        return f"Incorrect type for key '{self.key}': Expected {self.expected_type}, got {self.actual_type}"


class ListLengthError(Exception):
    """当列表长度不满足预期时抛出"""
    def __init__(self, key, expected_length, actual_length, message=None):
        super().__init__(message)
        self.message = message
        self.key = key
        self.expected_length = expected_length
        self.actual_length = actual_length

    def __str__(self):
        return f"Incorrect length for key '{self.key}': Expected {self.expected_length}, got {self.actual_length}"


class ValueRangeError(Exception):
    """当数值不在预定的范围内时抛出。范围"""
    def __init__(self, key, expected_range, actual_value, message=None):
        super().__init__(message)
        self.message = message
        self.key = key
        self.expected_range = expected_range
        self.actual_value = actual_value
    def __str__(self):
        return f"Out of range value for key '{self.key}': Expected range {self.expected_range}, got {self.actual_value}"


class ValueChooseError(Exception):
    """当值不在预定的选择范围内时抛出。固定选择"""
    def __init__(self, key, expected_value, actual_value, message=None):
        super().__init__(message)
        self.message = message
        self.key = key
        self.expected_value = expected_value
        self.actual_value = actual_value

    def __str__(self):
        return f"Invalid value for key '{self.key}': Expected one of {self.expected_value}, got {self.actual_value}"

class ValueConvertError(Exception):
    """当值不在预定的选择范围内时抛出。"""
    def __init__(self, key, expected_type, actual_value, message=None):
        super().__init__(message)
        self.message = message
        self.key = key
        self.expected_type = expected_type
        self.actual_value = actual_value

    def __str__(self):
        return f"Failed to convert key '{self.key}' with value '{self.actual_value}' to {self.expected_type.__name__}"


class UnknownkeywordError(Exception):
    # 检查字典中的某个键是否存在错误
    def __init__(self,  key, message=None):
        super().__init__(message)
        self.key = key

    def __str__(self):
        return f"Unknown keyword {self.key}"

class MisskeywordError(Exception):
    # 检查字典中的某个键是否存在错误
    def __init__(self,  key, message=None):
        super().__init__(message)
        self.key = key

    def __str__(self):
        return f"missing parameter {self.key}"

class CustomFileNotFoundError(Exception):
    def __init__(self, file_path, message=None):

        super().__init__(message)
        self.file_path = file_path

    def __str__(self):
        return f"FileNotFoundError: {self.file_path}"

if __name__ == "__main__":
    def process_data(data):
        if not data:
            raise CustomError("No data provided", error_code=100)
        elif 'error' in data:
            raise DataError("Error in data", error_code=200)
        else:
            print("Processing data...")
            # 处理数据的逻辑


    process_data("error  dsaffadsfasdf asdfg ")
