import argparse


def main():
    parser = argparse.ArgumentParser("py-term-watcher")
    parser.add_argument("path", help="Path to file")
    args = parser.parse_args()
    print(args.path)
    # if --u:
    #     video = openUrl()
    # else:
    #     video = openFile()
    # watch(video)


if __name__ == "__main__":
    main()
