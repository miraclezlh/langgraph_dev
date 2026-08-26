

if __name__ == "__main__":
    # all函数，用于判断：可迭代对象中，是否包含真值。全部为真，或者对象为空时，返回True，否则返回False

    print('==========列表list,存储bool类型的数据，举例=============')
    print(all([True, True, True]))        # 都是True，返回True
    print(all([True, False, True]))       # 包含False，返回False

    print('==========列表list,存储int类型的数据，举例=============')
    print(all([1, 2, 3]))        # 都是非0数字，返回True
    print(all([-1, 2, 3]))       # 只要不包含0，都返回True
    print(all([1, 2, 0]))       # 包含0，返回False

    print('==========元组tuple（数据不可变）,存储bool类型的数据，举例=============')
    print(all((True, True, True)))        # 都是True，返回True
    print(all((True, False, True)))       # 包含False，返回False

    print('==========元组tuple（数据不可变）,存储int类型的数据，举例=============')
    print(all((1, 2, 3)))        # 都是非0数字，返回True
    print(all((-1, 2, 3)))       # 只要不包含0，都返回True
    print(all((1, 2, 0)))       # 包含0，返回False

    print('===========列表list,存储字符串str的数据，举例============')
    print(all(["hello", "world"]))        # True（非空字符串是真值）
    print(all(["hello", ""]))             # False（列表里存在空字符串，是假值）

    print('===========元组tuple（数据不可变）,存储字符串str的数据，举例============')
    print(all(("hello", "world")))        # True（非空字符串是真值）
    print(all(("hello", "")))             # False（元组里存在空字符串，是假值）

    print('============空对象,举例==============')
    print(all([""]))                        # False
    print(all(("")))                        # True 特殊情况
    print(all([]))                        # True（空列表,返回True）
    print(all(()))                        # True（空元组,返回True）



    allowed_chars = set("0123456789+-*/()[].e")

    print(type(c in allowed_chars for c in '2+3*7'))
    print(c in allowed_chars for c in '2+3*7')