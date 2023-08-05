from trunity_3_client.utils.url import Url, API_ROOT


base_url = Url(API_ROOT)
base_url.tail = 'remote_files'


class FilesListClient(object):
    _url = base_url.list

    def __init__(self, session):
        self._session = session

    def post(self, remote_file_url: str=None, file_path=None) -> str:
        """
        Upload a file.
        (extension white list: jpg jpeg gif png doc pdf)

        :return: file_url
        """

        if remote_file_url:
            data = {
                'remote_file[remote_file_url]': remote_file_url,
            }
            response = self._session.post(self._url, data)

        elif file_path:

            with open(file_path, 'rb') as file_object:
                files = {'remote_file[file]': file_object}
                response = self._session.post(self._url, files=files)

        else:
            raise ValueError(
                "You should set either remote_file_url or file_path!"
            )

        response.raise_for_status()
        return response.json()['file_url']


class FilesClient(object):

    def __init__(self, session):
        self.list = FilesListClient(session)
