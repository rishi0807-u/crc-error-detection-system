from crc import calculate_crc, flip_bit, text_to_binary, validate_binary, verify_crc


def test_binary_validation():
    assert validate_binary("101101")
    assert not validate_binary("10201")
    assert not validate_binary("")


def test_calculation_and_valid_verification():
    result = calculate_crc("101101", "CRC-3")
    assert result["codeword"].startswith("101101")
    assert verify_crc(result["codeword"], "CRC-3")["valid"]


def test_changed_bit_is_detected():
    result = calculate_crc("101101", "CRC-3")
    changed = flip_bit(result["codeword"], 0)
    assert not verify_crc(changed, "CRC-3")["valid"]


def test_text_and_all_algorithms():
    binary = text_to_binary("HELLO")
    for algorithm in ["CRC-3", "CRC-4", "CRC-8", "CRC-32"]:
        result = calculate_crc(binary, algorithm)
        assert verify_crc(result["codeword"], algorithm)["valid"]