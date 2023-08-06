from bravado.requests_client import RequestsClient
from bravado.client import SwaggerClient
from bravado.swagger_model import load_file
from scabbard.access_token import get_token
import pkg_resources


def get_client():
    access_token = "Bearer " + get_token()
    http_client = RequestsClient()
    http_client.set_api_key(
        'api.test.sabre.com', access_token,
        param_name='Authorization', param_in='header'
    )

    resource_package = __name__
    resource_path = '/swagger.yaml'  # Do not use os.path.join()

    swagger_path = pkg_resources.resource_filename(resource_package, resource_path)
    return SwaggerClient.from_spec(load_file(swagger_path),
                                   http_client=http_client)

