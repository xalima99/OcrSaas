import re

def is_uppercase(string: str) -> bool:
    return string == string.upper()

def is_date(string: str) -> bool:
    string_formatted = string.replace(" ", "")
    pattern1 = re.compile(r"^[0-9]{2}(\.|\.)[0-9]{2}(\.|\.)[0-9]{4}")
    pattern2 = re.compile(r"^[0-9]{2}(\.|\.)[0-9]{6}") 
    match1 = bool(pattern1.findall(string_formatted))
    match2 = bool(pattern2.findall(string_formatted))
    if match1 or match2:
        return True
    return False
    
def extract_place(string: str) -> str:
    splitted_str = string.split(" ")
    del splitted_str[0]
    clean_place = " ".join(splitted_str)
    return clean_place

def extract_genre(string: str) -> str:
    genre = ""
    arr = string.split(" ")
    if len(arr) > 1:
        if is_uppercase(arr[1]):
            genre = arr[1]
            return genre

def extract_parents_name(string: str) -> str:
    splitted_str = string.split(" ")
    del splitted_str[0]
    del splitted_str[0]
    clean_name = " ".join(splitted_str)
    return clean_name
        
def is_alpha_numeric(string: str) -> bool:
    return string.isalnum()

def has_alpha(string: str) -> bool:
    return bool(re.search('[a-zA-Z]', string))

def has_numeric(string: str) -> bool:
    return bool(re.search('[0-9]', string))

def is_id(string: str) -> bool:
    check_alphanum = is_alpha_numeric(string)
    check_hasNum = has_numeric(string)
    check_hasAlpha = has_alpha(string)   
    if len(string) > 6 and len(string) < 9 and check_alphanum and check_hasAlpha and check_hasNum:
        return True
    return False
    
