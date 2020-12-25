from enum import Enum


class SheetNameEnum(Enum):
    FRONT_PAGE = '封面页'
    BACK_PAGE = '封底页'
    pass


if __name__ == '__main__':
    print(SheetNameEnum.FRONT_PAGE.value)
    pass
