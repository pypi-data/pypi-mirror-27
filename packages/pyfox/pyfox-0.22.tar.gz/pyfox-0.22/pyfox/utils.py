def traverse_nested_dict(d):
    iters = [d.iteritems()]

    while iters:
        it = iters.pop()
        try:
            k, v = it.next()
        except StopIteration:
            continue

        iters.append(it)

        if isinstance(v, dict):
            iters.append(v.iteritems())
        yield k, v


def transform_to_json(dot_notation_dict):
    keys_dict = {}
    delim = '.'
    for key, val in dot_notation_dict.items():
        if delim in key:
            splits = key.split(delim)
            if splits[0] not in keys_dict:
                keys_dict[splits[0]] = {}
            keys_dict[splits[0]]['.'.join(splits[1:])] = val
        else:
            keys_dict[key] = val
    for key, val in keys_dict.items():
        if isinstance(val, dict):
            keys_dict[key] = transform_to_json(val)
    return keys_dict
