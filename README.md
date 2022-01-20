# kæ语言：致力于使用人能看懂的纯中文进行编程

#### 介绍

kæ语言，一门用python实现的中文编程语言。致力于使用中国人容易理解的日常中文表达来进行编程。

「kæ」是福州话音译，意思是——傻、笨、蠢。顾名思义，它现在还很傻很笨，但我希望总有一天它会变得”聪明“起来，能和人类自由沟通。

它的图标是一只看起来很呆萌的小猪。æ是它的两个鼻孔

![kaelogo](https://images.gitee.com/uploads/images/2021/1222/094720_99655753_4988273.jpeg "kaelogo.jpg")

不好意思，这是我手绘的，大家凑活看吧。

#### 软件设计原则

这个语言绝对不会去涉及底层操作，不会变成完整的通用型语言，而且绝对不会有很复杂的东西，比如面向对象，闭包，多层函数嵌套。一切尽可能做到扁平化（因为自然语言表达很少有那么多层次的表达，太多层次人理解起来就很费劲）。

它的定位是面向应用的指令型语言，在特定场景下满足特定的用户。它的主要能力就是解析中文自然语义，然后转为底层封装好的能力去调用，仅此而已。

它的适用场景就是需要人通过自然语言交流指挥机器的场景（带一定的智能扩展），比如最常见就是很多科幻片里面的人和机器人交流的场景，xx精灵小x同学这种的智能家居智能穿戴产品，老人小孩病人康养陪伴的场景，指挥中心远程控制指挥的场景等，另外还比较适合于安装/烧写后很难再去动而又想带一点智能或扩展性的嵌入式场景。

#### 软件架构

这个语言的实现架构非常简单粗暴：使用正则解析中文语法，然后转成底层实现语言(python)指令并执行。

—— 致敬那个用转C语言写编程语言的五年级小盆友

#### 语法说明

##### 语句

虽然我很喜欢python的强制缩进，但是对于中文，似乎对缩进没有非常严格的要求，甚至对于段落也没有非常严格的要求。所以，你可以把一段话一行表达完，也可以分行，只要跟中文一样，使用“。”来表示一个语句的结束就可以。比如：

```
定义一个空列表名为“一行”。在《一行》中插入：3、“X”、7、“=”、3与7求积、制表符、制表符、“！”。将列表《一行》拼接。打印：《一行拼接后》的值。
```

和

```
定义一个空列表名为“一行”。
在《一行》中插入：3、“X”、7、“=”、3与7求积、制表符、制表符、“！”。

将列表《一行》拼接。打印：《一行拼接后》的值。
```

是一样的（甚至中间有空行也没关系）。“段落”在这里没有太强的语义约束。你按论文标准写还是按诗标准写代码都是可以的。但是符号——逗号、句号、顿号、冒号、引号和书名号都有强烈的语义含义。

本来我想像word一样，用段落，首字空两格，后面想想，算了——word这玩意儿又不是开放式格式，用这种语法复杂程度太高了。没有编辑器支持写代码的人太痛苦了（我又不是JB，没空做IDE）。

另外中文语法同一个意思会有很多的表达，我也给每种指令做了很多别名，以适应不同的中文表达。具体接受的表达下面会有详细的说明。

###### 关于注释

kæ有两种注释，一种是单行注释，一种是单句注释。单行注释就是在要注释的行前加【注】就行，那么本行【注】后面的所有内容都不执行。单句注释就是在不执行的句前加“开个玩笑哈~”或者在句尾加上“……”（还是要以句号结尾），就可以不执行当前句。比如：

```
打开在当前目录的图像文件“lena.png”。将图片《lena.png》大小改为横：200，竖：100。【注】展示图像《lena.png》
开个玩笑哈~将图片《图像1》切割成多个矩形“切割矩形”。将图片《图像1》切割成多个矩形“切割矩形”……。
```

##### 你、我、他/她/它 （部分实现）

既然这个语言使用场景设计成人机交互场景，就必然会涉及以下的指令：

```
打开XXXX给我看看。
给我接通XXXX的电话。
我要听XXXXX。
你把温度调低一点。
请你把音量提高一些。
```

诸如此类。虽然“给我”这样的词从语义上非常鸡肋，但是口语话就是会这么说，所以从解析角度就应该去支持。

另外，现在这段语句现在看起来相当蛋疼。


```
访问在磁颐国工根省测试数据市第一夫人室png间的图像文件“第一夫人”。将图片《第一夫人》大小改为横200像素，竖100像素。
将图片《第一夫人》改为二值图模式。展示图像《第一夫人》。将图片《第一夫人》另存为：磁颐国输目省图像市第一夫人室jpg间。
```

要是能把变量名称用“它”或者“其”来替代，语句就会简化很多：

```
访问在磁颐国工根省测试数据市第一夫人室png间的图像文件“第一夫人”。将其大小改为横200像素，竖100像素。
将它改为二值图模式。展示它。最后把它另存为：磁颐国输目省图像市第一夫人室jpg间。
```

所以，我们需要定义指代对象。以便形成“上下文”并明确很多语义。我们就暂定：


- “我”用来表示正在交互的人。
- “你”用来表示正在交互的机器。
- “它/他/她/其”用来表示上一次存取的对象。


----

现在已经支持：

```
老子要你立马在终端打印： “你好，世界2”。请你用语音说出： “你好，世界”。
```

不仅支持了"我"和"你"，还支持了“老子”。因为我不确定机器的对面是不是李云龙。

##### 输出

###### 控制台打印

控制台打印是最简单的功能，也是个惯例了，凡是个编程语义就有一个打印Helloworld，即使它其他什么也干不了，它也算是一门编程语言了。如果它不能打印Helloworld，就算它能吃3碗干饭，可它还算什么编程语言呢？

我们的hello world是这样的：

```
在控制台打印： “你好，世界”。
```

结果是：

你好，世界

好了，已经能打印helloworld了，我们已经开山立派建立了一门编程语言，我们的任务完成了，我们的教程结束了！下班了！大家晚安，拜拜！~~

开玩笑的，别当真。下面继续。

我们说了，表达是多样的，终端输出还可以这样写：

```
在控制台打印：“你好世界”。
于控制台打印：“你好世界”。
使用控制台打印：“你好世界”。
终端说：“你好世界”。
打印：“你好世界”。
用终端输出：“你好世界”。
```

那个：（中文冒号，英文冒号都可以）是必须有的，主要是为了和普通的“说”格式统一。后面中文的引号“”表示这是一个字符串。注意，是中文双引号，不支持单引号，不支持英文双引号，就这么牛逼！

如果要打印多个值，可以把所有的值都放到后面，用顿号（、）隔开。

```
在控制台打印：“你好”、“世界”、“！”。
```

“控制台”也可以换成“终端”，效果是一样的。

###### 语音输出

除了控制台，也支持语音输出（需要安装pyttsx3）。要让程序说一段文字，就像这样：

```
语音说：“你好，世界！”
```

语法和控制台打印一样，只是把“终端|控制台”换成“语音”罢了。

举一个复杂的例子，语音输出乘法口诀表的代码如下：

```
【注】打印九九乘法表
语音说：“九九乘法表”。
定义一个循环子叫“行”，值为列表：1到9。定义一个循环子叫“列”，值为列表：1到9。
启动循环《行》，执行如下动作：
1）有一个空列表叫做“乘法表一行”。
2）在《乘法表一行》中插入：《行》当前值、“ ”。【注】如果开始是一个数字，语音以为它是序号，不会读
2）启动循环《列》，执行如下动作：
2.1）定义一个叫“乘积”的整数，值为《行》当前值 乘以 《列》当前值。
2.2）在《乘法表一行》中插入：《列》当前值、“ ”、《行》当前值、“，”。
2.2）判断：如果《乘积》的值比10小，就在《乘法表一行》中插入：“德”，否则在《乘法表一行》中插入：“ ”。
2.2）在《乘法表一行》中插入：《乘积》的值、“，，”。
3）将列表《乘法表一行》进行拼接。
4）语音说：《乘法表一行拼接后》的值。
打印：“结束”。
```
感兴趣的童鞋可以试试。

##### 变量

定义一个变量的语法灵感来自一段歌词：

```
村里有个姑娘叫小芳，长得好看又善良，一双美丽的大眼睛，辫子粗又长。
```

其实这一段很好得解释了怎么定义一个变量及变量属性定义（甚至还包含了属性定义和初始化）。定义变量可以使用以下语句定义：

```
有一个名为“出版年份”的整数，值为2008。
定义一个字符串叫“字典”，值为“新华字典”
```

也可以这样定义：

```
[新建|创建|定义|有]一个[整数|浮点数|字符串|数组][称作|称为|名为|叫]“变量名”，[值|初始化]为XXXX
[新建|创建|定义|有]一个[称作|称为|名为|叫]“变量名”的[整数|浮点数|字符串|数组]，[值|初始化]为XXXX
```

变量名要用中文引号“”括住，突出一下。

定义了变量，下面要使用时，用这样的语句来调用：

```
用控制台打印：《出版年份》的值。
打印：“《”、《字典》的值、“》：”、《出版年份》的值、“版”。
```

使用变量要使用书名号（《》）把变量括起来，我本来是想用点复杂的标记（比如下划线波浪线之类），但是……输入太麻烦了。还要注意的是：要取变量的值，要跟“的值”两个字，预留着给对象的属性来使用的空间。

##### 重命名

现在在对对象做操作时，如果产生新对象，会对新对象做一个自动重命名（一般会叫XX后）。比如：


```
将图像《第一夫人》进行左右翻转。展示图像《第一夫人翻转后》。
```

这种自动的重命名给人非常怪异的感觉，而且在很多时候，你不一定知道某个动作后产生的数据究竟叫什么。所以，需要有一个重命名机制，让你自己控制新产生的数据叫什么。


```
将《第一夫人》向左进行90度旋转，并将其重命名为第一夫人左转。
将《第一夫人》向右进行90度旋转。并将其重命名为第一夫人右旋。
将《第一夫人》向右进行180度旋转。并将其重命名为第一夫人倒立。
在图板上按照一排2张并排展示图片《第一夫人》、《第一夫人左转》、《第一夫人右旋》、《第一夫人倒立》。
```

“重命名”也可以用“重定义|重新定义|重新命名”来替换。


##### 判断

判断使用如下语法：

```
判断：[如果|如|若|如若|若是]条件1，[则|就|那么]动作1，[如果|如|若|如若|若是]条件2，[则|就|那么]动作2，... [否则|不然|不然就]else动作
```

举个栗子：

```
判断：如果《出版年份》的值比2005小，就打印：“老字典”，若《出版年份》的值比2010大，就打印：“新字典”，否则打印：“不新不旧版”。
```

开头的 判断： 必须写。如果... 就，这个就类似 if ... elif ...，可以不停重复。最后的否则，就是else。

###### 用问句做判断

上面的判断语句并不符合日常交流习惯。日常交流里的判断选择一般是这样的：


```
你冷吗？冷就再穿一件。
冷吗？要是冷就调节空调温度，把《空调1》的温度设置为28度。
冷吗？要是觉得冷就调节空调温度，把《空调1》的温度设置为28度。
冷吗？要是冷，就调节空调温度，把《空调1》的温度设置为28度。
```

这种表达其实就是一种True or False的选择，现已支持。


###### 另一个例子（未实现）


```
李云龙：你教会了一个班，我让你当班长；你教会了一个排， 我就让你当排长。 士兵甲：那我要教会一个连呢？ 李云龙：那你就领两块银元，趁早给我滚蛋！我最烦放空炮的兵！
```

这个我试着实现一下，并且试着把函数加上。


##### 循环

循环需要先定义一个循环子，然后基于这个循环子去循环。

比如这样可以定义一个循环子：

```
定义一个循环子叫“一星期”，值为列表：1到7。
```
然后基于这个循环子开启/执行这个循环：
```
启动循环《一星期》，运行打印：“星期”、《一星期》当前值。
```
循环结果如下：
```
星期 1
星期 2
星期 3
星期 4
星期 5
星期 6
星期 7
```
当然，这仅仅是一个最简单的循环，对于复杂循环，可能需要多行或者多语句的处理，有可能还会有多层嵌套。碰到多层嵌套的时候，语句会变得相当复杂。如何处理多层嵌套，又能让中文代码简单易懂？这个问题我想了好几天。最后在敲文档的时候有了灵感。

在word里面，经常会敲：

```
1. xxxx
2. XXXX
2.1 xxxxx
2.1.1 xxxxx
3. xxxx
```

这样的章节结构。当然，标号又有一大堆不同形式，比如(1)，[1]，1），第1章，一、这样的形式。这种形式可以嵌套，而且层级结构非常清晰。我原来想说设计成不同的
层级不同的标号形式，后面感觉太复杂了，所以仅仅采用了1）,1.1）这样的标号来进行层级定义。一个复杂的嵌套循环可以写成这样：

```
【注】打印九九乘法表
定义一个循环子叫“行”，值为列表：1到9。定义一个循环子叫“列”，值为列表：1到9。
启动循环《列》，执行如下动作：
1）定义一个空列表名为“乘法表一行”。
2）启动循环《行》，执行如下动作：
2.1）在《乘法表一行》中插入：《行》当前值、“X”、《列》当前值、“=”、《行》当前值乘《列》当前值、制表符。
3）将列表《乘法表一行》进行拼接。
4）打印：《乘法表一行拼接后》的值。
```
需要注意的是：要开启一个新的代码段，需要在开启的一行的最后要这么写：

```
[如下|以下][动作|操作]：
```

很像python的:号。在标号里定义层级，和缩进很像。这很有python缩进的感觉。

后来我意识到：用标号，如果没有IDE的支持，很容易陷入“标号更改地狱”，也就是说，一旦调整结构，标号数字调整会非常痛苦。所以，我决定像markdown一样，让标号的数字不重要，只有标号分割的级别（.）是重要的，也就是说，先写2，再写1，还是全写1，都是没有问题的。

最后看下乘法表的输出结果：

```
1X1=1   2X1=2   3X1=3   4X1=4   5X1=5   6X1=6   7X1=7   8X1=8   9X1=9
1X2=2   2X2=4   3X2=6   4X2=8   5X2=10  6X2=12  7X2=14  8X2=16  9X2=18
1X3=3   2X3=6   3X3=9   4X3=12  5X3=15  6X3=18  7X3=21  8X3=24  9X3=27
1X4=4   2X4=8   3X4=12  4X4=16  5X4=20  6X4=24  7X4=28  8X4=32  9X4=36
1X5=5   2X5=10  3X5=15  4X5=20  5X5=25  6X5=30  7X5=35  8X5=40  9X5=45
1X6=6   2X6=12  3X6=18  4X6=24  5X6=30  6X6=36  7X6=42  8X6=48  9X6=54
1X7=7   2X7=14  3X7=21  4X7=28  5X7=35  6X7=42  7X7=49  8X7=56  9X7=63
1X8=8   2X8=16  3X8=24  4X8=32  5X8=40  6X8=48  7X8=56  8X8=64  9X8=72
1X9=9   2X9=18  3X9=27  4X9=36  5X9=45  6X9=54  7X9=63  8X9=72  9X9=81
```

完美！

###### 直到……时为止的循环

上面是普通的for循环，一般语言里面还会有while循环，现在同样支持。下面是一个简单的例子：

```
有一个名为“循环数”的整数，值为1。
对《循环数》执行自增，直到《循环数》的值等于100时为止。
打印：《循环数》的值。
```

语法很简单，就是`……（循环里要做的事），直到……（循环终止条件）时为止`。

###### 递归

现在甚至支持了递归。为了实验递归，我做了一个快速排序的例子(功能单元/快速排序法.ae)：

```
监听对象“序列”。
选择《序列》中第1个元素作为基准数。
抽取《序列》中小于《基准数》的值的元素组成“左区数组”。
抽取《序列》中等于《基准数》的值的元素组成“中区数组”。
抽取《序列》中大于《基准数》的值的元素组成“右区数组”。
清空《序列》。在《序列》中插入：《左区数组》的值、《中区数组》的值、《右区数组》的值。
判断：如果《左区数组》的长度大于1，则对《左区数组》执行快速排序法。
判断：如果《右区数组》的长度大于1，则对《右区数组》执行快速排序法。
```

这里`对《左区数组》执行快速排序法`和功能单元的名字相同，于是就形成了递归。总的调用如下：

```
有一个空列表叫做“序列1”。在《序列1》中插入：11、15、3、26、7、12、33、9。
怎样快速排序呢？由《快速排序法》来说明。
对《序列1》执行快速排序。将《序列1》进行一维化，并将其重命名为续后1。打印：《续后1》的值
```

最终也能得到正确的结果。

```
[11, 15, 3, 26, 7, 12, 33, 9]
[3, 7, 9, 11, 12, 15, 26, 33]
```

虽然我不是用数据交换这样的方式而是用抽取数据形成新数组的方式，但原理还是分区分治法。这种做法可能有人会诟病效率问题或者一定要求按照数据交换的方式来做，会说这样不涉及底层能力的不是编程语言。但是，你看，Python底层也会调用c库，不妨碍它作为编程语言而存在。永远记住：

> 正常情况下，我们不建议把功能单元写得非常复杂，建议把该底层的事情让底层语言或库去做，而我们只要管上层组织调用就行了。

##### 列表

可以定义一个空列表，往里面追加内容，然后拼接起来，输出拼接结果：
```
定义一个空列表名为“一行”。在《一行》中插入：3、“X”、7、“=”、3与7求积、制表符、制表符、“！”。将列表《一行》拼接。打印：《一行拼接后》的值。
```
输出：
```
3X7=21          ！
```
现在可以支持排序和倒排了：
```
定义一个空列表名为“另一行”。
在《另一行》中插入：3、7、12、33、9。
将列表《另一行》进行排序。
打印：《另一行》的值。
将列表《另一行》从大到小进行排序。
打印：《另一行》的值。
```
输出
```
[3, 7, 9, 12, 33]

[33, 12, 9, 7, 3]
```
##### 路径和url表达

```
从“d:/test/point.yml”加载yaml文件“多边形点集”。
将图片《图像1》另存为：“d:/output/图像数据输出/图像1.jpg”。
```

这样路径表达很让我很蛋疼：如果是按其他语言一样，用操作系统路径来表示路径，跟中文编程整体感觉格格不入，非常违和；且后续如果要接语音，用真实路径表达起路径来，令我想起我国防部发言人在发布会上一个字母一个字母念网友网名的尴尬。另外，不单纯文件路径，共享文件夹、网络URL也是一种路径，表达起来同样很尴尬。需要有一种表达方式能方便中文表达路径，又能方便语言访问。

有没有不违和地表示路径的方法呢？有！其实我们在编程的时候，太依赖操作系统了，文件路径难道就必须用操作系统的文件路径吗？我是GIS专业的，GIS给了我灵感，我做着地名地址解析，突然灵机一动——为什么不能用地名地址来表示路径（包括本地文件路径，共享文件夹和网络URL）呢？一个路径，我们用工具将其转为中文地址表达不就行了？比如d:/数据/几何数据/点数据.yml，可以转换成XX国XX省XX市XX区XX路XX号，这样就能非常亲切得访问文件路径了。为了区分和正经地名地址的区别，我们需要把国名换成完全不存在的国名（最好和镜花缘、山海经也不重名，带一点玄幻色彩），比如本地文件，我们叫“磁颐国”（颐取自六十四卦，表示磁是硅（山）和电（雷）的碰撞叠加）；如果是远程url，我们叫它“星辰国”好了；共享文件夹？叫他“睦邻国”好了。然后省、市、县、乡、村、路、号、楼、室按照路径结构继续往下编。有人说了：操作系统里那么多文件一一做对应，不累吗？其实我们不需要对整个操作系统文件做对应。ArcGIS在ArcCatalog里管数据的方式给了我启发，它在启动的时候是需要挂载数据目录才能在软件里认到，不是操作系统里所有的目录都能认，要添加数据目录（包括数据库、共享文件夹、远程数据服务url）需要手动添加。所以，在语言层面，我也设计了一个语言启动后加载的路径对应文件“urlmap.yml”，里面定义的是各个名字和根目录，结构是：

```
磁颐国 :
 工根省: .
 输目省: d:/output
星辰国 :
 百度省: https://www.baidu.com
睦邻国 :
```
其中“工根省”表示工作目录的根，一般都都是有的，“输目省”表示输出目录的根。为什么起这么土的名字？别问，问就起名无力症。至于“星辰国百度省”大家应该一看就明白。后面大家还需要挂载什么目录，手动改这个文件就好了，自己命名，并添加文件夹对应关系就行。其实**在我们日常编程中，很少使用磁盘所有的文件，真正使用时仅仅只是挑选几个读写罢了**。

定义好根目录（省），下面就按照目录里的层级一级一级下去吧。市、县、乡、村、路、号、楼、室、间，按照路径结构继续往下编，最多支持到7级目录。为什么是7级？为了区分目录和文件，需要把文件级别直接设定到“室”，甚至扩展名最好也拆开，命名到“间”，比如：d:/output/图像数据输出/图像1.jpg，可以转化为：磁颐国输目省图像数据输出市图像1室jpg间。然后读写文件就可以这样写：

```
访问磁颐国工根省测试数据市点室yml间，加载数据为“多边形点集”。
将图片《图像1》另存为：磁颐国输目省图像数据输出市图像1室jpg间。
```
感觉这样就符合日常习惯了。将来如果接入语言识别和语音播报，也会显得人性化很多。

> 如果下一代国产操作系统把文件系统改为地址系统，我觉得它就真的像一个给中国人用的操作系统了。

##### 文件操作

可以支持加载yaml和json文件。

```
从磁颐国工根省测试数据市点室yml间加载数据“多边形点集”。
```

这两种格式都是将数据读取进来并直接转为对象。后续可以加载更多，比如excel等，然后给pandas解析。另外我的专业是GIS，我可能后面会把GIS格式加入进来。以及进行几何图形运算+matplotlib可视化。


##### 面向“东西”的编程

###### 什么是面向“东西”

我说过Kæ不做“面向对象”的编程，但我没有说过Kæ不做面向“对象”的编程。其实所有自然语言里描述和操作的就是一个个对象，所以对“对象”的操作是核心，面向“对象”的能力是无法撇弃的。但是我这里的面向对象仅仅是面向对象个体，也就是说我不会去实现面向对象编程的三大特征：封装、继承、多态。这里的面向“对象”的编程，是把数据（字典）作为一个个对象进行操作，仅此而已。数据内也不定义方法，所有操作都在外部定义。为了和“面向对象”编程区别开来，我们可以把它叫做“面向东西”的编程。

首先我们要知道，我们所有的“东西”都是一个个个体。对应到程序里就是一个个数据对象。这个数据对象和Json的对象、yaml的对象、Python的字典是一个概念。它只是数据的概念，和程序里的对象是不一样的，因为我们不定义方法。对“东西”的操作只包含了数据的读写（后面可能会加更多的东西，但我还没有想好）。

###### 构建“东西”

任何一个“东西”都不是凭空从石头里蹦出来的。要想操作某个东西，首先先要有这个“东西”。所以首先需要构建出“东西”来。

1. 别人的东西

   像我们操作的图像、表格、画板等，是从已经存在库里构建的。是通过各种Open、new或者Create搞出来的。这种“东西”可以通过下面这种方式构建：


   ```
   新建一个空图像叫“图像1”，类型为二值图，大小为横600像素竖500像素。
   打开在磁颐国工根省测试数据市历年人口密度统计室xls间的表格文件，命名为“人口”。
   创建一个模式为正整形、大小为5行3列的全1矩阵叫“矩阵1”。
   ```

   这里的图像、表格、矩阵，都是一种“东西”的种类。随着我们对接的库越来越多，“东西”的类型也会越来越多。它们的本质就是Image、DataFrame、narray对象。我们也需要对这些对象的方法做一一对接，变成中文的动作语句，然后进而操作它们。

1. 自己的东西

   世界上不可能都有现成的东西。有的时候可能不得不自己造一个。所以不能只有别人的东西，也要有自己的东西。

   > 这个语言，它和利用现成语言建立的功能库最大的区别在于，他能建立自己的东西，能用自己的语言来描述自己的东西，所以它是一门语言，而不仅仅是一个功能库封装。

   它建立自己的东西最简洁的方式就是加载一个现成的对象（比如Json对象或者yaml对象或者XML对象，Python对象或者字典序列化后也可以，形式后面可以加）。

   ```
   从磁颐国工根省测试数据市点室yml间加载数据“多边形点集”。
   ```

   yml数据一旦读入，就是对象了（JSON对象也如此）。本质就是Python字典，直接可以使用。但是这里面临一些问题，比如大多json对象都是英文的属性名称，比如温度，一般数据里都是temperature，如果你要获取它的值，就得这样写：


   ```
   把《卧室空调》的temperature设置为28度。
   打印：《卧室空调》的temperature。
   ```

   久而久之就会形成这样的语言： `这个project的schedule有些问题，尤其是buffer不多。另外，cost也偏高。目前我们没法confirm手上的 resource能完全take得了。Anyway我们还是先pilot一下，再follow up最终的output，看能不能run的比较smoothly，更重要的是evaluate所有的cost能不能完全被cover掉……`

   我觉得kæ要是变成这种语言，还不如换关键字呢。

   所以如何让中英混杂文平滑过渡到中文日常正常的表达。我想了一个方法，就是做个数据属性中英文对照表。建立一个空调对象描述.yml文件，内容是：


   ```
   温度: temperature
   ```

   然后将其来解释某个空调数据。


   ```
   访问磁颐国工根省数据描述市空调对象描述室yml间，加载数据为“空调对象描述”。以《空调对象描述》来描述《卧室空调》。
   ```

   之后，那句蹩脚的中文就会变得丝滑：

   ```
   把《卧室空调》的温度设置为28度。
   打印：《卧室空调》的温度。
   ```

   当然用 `磁颐国` `数据描述市` 来表述描述文件的路径，大家还不是很习惯（习惯其实还好）。所以有更简洁的方式，如果这个文件在工作目录下的数据描述目录下，可以直接写：


   ```
   加载数据描述“空调对象描述”。以《空调对象描述》来描述《卧室空调》。
   ```

   这样就简单多了。

###### 通过描述文件新建东西

描述文件可以做对象的中英文属性对照，但它的作用不仅如此，它同样也能做数据结构描述，至少它能说明这种东西有哪些属性（和类声明已经有些相似了）。比如我们依照空调描述对象创建出一个空调对象，可以这样写：


```
加载数据描述“空调对象描述”。依照《空调对象描述》构建“空调1”。
```

然后就可以去读写“空调1”这个东西的属性了。

##### 功能单元

一个功能单元其实就是一个函数，把它看成是函数复用就行了。但是因为中文的习惯和函数定义和调用不太一样，所以语法上也有很大的区别。

###### 定义一个功能单元并调用

比如我们把获取当前温度的功能变成功能单元。在工程目录的“功能单元”目录下新建一个文件“获取当前温度.ae”，把代码黏贴到其中。

```
访问位于星辰国位处省查询室文本间的数据“当前所处城市文本”。解析《当前所处城市文本》中的对象“当前城市对象”。访问磁颐国工根省数据描述市当处城对象描述室yml间，加载数据为“城市对象描述”。以《城市对象描述》来描述《当前城市对象》。

访问位于星辰国城码省查询室json间的数据“当前所处省编码表”。
访问磁颐国工根省数据描述市省编码描述室yml间，加载数据为“省编码描述”。以《省编码描述》来描述《当前所处省编码表》。
查找《当前所处省编码表》中“名称”和《当前城市对象》的“城市名称”前半段相同的首条记录，并将其重命名为当前省。将《当前省》的编码命名为当前省之编码。

访问位于星辰国城码省当前省之编码市查询室json间的数据“当前市编码表”。
访问磁颐国工根省数据描述市市编码描述室yml间，加载数据为“市编码描述”。以《市编码描述》来描述《当前市编码表》。
查找《当前市编码表》中“名称”和《当前城市对象》的“城市名称”有包含关系的首条记录，并将其重命名为当前市。

访问磁颐国工根省数据描述市天气请求参数室yml间，加载数据为“天气请求参数描述”。
依照《天气请求参数描述》构建天气请求参数。设置《天气请求参数》的编码为《当前市》的编码。
带着《天气请求参数》访问位于星辰国天气省查询室json间的数据“当前市天气”。
访问磁颐国工根省数据描述市天气对象描述室yml间，加载数据为“天气对象描述”。以《天气对象描述》来描述《当前市天气》。

打印：“当前的气温”、《当前市天气》的气温、“度”。
```

这样就完成了对一个功能单元的定义。如何调用，在调用的文件里先申明：


```
怎样获取当前温度呢？让《获取当前温度》来解答。
```

首先提出疑问`怎样获取当前温度呢？`（“怎样”和“呢”之间的内容说明了功能调用的语法）后面可以使用`获取当前温度`来进行功能的调用。`让《获取当前温度》来解答`这句类似import，也就是类似`import 获取当前温度.ae`。书名号里就是模块文件的主文件名。这两句组合起来，就类似 import XXX as xxx 的效果。

定义好功能怎么调用呢？根据疑问内容，去掉“怎样”和“呢”。就是调用的语句。

```
获取当前温度。
```

这样就能调用了。


###### 功能返回值

上面的功能是没有返回的，如果需要返回，需要在模块里面做返回。修改“获取当前温度.ae”，添加一行：


```
获取当前温度结果即为《当前市天气》的气温。
```

`获取当前温度`是功能单元名字，“结果即为”后面就是要返回的值。那么返回的值外面怎么获取呢？


```
获取当前温度，并将其重定义为当前气温。打印：“当前气温”、《当前气温》的值、“摄氏度”。
```

重命名一下就好了。

###### 传递参数

大多数时候都需要进行参数的传递，那么传递参数要怎么写呢？比如有一个“空调遥控.ae”的功能单元

```
监听对象“空调”。
打印：“滴，空调已经设置到”、《空调》的温度、“度”
```

`监听对象“空调”`就是申明了一个参数（形参）。表示外面传入的数据在这里面叫做“空调”，里面可以对这个值进行读写，读写操作会影响到外面的实参的值。下面是怎么使用参数传递的例子：

```
加载数据描述“空调对象描述”。依照《空调对象描述》构建空调1。
怎样调节空调温度呢？由《空调遥控》来说明。调节空调温度，把《空调1》的温度设置为28度。
```

`加载数据描述“空调对象描述”。依照《空调对象描述》构建空调1。`是构建出数据对象（作为实参）。`怎样调节空调温度呢？由《空调遥控》来说明。`这是import操作。`调节空调温度`，是进行功能调用，`把《空调1》的温度设置为28度`是把“空调1”的温度设置为28度并作为实参传入给形参“空调”，内部操作对象的“温度”对象，能读取外部给定的温度数值。一句话：功能单元的内外共享同一个变量来达到参数传递的目的。

###### 功能单元嵌套

功能单元是可以嵌套的，也就是一个功能单元可以调用另外一个功能单元。比如这个冷不冷的例子，建立一个叫“冷不冷.ae”的功能单元，代码如下：

```
怎样获取当前温度呢？让《获取当前温度》来解答。
获取当前温度，并将其重定义为当前气温。
判断：如果《当前气温》的值小于20，则冷不冷结果即为是，否则冷不冷结果即为否。
```

这里调用了“获取当前温度”的功能单元。根据从网络爬取的当前气温来判断冷不冷。

在运行脚本里面调用冷不冷的代码如下：

```
怎样判断冷呢？由《冷不冷》来说明。
你冷吗？冷就调节空调温度，把《空调1》的温度设置为26度。
```

这里需要说明的一点，对于`判断冷`这样的表述，功能模块返回的只有真（True）和假（False），使用功能（调用）的时候，可以省略“判断”两个字。


#### 功能库

##### 1. [图片操作](https://gitee.com/linux_23/kaelang/wikis/%E5%8A%9F%E8%83%BD%E5%BA%93%E8%AF%B4%E6%98%8E/%E5%9B%BE%E7%89%87%E6%93%8D%E4%BD%9C)
##### 2. [图像处理](https://gitee.com/linux_23/kaelang/wikis/%E5%8A%9F%E8%83%BD%E5%BA%93%E8%AF%B4%E6%98%8E/%E5%9B%BE%E5%83%8F%E5%A4%84%E7%90%86)
##### 3. [绘制图表](https://gitee.com/linux_23/kaelang/wikis/%E5%8A%9F%E8%83%BD%E5%BA%93%E8%AF%B4%E6%98%8E/%E7%BB%98%E5%88%B6%E5%9B%BE%E8%A1%A8)
##### 4. [表格操作](https://gitee.com/linux_23/kaelang/wikis/%E5%8A%9F%E8%83%BD%E5%BA%93%E8%AF%B4%E6%98%8E/%E8%A1%A8%E6%A0%BC%E6%93%8D%E4%BD%9C)
##### 5. [网络请求](https://gitee.com/linux_23/kaelang/wikis/%E5%8A%9F%E8%83%BD%E5%BA%93%E8%AF%B4%E6%98%8E/%E7%BD%91%E7%BB%9C%E8%AF%B7%E6%B1%82)


更多的语言细节请看[维基页面](https://gitee.com/linux_23/kaelang/wikis/pages) 。



#### 安装教程

1. 安装python3
1. pip3 install -r requirements.txt 
2. 没有了

#### 使用说明

1. python ka.py 测试.ae

#### 交互式控制台

现在有一个交互式控制台来使用了。

运行


```
python dv.py
```

<img src=https://images.gitee.com/uploads/images/2022/0110/182537_58b0df9f_4988273.png width=80%>

这个控制台的界面风格参考了Jupyter Notebook，可以进行交互式输入输出了。

#### 参与贡献

1. Fork 本仓库
2. 新建 Feat_xxx 分支
3. 提交代码
4. 新建 Pull Request
