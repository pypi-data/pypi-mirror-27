import requests
import requests.utils
from .py_ms_cognitive_search import PyMsCognitiveSearch
from .py_ms_cognitive_search import QueryChecker


class PyMsCognitiveImageException(Exception):
    pass


class PyMsCognitiveImageSearch(PyMsCognitiveSearch):

    SEARCH_IMAGE_BASE = 'https://api.cognitive.microsoft.com/bing/v7.0/images/search'

    def __init__(self, api_key, query, custom_params={}, silent_fail=False,):
        query_url = self.SEARCH_IMAGE_BASE
        PyMsCognitiveSearch.__init__(self, api_key, query, query_url, custom_params, silent_fail=silent_fail)

    def _search(self, limit, format):
        """
        Returns a list of result objects, with the url for the next page MsCognitive search url.

        :param limit:
        :param format:
        :return:
        """
        limit = min(limit, self.MAX_SEARCH_PER_QUERY)
        payload = {
          'q': self.query,
          'count': limit,  # Currently 50 is max per search.
          'offset': self.current_offset,
        }
        payload.update(self.CUSTOM_PARAMS)

        headers = {'Ocp-Apim-Subscription-Key': self.api_key}

        if not self.silent_fail:
            QueryChecker.check_web_params(payload, headers)

        response = requests.get(self.QUERY_URL, params=payload, headers=headers)
        json_results = self.get_json_results(response)
        packaged_results = [ImageResult(single_result_json) for single_result_json in json_results["value"]]
        self.current_offset += min(50, limit)

        return packaged_results


class ImageResult(object):
    """
    The class represents a SINGLE Image result.
    Each result will come with the following:

    json: contains all the information returned from the API request
    url: web address of the image
    name: name of the image / page title
    extension: image extension
    """

    def __init__(self, result):
        self.json = result
        self.url = result.get('contentUrl')
        self.name = result.get('name')
        self.extension = result.get('encodingFormat')

