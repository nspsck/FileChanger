import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ChangeFileNameHandler(FileSystemEventHandler):
    def __init__(self, folder_path, target_file_name):
        self.folder_path = folder_path
        self.target_file = os.path.join(folder_path, target_file_name)

    def on_created(self, event):
        if not event.is_directory:
            time.sleep(1)
            new_file_path = event.src_path
            file_extension = os.path.splitext(new_file_path)[1].lower()

            if file_extension in ['.jpg',
                                  '.jpeg',
                                  '.png',
                                  #'.gif',
                                  #'.bmp',
                                  ]:
                print(f"New image detected: {new_file_path}")
                os.rename(new_file_path, self.target_file)
                print(f"Renamed to: {self.target_file}")


if __name__ == "__main__":
    # This has to match with target_file_names
    folders_to_monitor = [
            "/home/teng/Pictures/Stream/Startbild",
            "/home/teng/Pictures/Stream/Schlussbild"
            ] 

    # This has to match with folders_to_monitor
    target_file_names = [
            "Start.jpg",
            "End.jpg"
            ]

    observers = []

    for folder, target_file_name in zip(folders_to_monitor, target_file_names):
        print(f"{folder, target_file_name}")
        event_handler = ChangeFileNameHandler(folder, target_file_name)
        observer = Observer()
        observer.schedule(event_handler, path=folder, recursive=False)
        observers.append(observer)
        print(f"Monitoring folder: {folder}")
        observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for observer in observers:
            observer.stop()

    for observer in observers:
        observer.join()

