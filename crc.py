"""Small, easy-to-understand CRC implementation for the dashboard."""

CRC_ALGORITHMS = {
    "CRC-3": "1011",  # x^3 + x + 1
    "CRC-4": "10011",  # x^4 + x + 1
    "CRC-8": "100000111",  # x^8 + x^2 + x + 1
    "CRC-32": "100000100110000010001110110110111",  # standard CRC-32 polynomial
}


def validate_binary(data):
    """Return True only when data is a non-empty binary string."""
    return bool(data) and all(bit in "01" for bit in data)


def text_to_binary(text):
    """Convert text to its UTF-8 bit representation."""
    return "".join(format(byte, "08b") for byte in text.encode("utf-8"))


def bytes_to_binary(data):
    """Convert bytes to a bit string."""
    return "".join(format(byte, "08b") for byte in data)


def calculate_crc(data, algorithm="CRC-3"):
    """Calculate remainder and codeword using modulo-2 division."""
    if algorithm not in CRC_ALGORITHMS:
        raise ValueError("Unsupported CRC algorithm")
    if not validate_binary(data):
        raise ValueError("Data must contain only 0 and 1")

    generator = CRC_ALGORITHMS[algorithm]
    working = list(data + "0" * (len(generator) - 1))

    for position in range(len(data)):
        if working[position] == "1":
            for offset, bit in enumerate(generator):
                working[position + offset] = str(
                    int(working[position + offset]) ^ int(bit)
                )

    remainder = "".join(working[-(len(generator) - 1) :])
    return {
        "data": data,
        "generator": generator,
        "appended_data": data + "0" * (len(generator) - 1),
        "remainder": remainder,
        "codeword": data + remainder,
    }


def verify_crc(codeword, algorithm="CRC-3"):
    """Return True when dividing the received codeword gives all zeroes."""
    if algorithm not in CRC_ALGORITHMS:
        raise ValueError("Unsupported CRC algorithm")
    if not validate_binary(codeword):
        raise ValueError("Codeword must contain only 0 and 1")
    generator = CRC_ALGORITHMS[algorithm]
    if len(codeword) < len(generator) - 1:
        raise ValueError("Codeword is too short for this algorithm")

    working = list(codeword)
    for position in range(len(codeword) - len(generator) + 1):
        if working[position] == "1":
            for offset, bit in enumerate(generator):
                working[position + offset] = str(
                    int(working[position + offset]) ^ int(bit)
                )
    remainder = "".join(working[-(len(generator) - 1) :])
    return {"valid": set(remainder) == {"0"}, "remainder": remainder}


def flip_bit(codeword, position):
    """Flip one zero-based bit position."""
    if not validate_binary(codeword):
        raise ValueError("Codeword must contain only 0 and 1")
    if position < 0 or position >= len(codeword):
        raise ValueError("Bit position is outside the codeword")
    bits = list(codeword)
    bits[position] = "1" if bits[position] == "0" else "0"
    return "".join(bits)