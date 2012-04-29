import tablib
import xlrd

def import_xls(in_stream, headers=True):
    """Returns databook from XLS stream."""
    dbook = tablib.Databook()
    wb = xlrd.open_workbook(file_contents=in_stream)
    for ws in wb.sheets():
        data = tablib.Dataset()
        data.title = ws.name
        for i in range(ws.nrows):
            if (i == 0) and (headers):
                data.headers = ws.row_values(i)
            else:
                data.append(ws.row_values(i))
        dbook.add_sheet(data)
    return dbook

from django.core.serializers.json import simplejson, DjangoJSONEncoder
from django.http import HttpResponse
from plugins.types import Scalar, Vector
from decimal import Decimal

class JSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if hasattr(o,'_as_dict'):
            return o._as_dict()
        elif isinstance(o, Scalar):
            return unicode(o.get_value())
        elif isinstance(o, Vector):
            return o.get_values()
        else:
            return super(JSONEncoder, self).default(o)

from ordereddict import OrderedDict

def render_json(output):
    if 'data' in output and isinstance(output['data'],dict) or isinstance(output['data'], OrderedDict):
        output['data'] = OrderedDict([(k.name, v) for k,v in output['data'].items()])
    return HttpResponse(simplejson.dumps(output, cls=JSONEncoder, indent=2), content_type="application/json")
