from csv import DictReader


def import_from_csv(file, entity_cls, database, translation_dict):
    """
    Imports a csv file to the given database.

    :param file: csv file with entity attributes and values
    :param entity_cls: Entity class used to build objects
    :param database: Database to import objects into
    :param translation_dict: Dictionary used to translate keys to match
    the objects attributes
    :return: True if no errors
    """
    with open(file) as f:
        reader = DictReader(f)
        old_list = [d for d in reader]

    new_list = [{translation_dict[old_key]: old_dict[old_key]
                for old_key in translation_dict}
                for old_dict in old_list]

    for obj_dict in new_list:
        database.create(entity_cls(**obj_dict))

    return True

