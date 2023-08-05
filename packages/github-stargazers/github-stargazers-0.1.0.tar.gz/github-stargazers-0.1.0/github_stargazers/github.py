import os
import re
import typing

from bs4 import BeautifulSoup
from bs4 import element
import requests


class UsernameRepositoryError(ValueError):

    def __init__(self) -> None:
        super().__init__("Argument should be of form username/repository.")


class TooManyRequestsHttpError(Exception):

    def __init__(self) -> None:
        super().__init__("Too many requests.")


class UrlNotFoundError(Exception):

    def __init__(self, repository: str) -> None:
        super().__init__(f"Resource not Found. Check that the repository {repository or ''} is correct.")


class HTTPError(Exception):

    def __init__(self, status_code: int) -> None:
        super().__init__("{} HTTP.".format(status_code))


class MissingHyperlinkTagError(Exception):

    def __init__(self) -> None:
        super().__init__("Missing hyperlink tag.")


class MissingHrefAttributeError(Exception):

    def __init__(self) -> None:
        super().__init__("Missing 'href' attribute from hyperlink tag.")


class HrefContentError(Exception):

    def __init__(self, href_content: str) -> None:
        super().__init__(f"Wrong 'href' content: '{href_content}'. It should be of form /username.")


class GitHub:
    """Creates a GitHub instance for listing the stargazers of a given repository
    and checking if a user's full name is in the list of stargazers.

    The constructor requires a string of the following form: `username/repository`,
    both representing the GitHub meaning of them.
    """
    __GITHUB_URL: str = "https://github.com"
    __STARGAZERS_URL_SUFFIX: str = "/stargazers"
    __PAGE_SUFFIX: str = "?page="
    __MARK_END_OF_STARGAZERS: str = 'This repository has no more stargazers.'

    __OK_STATUS_CODE: int = 200
    __TOO_MANY_REQUESTS_STATUS_CODE: int = 429
    __NOT_FOUND_STATUS_CODE: int = 404

    def __init__(self, username_and_repository: str) -> None:
        self.__username, self.__repository = GitHub.__extract_user_and_repo(username_and_repository)
        self.__repository_url: str = self.__get_repository_url()
        self.__stargazers_base_url: str = self.__repository_url + self.__STARGAZERS_URL_SUFFIX

    @classmethod
    def __extract_user_and_repo(cls, username_and_repository: str) -> typing.Optional[typing.Tuple[str, str]]:
        components: typing.List[str] = username_and_repository.split("/")
        if len(components) != 2:
            raise UsernameRepositoryError()
        for component in components:
            if component == "":
                raise UsernameRepositoryError()

        return components[0], components[1]

    def __get_repository_url(self) -> str:
        return os.path.join(self.__GITHUB_URL, self.__username, self.__repository)

    def __get_soup(self, url: str) -> BeautifulSoup:
        response: requests.Response = requests.get(url, headers={'Content-Type': 'text/html'})

        status_code: int = response.status_code
        if status_code == self.__OK_STATUS_CODE:
            return BeautifulSoup(response.text, "html.parser")
        if status_code == self.__TOO_MANY_REQUESTS_STATUS_CODE:
            raise TooManyRequestsHttpError()
        if status_code == self.__NOT_FOUND_STATUS_CODE:
            raise UrlNotFoundError(os.path.join(self.__username, self.__repository))
        raise HTTPError(status_code)

    def __extract_stargazers_from_url(self, url: str) -> typing.List[str]:
        soup: typing.Optional[BeautifulSoup] = self.__get_soup(url)
        h3_components: element.ResultSet = soup.find_all('h3')

        def _check_hyperlink_component(component: element.Tag) -> None:
            """Check the BeautifulSoup `element.Tag` component that receives a hyperlink HTML tag.

            The expected structure is as follows:
            '<h3> <a href="/foo"> John Williams </a> </h3>'
            It incrementally dives into the component one tag or attribute of a tag at a time, making sure they appear:
            - the hyperlink tag: <a>
            - the `href` attribute: <a href="..."> </a>
            - the content of hyperlink's `href` attribute.
            The href content contains the GitHub username prefixed by the '/' character, with the following form:
            `/username`.

            If any of the above mentioned is missing or not in the expected form, an Exception is raised.
            """
            hyperlink_component: typing.Optional[element.Tag] = component.find('a')
            if not hyperlink_component:
                raise MissingHyperlinkTagError()
            if not hyperlink_component.get('href'):
                raise MissingHrefAttributeError()
            href_content: str = hyperlink_component['href']
            if not re.match(r"/.+$", href_content):
                raise HrefContentError(href_content)

        def _extract_username_from_h3(component: element.Tag) -> typing.Optional[str]:
            if component.get_text() == self.__MARK_END_OF_STARGAZERS:
                return None
            _check_hyperlink_component(component)
            return component.a['href'][1:]  # dropping the first '/' character

        users: typing.List[str] = []
        for component in h3_components:
            username: typing.Optional[str] = _extract_username_from_h3(component)
            if not username:
                break
            users.append(username)

        return users

    def __get_url_page_template(self, page_number: int) -> str:
        return self.__stargazers_base_url + self.__PAGE_SUFFIX + str(page_number)

    def get_all_stargazers(self) -> typing.List[str]:
        page_number: int = 1

        all_stargazers: typing.List[str] = []
        previous_stargazers: typing.List[str] = []
        while True:
            current_url: str = self.__get_url_page_template(page_number)
            current_stargazers: typing.List[str] = self.__extract_stargazers_from_url(current_url)
            if not current_stargazers:
                break
            if current_stargazers == previous_stargazers:
                break
            all_stargazers += current_stargazers
            previous_stargazers = current_stargazers
            page_number += 1

        return sorted(all_stargazers)

    def is_stargazer(self, user: str) -> bool:
        page_number: int = 1

        previous_stargazers: typing.List[str] = []
        while True:
            current_url: str = self.__get_url_page_template(page_number)
            current_stargazers: typing.List[str] = self.__extract_stargazers_from_url(current_url)
            if not current_stargazers:
                break
            if current_stargazers == previous_stargazers:
                break
            if user in current_stargazers:
                return True
            previous_stargazers = current_stargazers
            page_number += 1

        return False
