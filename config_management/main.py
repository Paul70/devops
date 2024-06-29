from .cli_parser import create_parser

def main():
    parser = create_parser()
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
    else:
        args.func()

if __name__ == "__main__":
    main()
