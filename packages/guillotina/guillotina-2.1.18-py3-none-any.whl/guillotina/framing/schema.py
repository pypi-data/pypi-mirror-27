from guillotina import configure
from guillotina.component import get_multi_adapter
from guillotina.component import query_utility
from guillotina.component.interfaces import IFactory
from guillotina.interfaces import IRequest
from guillotina.interfaces import IResourceSerializeToJson
from guillotina.renderers import IFrameFormatsJson


@configure.adapter(for_=IRequest, provides=IFrameFormatsJson, name="schema")
class Framing(object):

    def __init__(self, request):
        self.request = request

    async def __call__(self, json_value):
        if self.request.resource:
            fti = query_utility(
                IFactory, name=self.request.resource.type_name)
            schema_summary = get_multi_adapter(
                (fti, self.request), IResourceSerializeToJson)
            json_value['schema'] = await schema_summary()
        return json_value
