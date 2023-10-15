from csv_paser import CSVParser


PARSERS = {
    "CSVParser": CSVParser,
}

def get_parser(file_name, event):
    for key, value in PARSERS.items():
        if value.match_file(file_name):
            return value(event)

    raise ValueError(file_name)


def execute(event, file_name, file_path):
    parser = get_parser(file_name, event)
    return parser.run(file_path)
