## 利用自动化找出试卷答案

事情是这样的，前两天一位同学咨询我一个问题：
![](img/topic_aswer_01.png)
![](img/topic_aswer_02.png)

通过上面的对话，至少确认他的目的不是为了`干坏事`或`作弊`！

思路我上面有说，接下来，我想自己动手做做。

## 实践过程

#### 第一步，查看页面结构

首先打开网站，看一下每道题的HTML结构。

```html

<div id="single_test" style="display: block;">
  <a name="name1"></a>
    <h2>一.单项选择题（共40题，每题1分）</h2>
    <div class="des">
      <p>1.Playfair密码是（）年由Charles Wheatstone提出来的。</p>
      <ul>
        <li><input name="1433" type="radio" value="A">&nbsp;A.1854</li>
        <li><input name="1433" type="radio" value="B">&nbsp;B.1855</li>
        <li><input name="1433" type="radio" value="C">&nbsp;C.1856</li>
        <li><input name="1433" type="radio" value="D">&nbsp;D.1853</li>
      </ul>
      <input type="hidden" id="1" value="A">
    </div>
    
    <div class="des">
      <p>2.PKI是（    ）的简称。 </p>
      <ul>
        <li><input name="1792" type="radio" value="A">&nbsp;A.Private Key Infrastructure</li>
        <li><input name="1792" type="radio" value="B">&nbsp;B.Public Key Infrastructure </li>
        <li><input name="1792" type="radio" value="C">&nbsp;C.Public Key Institute    </li>
        <li><input name="1792" type="radio" value="D">&nbsp;D.Private Key Institute </li>
      </ul>
      <input type="hidden" id="2" value="B">
    </div>
    ...

```

从HTML结构来看，定位起来并不复杂。

#### 第二步，定位元素

打开题目找出题目关键信息

* 找出所有的单选题目

```js
document.querySelectorAll("#single_test > div.des")
```

* 找出题目的名称

```js
document.querySelectorAll("#single_test > div.des > p")[0].textContent
```

* 找出A、B、C、D 选项

```js
document.querySelectorAll("#single_test > div.des > ul > li")[0].textContent
document.querySelectorAll("#single_test > div.des > ul > li:nth-child(2)")[0].textContent
document.querySelectorAll("#single_test > div.des > ul > li:nth-child(3)")[0].textContent
document.querySelectorAll("#single_test > div.des > ul > li:nth-child(4)")[0].textContent
```

* 然后再试试A、B、C、D 是否可点击

```js
document.querySelectorAll("#single_test > div.des > ul > li > input")[0].click()
document.querySelectorAll("#single_test > div.des > ul > li:nth-child(2) > input")[0].click()
document.querySelectorAll("#single_test > div.des > ul > li:nth-child(3) > input")[0].click()
document.querySelectorAll("#single_test > div.des > ul > li:nth-child(4) > input")[0].click()
```

![](img/topic_aswer_03.png)

#### 第三步：找出得分

3. 交卷查看得分

![](img/topic_aswer_04.png)

题目类型分三类：

* 单项选择题
* 多项选择题
* 判断题

通过操作得到以下结果：
1. 必须切换到`判断题`才能看到`交卷`按钮。
2. 所有答案可以不选，这样可以每道题单个试验。
3. 通过分数倒推答案是否正确。这一步很重要。

#### 第四步：实现代码

经过上面的试验，题目和答案定位都没问题，那么接下来通过selenium实现自动化。

