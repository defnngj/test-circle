from testdata_func import get_phone
from testdata_func import first_name, last_name, username

# 随机一个手机号
print("手机号:", get_phone())
print("手机号(移动):", get_phone(operator="mobile"))
print("手机号(联通):", get_phone(operator="unicom"))
print("手机号(电信):", get_phone(operator="telecom"))


# 随机一个名字
print("名字：", first_name())
print("名字(男)：", first_name(gender="male"))
print("名字(女)：", first_name(gender="female"))

# 随机一个姓
print("姓:", last_name())

# 随机一个姓名
print("姓名:", username())

