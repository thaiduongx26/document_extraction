def split(arr: list, deliminator):
    chunks = []
    indices = []
    chunk = []

    for i, e in enumerate(arr):
        if deliminator(e):
            if len(chunk) > 0:
                chunks.append(chunk)
                indices.append(i)
            chunk = []
        else:
            chunk.append(e)
    else:
        if len(chunk) > 0:
            chunks.append(chunk)
            indices.append(i)

    return chunks, indices
