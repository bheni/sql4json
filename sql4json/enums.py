class CEnum(object):
    def __init__(self, enum_items):
        self.__enum_items = enum_items

        index = 0
        for item in enum_items:
            self.__dict__[item] = index
            index += 1

        self.COUNT = index

    def choices(self):
        choices = []

        for item in self.__enum_items:
            choices.append((self.__dict__[item], item))

        return choices


class JavaEnum(object):
    class JavaEnumItem(object):
        def __init__(self, item, enum_fields):
            for field_index, field in enumerate(enum_fields):
                self.__dict__[field] = item[field_index + 1]

    def __init__(self, enum_fields, enum_items):
        self.__vals = []
        for item in enum_items:
            self.__dict__[item[0]] = JavaEnum.JavaEnumItem(item, enum_fields)
            self.__vals.append(self.__dict__[item[0]])

    def values(self):
        return self.__vals
