import click
import requests

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Handler(FileSystemEventHandler):
    def __init__(self, output_url):
        super(Handler, self).__init__()
        self.output_url = output_url

    def on_created(self, event):
        print(event)
        req = requests.post(self.output_url, files={
            'file': open(event.src_path, 'rb')
            })

        print(req.text)


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option('-i', '--input-directory', default='.', help='Input directory to watch')
@click.option('-o', '--output-url', help='Output url to upload to')
def watch(input_directory, output_url):
    """File watcher/uploader"""

    observer = Observer()
    observer.schedule(Handler(output_url), input_directory, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

