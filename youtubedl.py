from __future__ import unicode_literals
import argparse
import youtube_dl
import threading
import os


default_path = os.path.join(os.path.expandvars('%userprofile%'), 'downloads')


def _check_path(path):
    """Checks if the given path is valid"""
    if not os.access(os.path.dirname(path), os.W_OK):
        raise argparse.ArgumentTypeError("cannot write to path '{}'".format(path))
    return path


def run(args):
    def set_options(args):
        """Takes parsed args and builds an options dict to pass to YoutubeDL"""
        ydl_opts = {'outtmpl': '{}\%(title)s.%(ext)s'.format(args.path)}
        ydl_opts['ignoreerrors'] = True
        if args.audio:
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['writethumbnail'] = True
            ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio',
                                      'preferredcodec': 'mp3'},
                                      {'key': 'EmbedThumbnail'}]
        return ydl_opts

    ydl_opts = set_options(args)

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        dl_thread = threading.Thread(target=ydl.download, args=([args.url],))
        dl_thread.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='download youtube videos and convert them to mp3')
    parser.add_argument('url', help='the url of the video to download')
    parser.add_argument('-a', '--audio', action='store_true',
                        help='downloads audio instead of video')
    parser.add_argument('-p', '--path', default=default_path, type=_check_path,
                        help='the path where videos will be saved')
    args = parser.parse_args()

    run(args)