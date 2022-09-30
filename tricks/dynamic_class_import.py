def get_external_class(sender_model: str) -> type | None:
    sm_list = sender_model.split('.')
    sm_path = '.'.join(sm_list[:-1])
    sm_class = sm_list[-1]
    try:
        sm_import_path = __import__(sm_path, fromlist=[''])
    except ModuleNotFoundError:
        return None
    return getattr(sm_import_path, sm_class, None)


if __name__ == "__main__":
    sender_model = 'research.models.Drug'
    if model := get_external_class(sender_model):
        print(model.__name__)
