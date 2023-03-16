import argparse
import os

def convert_line(line):
    parts = line.split('\t')
    time = parts[4]
    can_id = parts[6].replace("0x", "")
    direction = parts[3]
    bus = parts[1]
    length = parts[7]
    data = parts[8].replace("0x", "").split(" ")
    extended = "false"

    return f"{time},{can_id},{extended},{direction},{bus},{length},{','.join(data)}"

def convert_datalog(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        outfile.write("Time Stamp,ID,Extended,Dir,Bus,LEN,D1,D2,D3,D4,D5,D6,D7,D8\n")
        header = True

        for line in infile:
            if header:
                header = False
                continue

            converted_line = convert_line(line.strip())
            outfile.write(f"{converted_line}\n")
			
def process_folder(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for file in os.listdir(input_folder):
        input_file = os.path.join(input_folder, file)
        output_file = os.path.join(output_folder, f"{os.path.splitext(file)[0]}.csv")
        if os.path.isfile(input_file) and is_valid_log_file(input_file, "ParserFlags\tCh\tCounter\tT/R\tTime\tFlags\tCAN ID\tLen\tData\tParser Name\tdefault"):
            convert_datalog(input_file, output_file)

def is_valid_log_file(file_path, expected_header):
    with open(file_path, "r") as file:
        first_line = file.readline().strip()
        return first_line == expected_header

def main():
    parser = argparse.ArgumentParser(description="Convert datalog format")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", "--files", nargs=2, metavar=("INPUT_FILE", "OUTPUT_FILE"), help="Path to the input log file and output CSV file")
    group.add_argument("-d", "--directory", nargs=2, metavar=("INPUT_DIR", "OUTPUT_DIR"), help="Path to the input folder and output folder")
    args = parser.parse_args()

    if args.files:
        input_file, output_file = args.files
        convert_datalog(input_file, output_file)
    elif args.directory:
        input_folder, output_folder = args.directory
        process_folder(input_folder, output_folder)

if __name__ == "__main__":
    main()