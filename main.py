import os

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import SearchRequest
from telethon.tl.types import InputMessagesFilterPhotos

from settings import API_ID, API_HASH


class TGMediaDownloader:
    def __init__(self, api_id, api_hash):
        """Class constructor"""
        self.client = TelegramClient('TGMediaDownloader', api_id, api_hash)

    def download_pictures(self, target_username, limit=None):
        """Call the download function using photos filter"""
        self.__download(target_username, limit, InputMessagesFilterPhotos())

    def __download(self, target_username, limit, filter_f):
        """Start download process"""
        with self.client:
            target = self.client.get_entity(target_username)

            # Create some directories
            if not os.path.isdir("Backup"):
                os.mkdir("Backup")
                os.mkdir("Backup/" + target_username)
            elif not os.path.isdir("Backup/" + target_username):
                os.mkdir("Backup/" + target_username)

            if not limit:
                # Get message count for the chat
                result = self.client(SearchRequest(
                    peer=target,
                    q='',
                    filter=filter_f,
                    min_date=None,
                    max_date=None,
                    offset_id=0,
                    add_offset=0,
                    limit=0,
                    max_id=0,
                    min_id=0,
                    hash=0
                ))

                msg_count = result.count
            else:
                msg_count = limit

            offset = 0

            # Get messages (max 100 for each request)
            while offset < (msg_count - 1):
                result = self.client(SearchRequest(
                    peer=target_username,
                    q='',
                    filter=filter_f,
                    min_date=None,
                    max_date=None,
                    offset_id=0,
                    add_offset=offset,
                    limit=100,
                    max_id=0,
                    min_id=0,
                    hash=0
                ))

                for i in range(len(result.messages)):
                    media = result.messages[i]
                    self.client.download_media(media, "Backup/" + target_username) 
                    print("Downloading {0}%".format(((offset+i)/msg_count)*100))

                offset = offset + i

            print("Done!")


if __name__ == "__main__":
    downloader = TGMediaDownloader(API_ID, API_HASH)

    username = input("Username: ")
    downloader.download_pictures(username)
