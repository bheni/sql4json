from tokenizer import Tokenizer

PATH_SEPERATORS = frozenset(('/','.','\\'))

def get_element_by_path(data, path):
    tokenizer = Tokenizer(path)

    return get_element_by_path_tokens(data, list(tokenizer))

def get_element_by_path_tokens(data, path_tokens):
    token_should_be_seperator = (path_tokens[0] in PATH_SEPERATORS) if len(path_tokens) > 0 else False

    current = data
    found = True

    for token in path_tokens:
        if token_should_be_seperator:
            if not token in PATH_SEPERATORS:
                raise Exception("Invalid tokens used as dictionary path")

        else:
            if current != None and token in current:
                current = current[token]
            else:
                current = None
                found = False
                break

        token_should_be_seperator = not token_should_be_seperator

    return found, current

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