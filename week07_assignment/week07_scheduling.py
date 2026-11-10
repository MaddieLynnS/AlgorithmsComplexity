def interval_schedule(intervals: list[tuple[int, int]]) -> list[int]:
    """Return original position indices of a maximum-cardinality compatible schedule."""
    if intervals == []:
        return []

    # sort list and return it in increasing order of second digit in tuple,
    # then by the first digit if there are ties in the second digit
    # leaves original data list intact as requested
    ordered_list = sorted(intervals, key=lambda number:(number[1], number[0]))

    # iterate through the ordered list and select only compatible intervals
    right_list_indexes = []
    end_time = 0
    for i in ordered_list:
        previous_end_time = end_time
        if previous_end_time > i[0]:
            continue
        end_time = i[1]
        right_list_indexes.append(intervals.index(i))

    # return a new list of indices indicating best schedule based off ORIGINAL list
    return right_list_indexes