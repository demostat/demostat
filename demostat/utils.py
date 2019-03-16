class Querystring():
    __params={}
    def __init__(self, dict):
        for key, value in dict.items():
            if isinstance(value, str):
                dict[key] = [value] # Einzelne Werte könne auch direkt als String übergeben werden, die werden hier in eine Liste umgewandelt

        self.__params=dict

    def __to_querystring(self, dict):
        out = ""
        for key, value in dict.items():
            for v in value:
                out += "&" + key + "=" + v

        return "?" + out[1:]

    def raw(self):
        return self.__params

    def get(self):
        return self.__to_querystring(self.__params)

    def get_without(self, key, value):
        dict = self.__params
        if key in dict:
            while value in dict[key]:
                dict[key].remove(value)

        return self.__to_querystring(dict)



if __name__ == "__main__":
    qs = Querystring({
        "tag": [
            "umwelt",
            "internet",
        ],
        "org": "fridaysforfuture",
    })
    print(qs.raw())
    print(qs.get())
    print(qs.get_without("tag", "internet"))
