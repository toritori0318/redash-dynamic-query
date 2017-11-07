import time

import pystache
import requests


class RedashDynamicQuery():
    def __init__(self, endpoint, apikey, data_source_id, max_age=0, max_wait=60):
        self.endpoint = endpoint
        self.apikey = apikey
        self.data_source_id = data_source_id
        self.max_age = max_age
        self.max_wait = max_wait

    def query(self, query_id, bind=None, as_csv=False):
        if as_csv and self.max_age != 0:
            raise Exception('When you want to call it with as_csv argument as True, max_age field have to be 0.')

        # get query body
        query_body = self._api_queries(query_id)['query']

        # bind params to query body
        query_body = self._bind_params(query_body, bind)

        # post query result
        response = self._api_query_results(self._build_query(query_id, query_body))
        if 'query_result' in response:
            return response

        # wait job
        job = response['job']
        job_result = self._wait_job(job)
        query_result_id = job_result['query_result_id']

        # get query result
        if as_csv:
            return self._api_query_results_csv(query_id, query_result_id)

        return self._api_query_results_json(query_id, query_result_id)

    def _bind_params(self, query_body, bind):
        if bind:
            query_body = query_body.replace('{{{', '{{').replace('}}}', '}}')
            query_body = pystache.render(query_body, bind)

        return query_body

    def _build_query(self, query_id, query_body):
        return {
            'query': query_body,
            'query_id': query_id,
            'data_source_id': self.data_source_id,
            'max_age': self.max_age,
        }

    def _wait_job(self, job):
        for x in range(self.max_wait):
            response = self._api_jobs(job['id'])
            job = response['job']
            if job['status'] in [3, 4]:
                break
            time.sleep(1)
        else:
            raise Exception('job wait timeout.')

        if job['error']:
            raise Exception('wait_job failed. [%s]' % job['error'])

        return job

    def _api_queries(self, query_id):
        response = requests.get(
            '%s/api/queries/%s' % (self.endpoint, query_id),
            params={'api_key': self.apikey},
        )
        if response.status_code != 200:
            raise Exception('api_queries. [%d]' % response.status_code)

        return response.json()

    def _api_query_results(self, query_string):
        response = requests.post(
            '%s/api/query_results' % self.endpoint,
            params={'api_key': self.apikey},
            json=query_string,
        )
        if response.status_code != 200:
            raise Exception('query_results failed. [%d]' % response.status_code)

        return response.json()

    def _api_jobs(self, job_id):
        response = requests.get(
            '%s/api/jobs/%s' % (self.endpoint, job_id),
            params={'api_key': self.apikey},
        )
        if response.status_code != 200:
            raise Exception('api_jobs failed. [%d]' % response.status_code)

        return response.json()

    def _api_query_results_json(self, query_id, query_result_id):
        response = requests.get(
            '%s/api/queries/%s/results/%s.json' % (self.endpoint, query_id, query_result_id),
            params={'api_key': self.apikey},
        )
        if response.status_code != 200:
            raise Exception('api_query_results_json failed. [%d]' % response.status_code)

        return response.json()

    def _api_query_results_csv(self, query_id, query_result_id):
        response = requests.get(
            '%s/api/queries/%s/results/%s.csv' % (self.endpoint, query_id, query_result_id),
            params={'api_key': self.apikey},
        )
        if response.status_code != 200:
            raise Exception('api_query_results_csv failed. [%d]' % response.status_code)

        return response.text
