# kæ语言：致力于使用人能看懂的纯中文进行编程

#### 介绍

kæ语言，一门用python实现的中文编程语言。致力于使用中国人容易理解的日常中文表达来进行编程。

「kæ」是福州话音译，意思是——傻、笨、蠢。顾名思义，它现在还很傻很笨，但我希望总有一天它会变得”聪明“起来，能和人类自由沟通。

#### 软件设计原则

这个语言绝对不会去涉及底层操作，不会变成完整的通用型语言，而且绝对不会有很复杂的东西，比如面向对象，闭包，复杂的嵌套。一切尽可能做到扁平化（因为自然语言表达很少有那么多层次的表达，太多层次人理解起来就很费劲）。

它的定位是面向应用的指令型语言，在特定场景下满足特定的用户。它的主要能力就是解析中文自然语义，然后转为底层封装好的能力去调用，仅此而已。

它的适用场景就是需要人通过自然语言交流指挥机器的场景（带一定的智能扩展），比如最常见就是很多科幻片里面的人和机器人交流的场景，xx精灵小x同学这种的智能家居智能穿戴产品，老人小孩病人康养陪伴的场景，指挥中心远程控制指挥的场景等，另外还比较适合于安装/烧写后很难再去动的嵌入式场景。

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

kæ有两种注释，一种是单行注释，一种是单句注释。单行注释就是在要注释的行前加【注】就行，那么本行【注】后面的所有内容都不执行。单句注释就是在不执行的句前加“开个玩笑哈~”，就可以不执行当前句。比如：

```
打开在当前目录的图像文件“lena.png”。将图片《lena.png》大小改为横：200，竖：100。【注】展示图像《lena.png》
开个玩笑哈~将图片《图像1》切割成多个矩形“切割矩形”。
```

##### 控制台打印

控制台打印是最简单的功能，也是个惯例了，凡是个编程语义就有一个打印Helloworld，即使它其他什么也干不了，它也算是一门编程语言了。如果它不能打印Helloworld，就算它能吃3碗干饭，可它还算什么编程语言呢？

我们的hello world是这样的：

```
在控制台打印： “你好，世界”。
```

结果是：

你好，世界

好了，已经能打印helloworld了，我们已经开山立派建立了一门编程语言，我们的任务完成了，我们的教程结束了！下班了！大家晚安，拜拜！~~

开玩笑的，别当真。下面继续。

我们说了，表达是多样的，打印还可以这样写：

```
在控制台打印：“你好世界”。
于控制台打印：“你好世界”。
使用控制台打印：“你好世界”。
打印：“你好世界”。
```

那个：（中文冒号，英文冒号都可以）是必须有的。后面中文的引号”“表示这是一个字符串。注意，是中文双引号，不支持单引号，不支持英文双引号，就这么牛逼！

如果要打印多个值，可以把所有的值都放到后面，用顿号（、）隔开。

```
在控制台打印：“你好”、“世界”、“！”。
```

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
打印："《"、《字典》的值、“》：”、《出版年份》的值、“版”。
```

使用变量要使用书名号（《》）把变量括起来，我本来是想用点复杂的标记（比如下划线波浪线之类），但是……输入太麻烦了。还要注意的是：要取变量的值，要跟“的值”两个字，预留着给对象的属性来使用的空间。

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

后续可以加载更多，比如excel等，然后给pandas解析。另外我的专业是GIS，我可能后面会把GIS格式加入进来。以及进行几何图形运算+matplotlib可视化。


##### 图片操作

比如可以这样打开图片：
```
打开在磁颐国工根省测试数据市lena室png间的图像文件“第一夫人”。
```
这样显示图片
```
展示图像《第一夫人》。
```
可以改变图片大小：
```
将图片《第一夫人》大小改为横：200，竖：100。
```
转换图片形式（二值、灰度、颜色索引、RGB、RGBA）
```
将图片《第一夫人》改为“二值图”模式。
```
然后保存
```
将图片《第一夫人》另存为：磁颐国输目省图像市第一夫人室jpg间。
```
也可以新建一张图片
```
新建一个空图像叫“图像1”，初始化为：模式为：“二值图”，大小为：横：600，竖：500。
```
在图片上画简单的图形：
```
新建一个空图像叫“图像1”，初始化为：模式为：“二值图”，大小为：横：600，竖：500。新建一个色刷名为“白色填充色”，初始化为白色。
从磁颐国工根省测试数据市点室yml间加载数据“多边形点集”。
在图像《图像1》上用色刷《白色填充色》绘制多边形图案《多边形点集》。【注】展示图像《图像1》。
将图片《图像1》另存为：磁颐国输目省图像市图像1室jpg间。
```
这里用上了刚才打开的yml文件，里面记录着点坐标数据。

##### 语音输出

现在支持语音输出了（需要安装pyttsx3）。要让程序说一段文字，就像这样：

```
语音说：“你好，世界！”
```

语音输出乘法口诀表的代码如下：

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

#### 安装教程

1. 安装python3
1. pip3 install pyyaml
2. 没有了

#### 使用说明

1. python ka.py 测试.k

#### 参与贡献

1. Fork 本仓库
2. 新建 Feat_xxx 分支
3. 提交代码
4. 新建 Pull Request
