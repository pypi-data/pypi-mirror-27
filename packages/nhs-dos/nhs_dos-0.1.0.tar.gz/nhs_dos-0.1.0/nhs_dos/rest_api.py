import requests

from . import users
from .models import Service, ServiceList
from .exceptions import DosClientException

uat_url = 'https://uat.pathwaysdos.nhs.uk/app/controllers/api/v1.0/'


class RestApiClient:
    """
    Client object for performing requests against the DoS Rest API
    """
    def __init__(self, user: users.User, url: str=uat_url):

        self.user = user
        self.url = url
        self.s = requests.Session()
        self.s.auth = (user.username, user.password)

    def get_service_by_id(self, service_id):

        api_path = '/app/controllers/api/v1.0/services/byServiceId/'

        url = f'{self.url}{api_path}{service_id}'

        try:
            response = self.s.get(url)

        except requests.RequestException as e:
            raise e

        except Exception as e:
            raise DosClientException("Unable to complete request")

        service_count = int(response.json()['success']['serviceCount'])

        if service_count == 1:
            s1 = Service(response.json()['success']['services'][0])
            print(s1.id)
            print(s1.name)
            print(s1.endpoints)
            return s1
        elif service_count == 0:
            return ServiceList()
        else:
            raise DosClientException("Didn't get 0 or 1 services returned")

    def get_service_by_ods(self, ods_code):
        api_path = '/app/controllers/api/v1.0/services/byOdsCode/'

        url = f'{self.url}{api_path}{service_id}'

        try:
            response = self.s.get(url)

        except requests.RequestException as e:
            raise e

        except Exception as e:
            raise DosClientException("Unable to complete request")

        service_count = int(response.json()['success']['serviceCount'])

        if service_count == 1:
            s1 = Service(response.json()['success']['services'][0])
            print(s1.id)
            print(s1.name)
            print(s1.endpoints)
            return s1
        elif service_count == 0:
            return ServiceList()
        else:
            raise DosClientException("Didn't get 0 or 1 services returned")

    def get_services_by_clinical_capability(self, case):
        raise NotImplementedError("Method not yet implemented.")

    def get_services_by_type(self, list_of_types):
        raise NotImplementedError("Method not yet implemented.")
