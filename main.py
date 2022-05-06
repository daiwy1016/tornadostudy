import textwrap
import os.path
import random

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)


# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class Index2Handler(tornado.web.RequestHandler):
    def get(self):
        greeting = self.get_argument('greeting', 'hello')  # 获取请求参数为 greeting 默认值 hello
        self.write(greeting + ',friendly user!!1111')


class ReverseHandler(tornado.web.RequestHandler):
    def get(self, input):
        self.write(input[::-1])


class WrapHandler(tornado.web.RequestHandler):
    def post(self):
        text = self.get_argument('text')
        width = self.get_argument('width', 40)
        self.write(textwrap.fill(text, int(width)))


class PoemPageHandler(tornado.web.RequestHandler):
    def post(self):
        noun1 = self.get_argument('noun1')
        noun2 = self.get_argument('noun2')
        verb = self.get_argument('verb')
        noun3 = self.get_argument('noun3')
        self.render('poem.html', roads=noun1, wood=noun2, made=verb, difference=noun3)


class BookHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            'book.html',
            title='这是一个标题',
            header='books',
            books=[
                'learning python',
                '&二级C语言',
                '<restful web services>',
            ],
        )


class MungedPageHandler(tornado.web.RequestHandler):
    def map_by_first_letter(self, text):
        mapped = dict()
        for line in text.split('\r\n'):
            for word in [x for x in line.split(' ') if len(x) > 0]:
                if word[0] not in mapped:
                    mapped[word[0]] = []
                mapped[word[0]].append(word)
        return mapped

    def post(self):
        source_text = self.get_argument('source')
        text_to_change = self.get_argument('change')
        source_map = self.map_by_first_letter(source_text)
        change_lines = text_to_change.split('\r\n')
        self.render('munged.html', source_map=source_map, change_lines=change_lines, choice=random.choice)


class PoemIndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('munged_index.html')


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index2.html', header_text='这个是头部', footer_text='这个是底部')


class HelloModule(tornado.web.UIModule):
    def render(self):
        return '<h1>Hello, world!12121</h1>'

    # 插入到<body>的闭标签中
    def embedded_javascript(self):
        return 'document.write("Hi")'

    # 被直接添加到<head>的闭标签之前
    def embedded_css(self):
        return ".book {background-color:#F5F5F5}"

    # 闭合的</body>标签前添加完整的HTML标记
    def html_body(self):
        return "<script>document.write(\"Hello!\")</script>"

    def css_files(self):
        return '/static/css.css'

    def javascript_files(self):
        return 'https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.14/jquery-ui.min.js'


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[
        (r"/", IndexHandler),
        (r"/reverse/(\w+)", ReverseHandler),
        (r"/wrap", WrapHandler),
        (r"/poem2", PoemPageHandler),
        (r"/book", BookHandler),
        (r"/poem", MungedPageHandler),
        (r"/poem-index", PoemIndexPageHandler),
        (r"/main", MainHandler),
    ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), 'static'),
        debug=True,
        ui_modules={'Hello': HelloModule}
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
    print('ending')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
