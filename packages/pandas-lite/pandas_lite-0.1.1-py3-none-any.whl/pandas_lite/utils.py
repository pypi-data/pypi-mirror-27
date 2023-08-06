from typing import List


def check_duplicate_list(lst: List) -> None:
    for i, elem in enumerate(lst):
        if elem in lst[i + 1:]:
            raise ValueError(f'Column {elem} is selected more than once')
