
class Status():
    OK_JSON = {"status": "ok"}
    NOTFOUND_JSON = {"status": "not found"}
    ERROR_JSON = {"status": "error"}
    @staticmethod
    def ok_with_data(data):
        return {"status": "ok", "data":data}