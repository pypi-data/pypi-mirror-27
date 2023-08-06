def Custom(parts, merger):
    result = []
    for index, part in enumerate(parts):
        result.append(merger(part, index))
    return result
