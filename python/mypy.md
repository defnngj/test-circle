# Python类型检查工具Mypy

在过去的一年时间里，我使用Golang的时间大于Python，作为一个长期使用Python的人来说，最难受的莫过于对于复杂JSON/XML的处理，要定义复杂的结构体来解析。当我逐渐适应了Golang的类型系统后，发现了他的好处，Golang在运行的时候就帮我检查出了类型问题。

这会给我带来潜在的安全感，当我在发布Golang项目的时候，我对修改的代码充满信心，我认为我刚才的改动是可靠的，并且不会出什么差错。

然而，当我在发布 Python项目的时候，这种信心会明显不足，我不太确定刚刚的改动是否引入新的问题，或者是否漏掉了什么。以至于我需要多花一点时间来自测。

这种感觉非常明显，我并不会觉得当我成为Python高手的时候，就不会再犯一些低级的错误了。后来，意识到这种差异主要来源于类型系统，Python是动态语言，需要程序在运行过程中来检查类型。不过，在写Python的时候在程序中增加类型注解。从而让程序的可读性变得更好。


前几天同事强烈建议我使用 Mypy 来检查类型，于是我尝试了一下，发现还是挺好用的。

## Mypy 类型检查器

Mypy是Python的静态类型检查器。

类型检查器有助于确保您在代码中正确使用变量和函数。使用 Mypy 可以向你的Python程序添加类型提示(PEP 484)。 当错误的使用类型时， Mypy检查会发不告警。

Mypy拥有强大且易于使用的类型系统，支持类型推断、泛型、可调用类型、元组类型、联合类型、结构子类型等功能。 使用 Mypy 将使您的程序更易于理解、调试和维护。

* 安装

```bash
> pip install Mypy
```

* 测试代码：

```py
# demo.py
number = input("What is your favourite number?")
print("It is", number + 1)
```

* Mypy 检查


```bash
> mypy demo.py

demo.py:2: error: Unsupported operand types for + ("str" and "int")  [operator]
Found 1 error in 1 file (checked 1 source file)
```

其实很好理解，运行 `demo.py` 程序，用户通过`input` 任何字符都会作为字符串进行处理，而`number + 1` 需要类型一样才能相加。


## Pycharm 配置 Mypy

我们可以用 PyCharm 中配置 Mypy，这样就不需要通过 `Mypy` 命令检查了。

`File` ->  `Setting` ->  `Tools` ->  `External Tools`  添加配置：

![](./img/Mypy_setting.png)

* Program：`C:\Python311\\Scripts\Mypy.exe`
* Arguments：`$FilePath$`
* Working directory：`$FileDir$`


完成配置之后，可以有任何想要使用 Mypy 检查的文件中右键选择 Mypy 进行检查。

![](./img/Mypy_use.png)


## 总结


利用Mypy检查Python的类型并不会干扰程序的运行方式。我们可以将类型提示视为类似于注释！ 即使Mypy报告错误，仍然可以使用 Python解释器来运行代码。

Mypy的设计考虑到了渐进式打字。 这意味着你可以慢慢地将类型提示添加到代码库中，并且当静态类型不方便时，您始终可以回退到动态类型。

