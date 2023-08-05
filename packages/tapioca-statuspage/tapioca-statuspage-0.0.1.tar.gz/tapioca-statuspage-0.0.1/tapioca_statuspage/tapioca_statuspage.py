from tapioca import (
    TapiocaAdapter, generate_wrapper_from_adapter, JSONAdapterMixin)


from .resource_mapping import RESOURCE_MAPPING


class StatuspageClientAdapter(JSONAdapterMixin, TapiocaAdapter):
    api_root = 'https://api.statuspage.io/v1/'
    resource_mapping = RESOURCE_MAPPING

    def get_request_kwargs(self, api_params, *args, **kwargs):
        params = super(StatuspageClientAdapter, self).get_request_kwargs(
            api_params, *args, **kwargs)

        params['headers'].update(api_params.get('credentials'))

        return params

    def get_iterator_list(self, response_data):
        return response_data

    def get_iterator_next_request_kwargs(self, iterator_request_kwargs,
                                         response_data, response):
        pass


Statuspage = generate_wrapper_from_adapter(StatuspageClientAdapter)
