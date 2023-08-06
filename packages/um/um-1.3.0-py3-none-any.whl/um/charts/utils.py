"""
Utility functions for chatrs package
"""

def merge_dicts(dict_primary, *to_merge):
    """
    Merge multiple *to_merge dictionaries to dict_primary
    Leaves originals unchanged

    :param dict_primary:
    :param to_merge:
    :return: copy of merged dictionary (originals unchanged)
    """

    copy = dict_primary.copy()
    for dictionary in to_merge:
        copy.update(dictionary)
    return copy
