def find_first_index_of(iterable, cond, default=None):
    try:
        return next(i for i, x in enumerate(iterable) if cond(x))
    except StopIteration:
        return default
