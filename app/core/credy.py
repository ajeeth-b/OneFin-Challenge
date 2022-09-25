import requests
from django.conf import settings as app_settings
from requests.exceptions import RequestException
from requests.adapters import HTTPAdapter


def get_movies(page=1, max_retries=1):

    session = requests.Session()
    session.mount("", HTTPAdapter(max_retries=max_retries))
    session.auth = (app_settings.CREDY_USERNAME, app_settings.CREDY_PASSWORD)
    try:
        response = session.get(
            "{url}?page={page}".format(
                url=app_settings.CREDY_MOVIES_URL,
                page=page,
            )
        )
    except RequestException:
        return False, None

    if response.status_code != 200:
        print(response)
        return False, None

    return True, response.json()
