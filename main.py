from ArgsList import ArgStore
from Parser import Parser


def main():
    parser = Parser()
    print(parser.create_args(ArgStore.convert_args_to_dict_with_internal_names()))


if __name__ == "__main__":
    main()
