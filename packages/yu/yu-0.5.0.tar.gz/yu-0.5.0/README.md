# pYthon Utilities

安装

```
$ pip install yu
```

## extractors - 数据提取

数据提取，支持:

* Field
  * SkipField - 直接跳过
  * PassField - 不做转换
  * StringField - 字符串，支持长度验证
  * IntegerField - 整数，支持最大、最小值验证
  * FloatField - 浮点数
  * DateField - 日期
* RowExtractor
* CSVExtractor

### 示例

csv.extract 的用法:

```python
import csv
from yu.extractors import csv as ce


fields = [
    ce.StringField(min_length=2, max_length=4),  # 姓名
    ce.SkipField(),  # 民族
    ce.IntegerField(max_value=150),  # 年龄
    ce.FloatField(min_value=5, max_value=200),  # 体重
    ce.DateField(),  # 生日
    ce.PassField(),  # 备注
]


with open('data/person.csv') as fp:
    reader = csv.reader(fp)
    for row in ce.extract(reader, fields=fields):
        print(row)
```

### excel.extract 的用法

```python
import xlrd
from yu.extractors import excel as ee

fields = [
    ee.StringField(min_length=2, max_length=4),  # 姓名
    ee.SkipField(),  # 民族
    ee.IntegerField(max_value=150),  # 年龄
    ee.FloatField(min_value=5, max_value=200),  # 体重
    ee.DateField(),  # 生日
    ee.PassField(),  # 备注
]

book = xlrd.open_workbook('data/person.xlsx')
sheet = book.sheet_by_name('person')
for row in ee.extract(sheet, fields=fields):
    print(row)
```

## utils - 其他工具

包括

* cached_property - 代码来自 Django 项目
* InstanceMeta - 类的自动实例化
* Instance - 类的自动实例化（继承方式）

### InstanceMeta 示例

```python
from yu.utils import InstanceMeta

class Color(metaclass=InstanceMeta, abstract=True):
    def __str__(self):
        return f'{self.name} = {self.value}'

class Red(Color):
    name = 'red'
    value = 'FF0000'

class Green(Color):
    name = 'green'
    value = '00FF00'

print(Red)
print(Green)
```

## formula

用法：

```python
# 定义公式
try:
    面积公式 = Formula('面积 = 长 * 宽', '长方形面积')
except FormulaError as exc:
    print(exc)

# 进行计算
context = {
    '长': 16,
    '宽': 15,
}
try:
    面积公式(context)
except FormulaError as exc:
    print(exc)

# 读取结果
print(context['面积'])
```



## 修改记录

v0.5.0

* 2017-12-28 添加 yu.formula

v0.4.1

* 2017-12-20 完善 yu.extractors, 封装返回值

v0.4.0

* 2017-12-15 增加 argparseutils 模块，支持 DateType, DatetimeType

v0.2.2

* 2017-12-15 完善 extractors.excel 和 extractors.csv

v0.2.1

* 2017-12-11 发布里增加 README.md, data/*

v0.2.0

* 2017-12-10 添加 yu.extractors.excel，处理 Excel 文件的数据提取

v0.1.1

* 2017-12-09 添加 yu.extractors.csv, 处理 CSV 文件的数据提取
