"""
Tool to avoid many checks is every record in related tables exist.
Returns None if any of records are missing, so it's easy to get value or None
with no catching exceptions.

>>> def user_info(request):
>>>     return {
>>>         "name": request.user.username,
>>>         "email": request.user.email,
>>>         "phone": attr_chain(request.user, "contacts.phone_number") or "Undefined",
>>>         "gender": attr_chain(request.user, "profile.gender") or "🏳️‍🌈",
>>>     }

"""


def attr_chain(obj: object, attr_string: str) -> object | None:
    """
    Checks attributes of an `obj` step by step
    and returns `None` or a resulting value

    """
    chain = attr_string.split(".")
    if not chain:
        return None
    result = obj
    for chainlink in chain:
        result = getattr(result, chainlink, None)
        if result is None:
            return None
    return result
