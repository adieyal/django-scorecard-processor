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
