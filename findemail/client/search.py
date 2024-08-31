import typing


from .. import errors

if typing.TYPE_CHECKING:
    from .client import Client


class SearchMethods:

    # region Public methods
    
    def search_domain(self: 'Client', domain: str) -> 'Client':
        """
        Performs domain email search operations.

        Args:
            domain (str): It gets the required domain like google.com.

        Raises:
            ValueError: If there is no information, it shows an error.

        Returns:
            dict: Returns the received information as a dict.
        """
        data = self._request(
            "POST",
            self.url.format("/v1/search/domain"),
            {
                "domain": domain
            }
        )
        
        if not data['ok']:
            raise ValueError(data['message'])
        
        return data['data']

    def search_leak(self: 'Client', data: str, _type: str) -> 'Client':
        """
        Searches for leaked data.

        Args:
            data (str): Gets the required value for search.
            _type (str): Receives the required types for search. (domain, username, email, phone_number, ip)

        Raises:
            InvalidTypeError: This error occurs if _type is wrong.
            ValueError: If there is no information, it shows an error.

        Returns:
            dict: Returns the received information as a dict.
        """
        if _type not in (
            "domain", "username", "email",
            "phone_number", "ip"
        ):
            raise errors.InvalidTypeError("invalid search type!")
        
        data = self._request(
            "POST",
            self.url.format("/v1/search/leak"),
            {
                "type": _type,
                "data": data
            }
        )
        
        if not data['ok']:
            raise ValueError(data['message'])
        
        return data['data']

    def search_logs(self: 'Client', data: str, _type: str) -> 'Client':
        """
        Searches for logs data.

        Args:
            data (str): Gets the required value for search.
            _type (str): Receives the required types for search. (domain, username, port, tech, keyword, sub_domain or subdomain)

        Raises:
            InvalidTypeError: This error occurs if _type is wrong.
            ValueError: If there is no information, it shows an error.

        Returns:
            dict: Returns the received information as a dict.
        """
        if _type not in (
            "domain", "username", "port", "tech",
            "keyword", "sub_domain", "subdomain"
        ):
            raise errors.InvalidTypeError("invalid search type!")
        
        data = self._request(
            "POST",
            self.url.format("/v1/search/logs"),
            {
                "type": _type,
                "data": data
            }
        )
        
        if not data['ok']:
            raise ValueError(data['message'])
        
        return data['data']
