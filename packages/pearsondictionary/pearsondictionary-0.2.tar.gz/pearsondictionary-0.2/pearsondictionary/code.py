import json
import logging
import requests


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

# Longman Afrikaans to English
DICT_LEASD = 'leasd'

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
    DICT_LEASD,
    DICT_LASE,
    DICT_BREP
)

ENGLISH_ONLY_DICTS = [
    DICT_LASDE,
    DICT_LDOCE5,
    DICT_LAAD3,
    DICT_WORDWISE
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
API_RESPONSE_DATASETS = 'datasets'



class PearsonDictionary:
    """
    Simple wrapper for Pearson API
    """

    def __init__(self):
        """

        """
        self.session = requests.Session()

        self.session.mount("http://", requests.adapters.HTTPAdapter(max_retries=REQUESTS_MAX_RETRIES))
        self.session.mount("https://", requests.adapters.HTTPAdapter(max_retries=REQUESTS_MAX_RETRIES))

        self.last_request_raw_data = None
        self.last_request_processed_data = {}

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
            ''' Not english dict '''
            non_english = False
            for d in item[API_RESPONSE_DATASETS]:
                if d in['dictionary', 'sandbox']:
                    continue

                if d not in ENGLISH_ONLY_DICTS:
                    non_english = True
                    break

            if non_english:
                continue

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

            if item[API_RESPONSE_SENSES] is not None:
                for sense in item[API_RESPONSE_SENSES]:
                    if API_RESPONSE_DEF in sense:

                        # Sometimes array comes here
                        if isinstance(sense[API_RESPONSE_DEF], list):
                            for s in sense[API_RESPONSE_DEF]:
                                self.last_request_processed_data[item[API_RESPONSE_HEADWORD]]['poses'][item[API_RESPONSE_POS]] = self._append_defnition_to_list(
                                    self.last_request_processed_data[item[API_RESPONSE_HEADWORD]]['poses'][item[API_RESPONSE_POS]],
                                    s
                                )
                        else:
                            self.last_request_processed_data[item[API_RESPONSE_HEADWORD]]['poses'][
                                item[API_RESPONSE_POS]] = self._append_defnition_to_list(
                                self.last_request_processed_data[item[API_RESPONSE_HEADWORD]]['poses'][item[API_RESPONSE_POS]],
                                sense[API_RESPONSE_DEF]
                            )

        # Don't hsave to perform multiple requests
        if self.last_request_raw_data[API_RESPONSE_TOTAL] <= LIMIT and load_all_items == True:
            load_all_items = False

        # Recursive requests if
        if load_all_items and offset + LIMIT < self.last_request_raw_data[API_RESPONSE_TOTAL]:
            return self.get_definitions(word, dictionary=dictionary, pos=pos, offset=offset+LIMIT, load_all_items=load_all_items)

        return self.last_request_processed_data

    def _cleanup_request_data(self):
        self.last_request_raw_data = None
        self.last_request_processed_data = {}

    def _levenshtein(self, s1, s2):
        """

        :param s1:
        :param s2:
        :return:
        """
        if len(s1) < len(s2):
            return self._levenshtein(s2, s1)

        # len(s1) >= len(s2)
        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[
                                 j + 1] + 1  # j+1 instead of j since previous_row and current_row are one character longer
                deletions = current_row[j] + 1  # than s2
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    def _append_defnition_to_list(self, defs, new_def ):
        """

        :param defs:
        :param new_def:
        :return:
        """
        levenshtein_treshold = len(new_def) / 2 # 5% variance
        append = True

        if new_def in defs:
            append = False
        else:
            for d in defs:
                if abs(self._levenshtein(new_def, d)) < levenshtein_treshold:
                    append = False
        if append:
            defs.append(new_def)

        return defs

