def get_all_subclasses(cls):
    all_subclasses = []

    direct_subclasses = cls.__subclasses__()

    all_subclasses.extend(direct_subclasses)

    for subclass in direct_subclasses:
        all_subclasses.extend(get_all_subclasses(subclass))

    return all_subclasses
