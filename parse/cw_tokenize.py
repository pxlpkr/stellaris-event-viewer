def safe_split(items: list[str], delim: str):
    result = []
    for item in items:
        if item == delim:
            result.append(item)
            continue

        split_item = item.split(delim)
        for fragment in split_item[:-1]:
            if fragment != '':
                result.append(fragment)
            result.append(delim)
        if split_item[-1] != '':
            result.append(split_item[-1])

    return result

def safe_set(path: list[dict], key: str, token: any):
    try:
        if token is None:
            if key not in path[-1]:
                path[-1][key] = token
            return

        if path[-1][key] is None:
            path[-1][key] = token
            return

        if not isinstance(path[-1][key], list):
            path[-1][key] = [path[-1][key]]

        path[-1][key].append(token)
    except Exception:
        print(f'Exception:\npath={[len(i) for i in path]}\n{token=}\n{key=}\n')
        raise

def cw_parse_token(path: list[dict], token: str, *args) -> list[str]:
    # print(f'token={token}; path={[len(i) for i in path]}')
    # Dealing with Comments
    if token == "\n":
        if args and args[-1] == "#":
            return [*args[:-1]]
        else:
            return [*args]

    if args and args[-1] == "#":
        return [*args]

    if token.startswith("#"):
        return [*args, "#"]

    # Empty lines
    if not token:
        return [*args]

    # Variable setting
    if len(args) == 2 and args[1] == "=":
        # New dict
        if token == "{":
            new_dict = dict()
            safe_set(path, args[0], new_dict)
            path.append(new_dict)
            return []

        # Boolean case
        elif token == "no":
            token = False

        elif token == "yes":
            token = True

        safe_set(path, args[0], token)
        return []

    if len(args) == 1 and token == "=":
        return [*args, token]

    if token == "}":
        path.pop()
        return []

    # Default case
    safe_set(path, token, None)
    return [token]

def cw_tokenize(fp: str):
    with open(fp, 'r') as f:
        raw: str = f.read()

    tokens: list[str] = raw.replace('\t', '').replace('\n', ' \n ').split(' ')
    tokens = safe_split(tokens, '=')
    tokens = safe_split(tokens, '{')
    tokens = safe_split(tokens, '}')

    root: dict = dict()
    path: list[dict] = [root]
    args: list[str] = []

    for token in tokens:
        args = cw_parse_token(path, token, *args)

    return root
