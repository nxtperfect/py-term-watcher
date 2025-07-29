import argparse

from src.video import Video


def main():
    parser = argparse.ArgumentParser("py-term-watcher")
    parser.add_argument("path", help="Path to file")
    parser.add_argument("-u", "--url", help="url to video")
    args = parser.parse_args()
    video = Video(args.path)
    video.play_video()
    watch(video)


if __name__ == "__main__":
    main()
