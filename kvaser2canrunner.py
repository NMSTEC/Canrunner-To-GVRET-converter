import sys

def convert_can_log(input_log: str) -> str:
    input_lines = input_log.strip().splitlines()
    output_lines = ["ParserFlags\tCh\tCounter\tT/R\tTime\tFlags\tCAN ID\tLen\tData\tParser Name\tdefault"]

    counter = 1
    for line in input_lines[1:]:
        parts = line.split()

        if "ErrorFrame" in parts or len(parts) < 8:
            continue

        ch, can_id, dlc, data, time, direction = (
            parts[0], parts[1], parts[2], parts[3:3+int(parts[2])], parts[-2], parts[-1]
        )

        ch_hex = hex(int(ch))
        can_id_hex = f"0x{int(can_id):08x}"
        dlc_int = int(dlc)
        data_hex = f"0x{int(data[0]):02x} " + " ".join([f"{int(x):02x}" for x in data[1:]])

        output_line = (
            f"1\t{ch_hex}\t{counter}\t{direction}\t"
            f"{int(float(time) * 1000000)}\tFlags\t{can_id_hex}\t{dlc}\t{data_hex}\tDefault Parser"
        )
        output_lines.append(output_line)
        counter += 1

    return "\n".join(output_lines)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python can_log_converter.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, "r") as f:
        input_log = f.read()

    output_log = convert_can_log(input_log)

    with open(output_file, "w") as f:
        f.write(output_log)
