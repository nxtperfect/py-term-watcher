import argparse


def main():
    parser = argparse.ArgumentParser("py-term-watcher")
    parser.add_argument("path", help="Path to file")
    parser.add_argument("-u", "--url", help="url to video")
    args = parser.parse_args()
    print(args.path)
    if args.url:
        video = openUrl()
    else:
        video = openFile()
    watch(video)


if __name__ == "__main__":
    main()
