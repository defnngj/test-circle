from testdata import *

asc = get_ascii(str_size=0)
print(f"生成ascii码: {asc}")

md5 = get_md5()
print(f"生成md5: {md5}")

ha = get_hash(str_size=32)
print(f"生成hash: {ha}")

b = get_bool()
print(f"随机生成布尔: {b}")

f = get_float(min_size=None, max_size=None)
print(f"生成float浮点数: {f}")

i = get_int(min_size=1, max_size=sys.maxsize)
print(f"生成int整型数: {i}")

n = get_name(name_count=2, as_str=True)
print(f"生成name: {n}")

e = get_email()
print(f"生成email: {e}")

s = get_str(str_size=0, chars=None)
print(f"生成字符串: {s}")

u = get_url()
print(f"生成url: {u}")

w = get_words(word_count=0, as_str=True)
print(f"生成单词: {w}")

pd = get_past_datetime()
print(f"生成过去时间: {pd}")

fd = get_future_datetime()
print(f"生成未来时间: {fd}")
