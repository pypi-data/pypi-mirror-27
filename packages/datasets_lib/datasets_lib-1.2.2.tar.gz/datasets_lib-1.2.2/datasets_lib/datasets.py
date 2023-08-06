import requests
from urljoin import url_path_join

from .datasets_config import DatasetsConfig


class Datasets(object):
    """
        Library for datasets browsing and management
    """

    def __init__(self, conf=DatasetsConfig()):
        # type: (DatasetsConfig) -> None
        """

        Args:
            conf (DatasetsConfig): instance of Datasets configuration class
        """
        self.conf = conf

    def list(self):
        # type: () -> dict
        """ Get all projects

        Returns:
            dict: list of all datasets
        """
        return requests.get(self.get_address()).json()

    def new(self):
        # type: () -> dict
        """Get new project ID

        Returns:
            dict: New dataset properties
        """
        # todo put/post?
        return requests.get(url_path_join(self.get_address(), "new")).json()

    def use(self, ds_id, usage={}):
        # type: (str, dict) -> dict
        """Get dataset info with use note

        Args:
            ds_id (str): dataset id
            usage (dict): usage details

        Returns:
            dict: dataset details
        """
        return requests.post(url_path_join(self.get_address(), "use", ds_id),
                             json=usage).json()

    def scan(self):
        # type: () -> None
        """ Force local fs rescan
        """
        return requests.get(url_path_join(self.get_address(), "scan"))

    def project_details(self, ds_id):
        # type (str) -> dict
        """ Get project details

        Args:
            ds_id (str): dataset id

        Returns:
            dict: Dataset details
        """
        return requests.get(url_path_join(self.get_address(),
                                          "detail",
                                          ds_id)).json()

    def update(self, ds_id, data):
        # type: (str, dict) -> None
        """ Update project details

        Args:
            ds_id (str): dataset id
            data (dict): new dataset properties
        """
        return requests.post(url_path_join(self.get_address(), "update", ds_id),
                             json=data)

    def reload(self):
        # type: () -> None
        """ Force server to reload DB
        """
        requests.post(url_path_join(self.get_address(), "reload"))

    def get_address(self):
        # type: () -> str
        """

        Returns:
            str: server address
        """
        return "{}://{}:{}".format("https" if self.conf.ssl else "http",
                                   self.conf.host,
                                   self.conf.port)
