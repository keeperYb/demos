class anObj:
    def __init__(self, obj_dict: dict):
        self.para1 = [1]
        for key in obj_dict.keys():
            setattr(self, key, obj_dict[key])
        pass
    pass


if __name__ == '__main__':
    the_obj_dict = {'para1': [2]}
    obj1 = anObj(the_obj_dict)
    obj1.para1 = [3]
    pass
