import pytest

from advent_of_code.aoc_2024 import parse_location_ids


class TestReadDataAndGetColumnsAsList():
    @pytest.mark.parametrize("filename,exp_length", [
        ("single_pair.txt", 1),
        ("multi_pair.txt", 2),
        ("values_int_str.txt", 1),
    ])
    def test_input_ok(self, filename, exp_length, datadir):
        left, right = parse_location_ids.read_data_and_get_columns_as_list(f"{datadir}/{filename}")
        assert len(left) == exp_length
        assert len(right) == exp_length

    @pytest.mark.parametrize("filename,exp_col_index", [
        ("missing_value_left.txt", 0),
        ("missing_value_right.txt", 1),
    ])
    def test_input_error(self, filename, exp_col_index, datadir):
        with pytest.raises(ValueError) as value_error:
            parse_location_ids.read_data_and_get_columns_as_list(f"{datadir}/{filename}")
        assert f"Integer column has NA values in column {exp_col_index}" == str(value_error.value)


class TestGetDistanceTwoLists():
    @pytest.mark.parametrize("left,right,exp_sum_distance", [
        # Test single value, no distance
        ([1], [1], 0),
        # Test single value, positive distance
        ([1], [2], 1),
        # Test single value, negative distance
        ([1], [-1], 2),
        # Test multi value, no distance, sort irrelevant.
        ([1, 1], [1, 1], 0),
        # Test multi value, positive distance, sort irrelevant.
        ([1, 1], [2, 2], 2),
        # Test multi value, negative distance, sort irrelevant.
        ([1, 1], [-1, -1], 4),
        # Test multi value, no distance, sort relevant.
        ([1, 2], [2, 1], 0),
        # Test multi value, positive distance, sort relevant.
        ([1, 2], [3, 2], 2),
        # Test multi value, negative distance, sort relevant.
        ([2, 1], [-2, -1], 6)
    ])
    def test_get_distance_two_lists(self, left, right, exp_sum_distance):
        result = parse_location_ids.get_distance_two_lists(lst_left=left, lst_right=right)
        assert result == exp_sum_distance

    @pytest.mark.parametrize("left,right", [
        # Test unequal list lengths
        ([1, 1], [2]),
        ([1], [2, 1])
    ])
    def test_error_input(self, left, right):
        with pytest.raises(ValueError) as value_error:
            parse_location_ids.get_distance_two_lists(lst_left=left, lst_right=right)
        assert f"Unequal length of lists, {len(left)} vs {len(right)}" == str(value_error.value)
