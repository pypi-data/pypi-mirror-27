'''自定义公式

用法:

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
'''


class FormulaError(Exception):
    def __init__(self, exc):
        if isinstance(exc, SyntaxError):
            super().__init__(f'语法错误: {exc.filename}, 第 {exc.lineno} 行, 第 {exc.offset} 个字符')
        elif isinstance(exc, NameError):
            msg = exc.args[0] if exc.args else '?'
            if "'" in msg:
                name = msg.split("'")[1]
            else:
                name = msg
            super().__init__('名称未定义: {}'.format(name))
        else:
            super().__init__('错误: {}'.format(exc))


class Formula:
    # 内置函数，可以用在公式里面
    builtin_functions = {
        'MAX': max,
        'MIN': min,
    }

    def __init__(self, formula, name='<noname>'):
        self.name = name
        self.formula = formula

        try:
            self.compiled_formula = compile(formula, self.name, 'exec')
        except Exception as exc:
            raise FormulaError(exc)

    def __call__(self, context):
        globals = {'__builtins__': self.builtin_functions}
        try:
            eval(self.compiled_formula, globals, context)
        except Exception as exc:
            raise FormulaError(exc)
        return context

    def __str__(self):
        return self.name


if __name__ == '__main__':
    import sys

    # 定义公式
    try:
        面积公式 = Formula('面积 = 长 * 宽', '长方形面积')
    except FormulaError as exc:
        print(exc)
        sys.exit(1)

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
    print('面积 =', context['面积'])
    print(context)
