"""本文件主要用来处理可能遇到的各种报错"""
class CustomError(Exception):
    """基础的自定义异常类，用于处理多种不同的错误情况。"""

    def __init__(self, message, error_code=None, **kwargs):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.extra_data = kwargs

    def __str__(self):
        return f"{self.message} {self.extra_data}"

class ValidateDictError(Exception):
    def __init__(self, message, key, expected, type_="parameter_type"):
        super().__init__(message)
        self.key = key
        self.expected = expected
        self.type_ = type_
    def __str__(self):
        if self.type_ == "parameter_type":
            return f"value type error - Key: {self.key}, Expected type: {self.expected}"
        elif self.type_ == "list_length":
            return f"list length error - Key: {self.key}, Expected length: {self.expected}"

class ValidationError(Exception):
    """基本异常类，用于其他数据验证异常的基类。"""
    def __init__(self, message, key):
        super().__init__(message)
        self.key = key

class TypeError(ValidationError):
    """当期望的数据类型不匹配时抛出。"""
    def __init__(self, key, expected_type, actual_type):
        super().__init__(f"Incorrect type for key '{key}': Expected {expected_type}, got {actual_type}", key)
        self.expected_type = expected_type
        self.actual_type = actual_type




class ListLengthError(ValidationError):
    """当列表长度不符合预期时抛出。"""
    def __init__(self, key, expected_length, actual_length):
        super().__init__(f"Incorrect length for key '{key}': Expected {expected_length}, got {actual_length}", key)
        self.expected_length = expected_length
        self.actual_length = actual_length


class RangeError(ValidationError):
    """当数值不在预定的范围内时抛出。"""
    def __init__(self, key, expected_range, actual_value):
        super().__init__(f"Out of range value for key '{key}': Expected range {expected_range}, got {actual_value}", key)
        self.expected_range = expected_range
        self.actual_value = actual_value

class ValueError(ValidationError):
    """当值不在预定的选择范围内时抛出。"""
    def __init__(self, key, expected_value, actual_value):
        super().__init__(f"Invalid value for key '{key}': Expected one of {expected_value}, got {key}")
        self.expected_value = expected_value

class ValueInLstCheckError(Exception):
    #检查列表中的某些值错误
    def __init__(self, message, value, index):
        super().__init__(message)
        self.value = value
        self.index = index
        self.message = message

    def __str__(self):
        return f"{self.message} -- Error at index {self.index}: {self.value}"


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
