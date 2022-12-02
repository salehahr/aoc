from .parse import parse_ints


def print_part(func):
    def _wrapped(*args, **kwargs):
        print(f"\nPart {kwargs['part']}")
        return func(*args, **kwargs)

    return _wrapped
