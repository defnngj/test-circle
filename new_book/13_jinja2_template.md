## jina模板引擎

Jinja是一个快速、表达能力强、可扩展的模板引擎。模板中的特殊占位符允许编写类似于Python语法的代码。然后向模板传递数据以呈现最终文档。

文档：https://jinja.palletsprojects.com/

```shell
> pip install Jinja2
```

## jina基础使用

* 例1：模板变量

```py
from jinja2 import Template
template = Template('Hello {{ name }}!')
template.render(name='John Doe')
```

`hello {{ name }}` 是定义的模板，`{{ name }}` 定义的变量。`template.render(name='John Doe')`对模板中变量name赋值。这其实有点像python 字符串格式化。

运行结果：

```shell
Hello John Doe!
```

* 例2：HTML模板

```py
from jinja2 import Template


template = Template("""
<html>
<body>

<h1> bobby: </h1>
{% for item in hobby %}
    <input type="checkbox" checked>{{item}}
{% endfor %}

</body>
</html>
""")
tmp = template.render(hobby=["eat", "sleep", "code"])
print(tmp)
```

模板中定义了HTML标签。 `{% for i in xxx %} ...{% endfor %}` 是模板语言for循环的写法；`hobby` 传入列表。

运行结果：

```html
<html>
<body>

<h1> bobby: </h1>
    <input type="checkbox" checked>eat
    <input type="checkbox" checked>sleep
    <input type="checkbox" checked>code

</body>
</html>
```

这是一段标准的 HTML代码，复制到 `xx.html` 文件中，通过浏览器打开。可以看到三个复选框。


### 测试结果写入HTML模板

HTML代码和python代码混合在一起自然是方便维护的，利用jinja2可以方便的将HTML文件导入到python中使用。

目录结构：

```
├───templates
│   └───table.html
├───jinja2_demo.py
└───result.html
```

* 创建HTML表格

```html
<html>
<body>

<h1> case list: </h1>
<table border="1">
  <tr>
    <th>name</th>
    <th>doc</th>
  </tr>

  {% for item in cases %}
  <tr>
    <td>{{ item.name }}</td>
    <td>{{ item.doc }}</td>
  </tr>
  {% endfor %}

</table>

</body>
</html>
```

* 引入HTML模板

```py
from jinja2 import Environment, FileSystemLoader, select_autoescape

# 加载 templates 目录
env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape()
)
# 指定 table.html 文件
template = env.get_template("table.html")

# 准备写入数据
cases_list = [
    {"name": "test_pass", "doc": "pass case"},
    {"name": "test_skip", "doc": "skip case"},
    {"name": "test_fail", "doc": "fail case"},
    {"name": "test_error", "doc": "error case"}
]

tmp = template.render(cases=cases_list)

# 保存HTML结果
with open("./result.html", "w", encoding="utf-8") as f:
    f.write(tmp)

```

整个过程可以分为三步：

1. 导入 table.html 模板。
2. 将测试数据写入（填充）模板。
3. 将填充数据后的模板保存。

最终得到 `result.html` 文件

```html
<html>
<body>

<h1> case list: </h1>
<table border="1">
  <tr>
    <th>name</th>
    <th>doc</th>
  </tr>

  <tr>
    <td>test_pass</td>
    <td>pass case</td>
  </tr>  
  <tr>
    <td>test_skip</td>
    <td>skip case</td>
  </tr>
  <tr>
    <td>test_fail</td>
    <td>fail case</td>
  </tr>
  <tr>
    <td>test_error</td>
    <td>error case</td>
  </tr>
</table>

</body>
</html>
```
