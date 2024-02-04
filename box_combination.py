from typing import List, Tuple


def _calculate_box_area(coordinates: List[int]) -> int:
    if len(coordinates) != 4:
        raise ValueError("Invalid coordinates")
    return abs(coordinates[1] - coordinates[0]) * abs(coordinates[3] - coordinates[2])


def _calculate_boxes_area(boxes: List[Tuple[str, int]]) -> int:
    return sum([box[1] for box in boxes])


def box_combination(
        boxes: List[Tuple[str, List[int]]],
        lower_limit: int,
        upper_limit: int,
) -> List[List[Tuple[str, int]]]:
    """
    :param boxes: list of boxes and box sizes
    :param lower_limit: greater than or equal to lower_limit
    :param upper_limit: strictly less than upper_limit
    :return:
    """
    result = []
    buffer = []
    prepared_boxes = []

    for box, dimensions in boxes:
        box_area = _calculate_box_area(dimensions)
        prepared_boxes.append((box, box_area))

    def _backtrack(sub_boxes: List[Tuple[str, int]]) -> List[List[Tuple[str, int]]]:
        boxes_area = _calculate_boxes_area(buffer)
        if lower_limit <= boxes_area < upper_limit:
            result.append(buffer[:])

        if boxes_area >= upper_limit:
            return

        for i in range(len(sub_boxes)):
            buffer.append(sub_boxes[i])
            _backtrack(sub_boxes[i + 1:])
            buffer.pop()

    _backtrack(prepared_boxes)
    return result