```python
from time import sleep
from selenium import webdriver

dr = webdriver.Chrome()
dr.get("https://www.chinacodes.com.cn/exercises/gotoExercises.do")

# 所有题目
all_topic = dr.find_elements("css selector", "#single_test > div.des > p")
# 所有题目选项
all_option_a = dr.find_elements("css selector", "#single_test > div.des > ul > li")
all_option_b = dr.find_elements("css selector", "#single_test > div.des > ul > li:nth-child(2)")
all_option_c = dr.find_elements("css selector", "#single_test > div.des > ul > li:nth-child(3)")
all_option_d = dr.find_elements("css selector", "#single_test > div.des > ul > li:nth-child(4)")

# 所有题目选项的选中按钮
all_option_a_checked = dr.find_elements("css selector", "#single_test > div.des > ul > li > input")
all_option_b_checked = dr.find_elements("css selector", "#single_test > div.des > ul > li:nth-child(2) > input")
all_option_c_checked = dr.find_elements("css selector", "#single_test > div.des > ul > li:nth-child(3) > input")
all_option_d_checked = dr.find_elements("css selector", "#single_test > div.des > ul > li:nth-child(4) > input")

# 题目类型:
# 单选题按钮
single_select = dr.find_element("css selector", "#tab_bottom > li:nth-child(1)")
# 多选题按钮
more_select = dr.find_element("css selector", "#tab_bottom > li:nth-child(2)")
# 判断选题按钮
trueorfalse = dr.find_element("css selector", "#tab_bottom > li:nth-child(3)")

# 交卷按钮
exercise_submit = dr.find_element("css selector", "#exercise_submit > a")

# 总得分
number = 0


def get_answer(i):
    """
    获得一道题目的答案
    :return:
    """
    global number
    answer = 1
    answer_list = {1: "A", 2: "B", 3: "C", 4: "D"}
    for j in range(1, 5):
        answer = j
        option = dr.find_elements("css selector", f"#single_test > div.des > ul > li:nth-child({j}) > input")[i]
        option.click()
        trueorfalse.click()
        dr.execute_script("window.scrollTo(0, 10000);")
        exercise_submit.click()
        # 获得得分
        alert_text = dr.switch_to.alert.text
        result = alert_text.split("：")[1]
        n = int(result)
        if n > number:
            number = n
            dr.switch_to.alert.dismiss()
            single_select.click()
            break
        else:
            dr.switch_to.alert.dismiss()
            single_select.click()

    return answer_list[answer], number


# 循环 40 道单选题
for i in range(len(all_topic)):
    print("题目", all_topic[i].text)
    print("A:", all_option_a[i].text)
    print("B:", all_option_b[i].text)
    print("C:", all_option_c[i].text)
    print("B:", all_option_d[i].text)
    ret, num = get_answer(i)
    print("正确答案：", ret, "总分:", num)


sleep(2)
dr.quit()
```

__执行过程：__

1. 首先把题目和选项打印出来，方便查看。

2. 实现`get_answer()` 函数，把第`i`个题目给它。 

3. 每个题目有4个选项，循环4次，每次点击一个选项，然后查看结果。

4. 最关键一步：通过`number` 记录总分为`0`，当第一提做对时，总分为`1`，把`1` 赋值给`number`，当第一提做对时，总分为`2`，把`2` 赋值给`number`，依次类推。

> 这个执行过程与我微信回答有出入，我以为每个题目必须有要选一个选项，其实不用。


__执行结果__

```shell
题目 1.伪造、冒用、盗用他人的电子签名，给他人造成损失的，依法承担_____。（ ）
A:  A.刑事责任
B:  B.刑事和民事责任
C:  C.民事责任
B:  D.法事责任
正确答案： C 总分: 1
题目 2.签名者把他的签名权授给某个人，这个人代表原始签名者进行签名，这种签名称为（ ）。
A:  B.刑事和民事责任
B:  B.群签名
C:  C.多重签名
B:  D.盲签名
正确答案： A 总分: 2
题目 3.字母频率分析法对（）算法最有效。
A:  C.民事责任
B:  B.单表代换密码
C:  C.多表代换密码
B:  D.序列密码
正确答案： B 总分: 3
...
```


## 最后

这里只实现了单选题，还有多选题，每道题A、B、C、D 排列组合会有14种结果，最多需要14次才能找到正确答案。
```
A
B
C
D
AB
AC
AD
BC
BD
CD
ABC
ABD
BCD
ABCD
```

感兴趣，去试试吧！
