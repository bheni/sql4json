from tokenizer import Tokenizer

PATH_SEPERATORS = frozenset(('/','.','\\'))

def get_elements_by_path(data, path):
    tokenizer = Tokenizer(path)

    return get_elements_by_path_tokens(data, list(tokenizer))

def get_elements_by_path_tokens(data, path_tokens):
    token_should_be_seperator = (path_tokens[0] in PATH_SEPERATORS) if len(path_tokens) > 0 else False
    
    elements = []

    if isinstance(data, list) or isinstance(data, tuple):
        root_items = data
    else:
        root_items = [data]

    for current in root_items:
        for i,token in enumerate(path_tokens):
            if token_should_be_seperator:
                if not token in PATH_SEPERATORS:
                    raise Exception("Invalid tokens used as dictionary path")

            else:
                if current != None and token in current:
                    current = current[token]

                    if (isinstance(current, list) or isinstance(current, tuple)):
                        for item in current:
                            found, subelements = get_elements_by_path_tokens(item, path_tokens[i+1:])
                            elements.extend(subelements)

                else:
                    current = None
                    break

            if i == len(path_tokens) - 1:
                elements.append(current)

            token_should_be_seperator = not token_should_be_seperator

    array_of_arrays = True
    for element in elements:
        if not (isinstance(current, list) or isinstance(current, tuple)):
            array_of_arrays = False
            break

    if array_of_arrays:
        flattened_array = []
        for element in elements:
            flattened_array.extend(element)

        elements = flattened_array

    return len(elements) > 0, elements

def split_on_any(string_to_split, delims, ignore_whitespace_strings=True, ignore_empty_trings=True):
    strings = []
    word_chars = []

    for char in string_to_split:
        if char in delims:
            string = ''.join(word_chars)
            word_chars = []

            if (not ignore_empty_trings) or ((not ignore_whitespace_strings) and len(string) > 0) or any([not current.isspace() for current in string]):
                strings.append( string )

        else:
            word_chars.append(char)

    string = ''.join(word_chars)

    if ((not ignore_whitespace_strings) and len(string) > 0) or any([(not current.isspace()) for current in string]):
        strings.append( string )

    return strings