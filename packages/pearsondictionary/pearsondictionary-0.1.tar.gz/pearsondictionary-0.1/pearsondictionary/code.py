import json
import logging
import requests
import collections


REQUESTS_MAX_RETRIES = 3


# Longman Active Study Dictionary
DICT_LASDE = 'lasde'

# Longman Dictionary of Contemporary English (5th edition)
DICT_LDOCE5 = 'ldoce5'

# Longman Advanced American Dictionary
DICT_LAAD3 = 'laad3'

# Longman Wordwise Dictionary
DICT_WORDWISE = 'wordwise'

# Longman English-Chinese Dictionary of 100,000 Words (New 2nd Edition)
DICT_LDEC = 'ldec'

# Longman Afrikaans to English
DICT_LAESD = 'laesd'

# English to Latin American Spanish
DICT_LASE = 'lase'

# English to Brazilian Portuguese
DICT_BREP = 'lase'



# List of valid dict codes
DICTS = (
    DICT_LDOCE5,
    DICT_LASDE,
    DICT_LAAD3,
    DICT_WORDWISE,
    DICT_LDEC,
    DICT_LAESD,
    DICT_LASE,
    DICT_BREP
)

ENGLISH_ONLY_DICTS = [
    DICT_LASDE,
    DICT_LDOCE5,
    DICT_LAAD3,
]

# Pearson API endpoint
API_ENDPOINT = 'http://api.pearson.com/v2/'

# Request limit
LIMIT = 25


# API response fields
API_RESPONSE_RESULTS = 'results'
API_RESPONSE_SENSES = 'senses'
API_RESPONSE_HEADWORD = 'headword'
API_RESPONSE_POS = 'part_of_speech'
API_RESPONSE_DEF = 'definition'
API_RESPONSE_TOTAL = 'total'



class PearsonDictionary:
    """
    Simple wrapper for Pearson API
    """

    def __init__(self, english_only=True):
        """

        """
        self.session = requests.Session()

        self.session.mount("http://", requests.adapters.HTTPAdapter(max_retries=REQUESTS_MAX_RETRIES))
        self.session.mount("https://", requests.adapters.HTTPAdapter(max_retries=REQUESTS_MAX_RETRIES))

        self.last_request_raw_data = None
        self.last_request_processed_data = {}

        self.english_only = english_only

    def is_english_dict(self, dict):
        """

        :param dict:
        :return:
        """
        if dict not in DICTS:
            raise Exception('PearsonDictionary trying to use non-English dict english_only mode {0}'.format(dict))

    def is_legit_dictionary(self, dict):
        """
        Validate dictionary code
        :param dict:
        :return:
        """
        if dict not in DICTS:
            raise Exception('PearsonDictionary invalid dictionary code {0}'.format(dict))

    def get_definitions(self, word, dictionary=None, pos=None, offset=0, load_all_items=False):
        path = 'dictionaries/entries'

        if dictionary is not None and self.is_legit_dictionary(dictionary):
            path = 'dictionaries/{0}/entries'.format(dictionary)

        request_address = '{0}{1}?headword={2}&limit={3}&offset={4}'.format(
            API_ENDPOINT, path, word, LIMIT, offset
        )

        if  pos is not None:
            request_address += '?{0}={1}'.format(API_RESPONSE_POS, pos)

        r = self.session.get(request_address)

        if not r.status_code == 200:
            logging.exception('PearsonDictionary: invalid response code: {0}, URL: {1}'.format(
                r.status_code,
                request_address
            ))

            # In case we are getting all records from API and one of requests failed: we still may return some results
            if len(self.last_request_processed_data) > 0:
                return self.last_request_processed_data

            return None

        self.last_request_raw_data = json.loads(r.text)

        if API_RESPONSE_RESULTS not in self.last_request_raw_data:
            logging.exception('PearsonDictionary: corrupted JSON answer: {0}, URL: {1}'.format(
                r.text,
                request_address
            ))

            return None

        for item in self.last_request_raw_data[API_RESPONSE_RESULTS]:

            # No definitions or no POS tags
            if API_RESPONSE_SENSES not in item or API_RESPONSE_POS not in item:
                continue

            if item[API_RESPONSE_HEADWORD] not in self.last_request_processed_data:
                self.last_request_processed_data[item[API_RESPONSE_HEADWORD]] = {
                    'word': item[API_RESPONSE_HEADWORD],
                    'poses': {}
                }

            # New POS for this word
            if  item[API_RESPONSE_POS] not in self.last_request_processed_data[item[API_RESPONSE_HEADWORD]]['poses']:
                self.last_request_processed_data[item[API_RESPONSE_HEADWORD]]['poses'][item[API_RESPONSE_POS]] = []

            for sense in item[API_RESPONSE_SENSES]:
                if API_RESPONSE_DEF in sense:

                    # Sometimes array comes here
                    if isinstance(sense[API_RESPONSE_DEF], list):
                        for s in sense[API_RESPONSE_DEF]:
                            if s not in self.last_request_processed_data[item[API_RESPONSE_HEADWORD]]['poses'][item[API_RESPONSE_POS]]:
                                self.last_request_processed_data[item[API_RESPONSE_HEADWORD]]['poses'][item[API_RESPONSE_POS]].append(s)
                    else:
                        self.last_request_processed_data[item[API_RESPONSE_HEADWORD]]['poses'][item[API_RESPONSE_POS]].append(sense[API_RESPONSE_DEF])

        # Don't hsave to perform multiple requests
        if self.last_request_raw_data[API_RESPONSE_TOTAL] <= LIMIT and load_all_items == True:
            load_all_items = False

        # Recursive requests if
        if load_all_items and offset + LIMIT < self.last_request_raw_data[API_RESPONSE_TOTAL]:
            print('RECURSION')
            return self.get_definitions(word, dictionary=dictionary, pos=pos, offset=offset+LIMIT, load_all_items=load_all_items)

        return self.last_request_processed_data

    def _cleanup_request_data(self):
        self.last_request_raw_data = None
        self.last_request_processed_data = {}
