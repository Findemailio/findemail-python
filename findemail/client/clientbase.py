from requests import request

import abc
import functools
import time
import typing
import pathlib
import re


from .. import version, errors

if typing.TYPE_CHECKING:
    from .client import Client


DEFAULT_URL = "https://api.findemail.io"

class ClientBase(abc.ABC):
    """
    This is the abstract base class for the client. It defines some
    basic stuff like connecting, etc.

    Arguments
        api_key (`str`, required):
            It's a KEY to use API to perform search and download operations.
            Note: This key has full access to your account on findemail.io.

        url (`str`, optional):
            Establishes the connection between the server and the client.
            There is no need to change, enter the new url if needed.

        timeout (`int` | `float`, optional):
            The timeout in seconds to be used when connecting.

        request_retries (`int` | `None`, optional):
            How many times a request should be retried.

        retry_delay (`int` | `float`, optional):
            The delay in seconds to sleep between automatic reconnections.
    """

    # Current Client version
    __version__ = version.__version__

    # region Initialization

    def __init__(
            self: 'Client',
            api_key: str,
            *,
            url: str = None,
            timeout: int = 10,
            request_retries: int = 5,
            retry_delay: int = 1
    ):
        if (
            not api_key or
            not re.match(
                r"^[0-9A-F]{8}-[0-9A-F]{4}-[4][0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}$",
                api_key
            )
        ):
            raise errors.ApiKeyError("Your API Key cannot be empty or None.")

        self.api_key = api_key

        if not url:
            self.url = DEFAULT_URL + "{}"
        
        else:
            self.url = url + "{}"
        
        self._request_retries = request_retries
        self._retry_delay = retry_delay or 0
        self._timeout = timeout
        
        if self.is_valid():
            pass
    
    @staticmethod
    def retry():
        def decorator(func: typing.Callable) -> typing.Callable:
            @functools.wraps(func)
            def wrapper(self: 'Client', *args, **kwargs) -> typing.Any:
                if self._request_retries < 1 or self._retry_delay <= 0:
                    raise ValueError('invalid usage!')
                    
                for _ in range(1, self._request_retries + 1):
                    try:
                        return func(self, *args, **kwargs)

                    except (
                        errors.ApiKeyError, errors.AccessForbiddenError, errors.NotFoundError,
                        errors.MethodNotAllowedError, errors.FloodWaitError, errors.UnknownError,
                        errors.InvalidInputError, errors.InvalidTypeError
                    ) as err:
                        raise err
                    
                    except Exception as err:
                        if _ == self._request_retries:
                            raise RuntimeError(
                                f'Error: {repr(err)}. \n'
                                f'failed after {self._request_retries} retries.'
                            )

                        else:
                            print(f'Error: {repr(err)} -> Retrying...')
                            time.sleep(self._retry_delay)

            return wrapper
        return decorator
    
    @property
    def headers(self: 'Client') -> dict:
        return {
            "Accept": "application/json,*/*",
            "Content-Type": "application/json",
            "User-Agent": f"findemail-{self.__version__}",
            "X-API-KEY": self.api_key
        }
    
    @retry()
    def _request(self: 'Client', method: str, url: str, json: dict = None) -> dict:
        """
        Handles HTTP requests.

        Args:
            method (str): The method receives the request.
            url (str): Gets the desired URL.
            json (dict, optional): Receives the required values of the request. Defaults to None.

        Raises:
            ApiKeyError: This error occurs if the api_key is wrong.
            AccessForbiddenError: This error occurs if your account has been banned.
            NotFoundError: If there is no URL, it gives an error.
            MethodNotAllowedError: This error occurs if the request method is incorrect.
            InvalidInputError: This error occurs if the request value is incorrect.
            FloodWaitError: This error occurs when the API is used enough per day.
            UnknownError: Indicates the status of the anonymous code.

        Returns:
            dict: It outputs the received information as dictation.
        """
        res = request(
            method, url,
            json=json,
            headers=self.headers,
            timeout=self._timeout
        )
        
        if res.status_code in (200, 400):
            return res.json()
            
        elif res.status_code == 401:
            raise errors.ApiKeyError
        
        elif res.status_code == 403:
            raise errors.AccessForbiddenError(res.json()['message'])
        
        elif res.status_code == 404:
            raise errors.NotFoundError
        
        elif res.status_code == 405:
            raise errors.MethodNotAllowedError(res.json()['message'])
        
        elif res.status_code == 422:
            raise errors.InvalidInputError
        
        elif res.status_code == 429:
            raise errors.FloodWaitError(res.json()['message'])
        
        else:
            raise errors.UnknownError(res.status_code)
    
    @retry()
    def download(
        self: 'Client', _id: str, _type: str,
        *, file_name: typing.Union[str, pathlib.Path] = None
    ):
        """
        It's a file download module that can receive the required data.

        Args:
            _id (str): A special search ID is used for downloading.
            _type (str): download_type, the limit based on the number of items to download and the amount of credit.
            file_name (Union[str, Path], optional): It will be named _id and saved in the same directory.
                                                    To customize, Specify the path and file name. defaults to None.

        Raises:
            InvalidTypeError: This error occurs if _type is wrong.
            ApiKeyError: This error occurs if the api_key is wrong.
            AccessForbiddenError: This error occurs if your account has been banned.
            NotFoundError: This error occurs if _id is no longer available.
            MethodNotAllowedError: This error occurs if the request method is incorrect.
            InvalidInputError: This error occurs if the request value is incorrect.
            FloodWaitError: This error occurs when the API is used enough per day.
            UnknownError: Indicates the status of the anonymous code.

        Returns:
            file_name: Saves the desired file and returns its name.
        """
        
        file_name = file_name if file_name else f"{_id}.txt"
        
        with request(
            "POST",
            self.url.format("/v1/download"),
            json={
                "id": _id,
                "type": _type
            },
            headers=self.headers,
            stream=True
        ) as res:
            if res.status_code == 200:
                with open(file_name, "wb") as file:
                    for chunk in res.iter_content(chunk_size=None):
                        if chunk:
                            file.write(chunk)
                
                return file_name

            if res.status_code == 400:
                raise errors.InvalidTypeError(res.json()['message'])

            elif res.status_code == 401:
                raise errors.ApiKeyError

            elif res.status_code == 403:
                raise errors.AccessForbiddenError(res.json()['message'])

            elif res.status_code == 404:
                raise errors.NotFoundError

            elif res.status_code == 405:
                raise errors.MethodNotAllowedError(res.json()['message'])

            elif res.status_code == 422:
                raise errors.InvalidInputError

            elif res.status_code == 429:
                raise errors.FloodWaitError(res.json()['message'])

            else:
                raise errors.UnknownError(res.status_code)
    
    def is_valid(self: 'Client'):
        data = self._request(
            "GET",
            self.url.format("/v1/user/info")
        )
        
        return data['ok']
    