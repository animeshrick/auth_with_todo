from flask.json import jsonify
import json
from decimal import Decimal


class Input(object):
    """
    input class
    """

    def __init__(self):
        """
        Constructor
        """
        self.rules = {}
        self.request = None
        self.params = None
        self.headerparams = None

    def register_request(self, request, copyheader=[], removehyphen=True):
        """
        @param request: request object
        @param copyheader: list. Copies header to body. Contains list of header fields to be copied in to body
        @param removehyphen: boolean. if True removes '-' hyphens from header field name. e.g. Content-Type becomes ContentType
        """
        self.request = request
        self.headerparams = dict(self.request.headers)
        if self.request.method == "GET":
            self.params = self.request.args.to_dict()
        else:
            if (
                self.request.headers.get("Content-Type", "").lower()
                == "application/json"
            ):
                self.params = self.request.get_json()
            else:
                self.params = self.request.form.to_dict()

        if len(copyheader) > 0:
            hkeys = self.headers().keys()
            hkeys2 = [k.replace("-", "") for k in hkeys]
            hkeymap = dict(zip(hkeys2, hkeys))
            hkeymap.update(dict(zip(hkeys, hkeys)))
            for x in copyheader:
                if hkeymap.get(x, False) and self.headers(hkeymap[x]) is not None:
                    if removehyphen is True:
                        self.params[x.replace("-", "")] = self.headers(hkeymap[x])
                    else:
                        self.params[x] = self.headers(hkeymap[x])

    def get(self, field=None):
        return self.params if field is None else self.params.get(field, None)

    def post(self, field=None):
        return self.params if field is None else self.params.get(field, None)

    def headers(self, field=None):
        return (
            self.headerparams if field is None else self.headerparams.get(field, None)
        )

    # def set_rules(self, rules, field=None):
    #     '''
    #     set validation rules
    #     @param rules: dictionary of rules
    #     @param field: if not set, all fields exists in rules are validated.
    #     if string is set e.g. 'field1' only field1 is validated,
    #     if a list of fields is sent those fields are validated
    #     '''
    #     if field is None:
    #         self.rules = rules
    #     elif isinstance(field, list):
    #         for val in field:
    #             if val in rules:
    #                 self.rules[val] = rules[val] #rules.get(val, {})
    #     elif field in rules:
    #         self.rules[field] = rules.get(val, {})

    #     def validate(self):
    #         '''
    #         validate each data as per set rules
    #         '''
    #         op = {}
    #         is_valid_all = True
    #         for field_name in self.rules:
    #             if (self.rules[field_name]['type'] != 'Custom'):
    #                 klass = getattr(validator, self.rules[field_name]['type'])
    #                 try:
    #                     is_valid, op_tmp, value = klass.check(self.rules[field_name], self.params.get(field_name))
    #                     self.params[field_name] = value
    #                 except:
    #                     is_valid, op_tmp = klass.check(self.rules[field_name], self.params.get(field_name))
    #
    #
    #                 is_valid_all = is_valid and is_valid_all
    #                 if op_tmp != {}:
    #                     op[field_name] = op_tmp
    # #         print(is_valid)
    # #         print(op)
    #         return is_valid_all, op

    def parse_rules(self, rule_str):
        rule_list = rule_str.split("|")


inp = Input()


def default(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)


def out(
    data: object,
    status: object = 2000,
    msg: object = "done successfully",
    raw: object = False,
) -> object:
    """
    output function
    """

    data = json.dumps(data, default=default)
    data = json.loads(data)

    if raw:
        return jsonify(data)
    else:
        return jsonify({"status": status, "message": msg, "data": data})


def err(
    data="Be patient!! - error teaches new thing! :)",
    status=5000,
    msg="some error occurred",
    raw=False,
):
    """
    output function
    """

    data = json.dumps(data, default=default)
    data = json.loads(data)

    if raw:
        return jsonify(data)
    else:
        return jsonify({"status": status, "message": msg, "data": data})
