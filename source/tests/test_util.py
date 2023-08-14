from util import convert_timestamp_to_jst_iso

def test_convert_timestamp_to_jst_iso():
    timestamp = 1679472645
    expected_iso = "2023-03-22T17:10:45+0900"
    result_iso = convert_timestamp_to_jst_iso(timestamp)
    assert result_iso == expected_iso

def test_convert_timestamp_to_jst_iso_millisec():
    timestamp = 1679472645123
    expected_iso = "2023-03-22T17:10:45+0900"
    result_iso = convert_timestamp_to_jst_iso(timestamp)
    assert result_iso == expected_iso
