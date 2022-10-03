import json
from ...infrastructure.firestore import Criteria, Filter, Operator


def filters_controller(params: str):
    criteria = Criteria(
        filters=[Filter(field='deleted_at', operator=Operator.EQUAL, value=None)])
    try:
        _filters = json.loads(params["filters"])
        for filter_item in _filters:
            criteria.filters.append(Filter(
                filter_item["field"], Operator[filter_item["operator"]], filter_item["value"]))
        return criteria
    except TypeError:
        return criteria
