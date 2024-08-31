import typing


if typing.TYPE_CHECKING:
    from .client import Client


class UsersMethods:

    # region Public methods
    
    def get_me(self: 'Client') -> dict:
        """
        Receives account information.

        Raises:
            ValueError: If there is no information, it shows an error.

        Returns:
            dict: Returns the received information as a dict.
        """
        data = self._request(
            "GET",
            self.url.format("/v1/user/info")
        )
        
        if not data['ok']:
            raise ValueError(data['message'])
        
        return data['data']
