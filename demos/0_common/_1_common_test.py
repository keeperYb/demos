class anObj:
    def __init__(self, obj_dict: dict):
        self.para1 = [1]
        for key in obj_dict.keys():
            setattr(self, key, obj_dict[key])
        pass

    pass


class source_obj:
    para1: str
    para2: str
    para3: str

    def __init__(self, para_dict):
        for key in para_dict.keys():
            setattr(self, key, para_dict[key])
            pass
        pass

    pass


class dest_obj:
    para1: str
    para2: str

    def my_init(self, para_dict={}):
        if para_dict:
            pass
        elif not para_dict:
            dest_obj.__init__(self)
        pass
    # python init 多态??

    # def __init__(self, para_dict: dict = {}):
    #     self.para1: str
    #     self.para2: str
    #     self.para3: str
    #     for key in para_dict.keys():
    #         setattr(self, key, para_dict[key])
    #         pass
    #     pass

    pass


def copySource2Dest():
    """
    copy the value of source_obj to dest_obj

    :return: None
    """
    source_para_dict = {
        'para1': 'Monster',
        'para2': 'Hunter',
        'para3': 'XX',
    }
    source = source_obj(source_para_dict)
    # how to decode the source_obj and get its attr??
    dest_para_dict = {}
    for attr_name in source.__dict__:
        attr_value = source.__getattribute__(attr_name)
        dest_para_dict[attr_name] = attr_value
        pass
    dest = dest_obj(dest_para_dict)
    for attr_name in dest.__dict__:
        print(dest.__getattribute__(attr_name))
    pass


if __name__ == '__main__':
    # the_obj_dict = {'para1': [2]}
    # obj1 = anObj(the_obj_dict)
    # obj1.para1 = [3]
    dest_o = dest_obj()
    print(dest_o.para1)
    pass
