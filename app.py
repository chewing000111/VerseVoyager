from src.db import search
from nicegui import ui, events
from nicegui.binding import bind
from src.glm import first_step
from src import settings
from RainbowPrint import RainbowPrint as rp
import torch
import os

class Values(object):
    def __init__(self, init_data="./data/init_new.pt"):
        self.search_rtn = []
        self.search_tag = "查询/ 无"
        self.history = []
        self.history_data = {}
        if os.path.exists(init_data):
            init_data = torch.load(init_data)
            self.search_rtn = init_data["search_rtn"]
            self.search_tag = init_data["search_tag"]
            self.history = ["关于边塞战局的诗词"]
            self.history_data = {self.history[0]: init_data}


    def search(self, text):
        step_1 = first_step(text)
        self.search_tag = f"查询> {step_1}"
        self.search_rtn = search(step_1)
        search_data = {"search_rtn": self.search_rtn, "search_tag": self.search_tag}
        # torch.save(search_data,"./data/init_new.pt")
        self.history.insert(0, text)
        self.history = self.history[:10]
        self.history_data[text] = search_data
        self.history_data = {k: d for k, d in self.history_data.items() if k in self.history}

        search_result.refresh()
        ui.notify('检索完成', type='positive')

    def backtrack(self, text):
        search_data = self.history_data[text]
        self.search_rtn = search_data["search_rtn"]
        self.search_tag = search_data["search_tag"]
        search_result.refresh()
        ui.notify('加载历史记录:' + text, type='positive')

value = Values()

ui.query('body').classes('bg-fixed').style('background: url("https://www.tailwindcss.cn/_next/static/media/docs@30.8b9a76a2.avif")no-repeat;')

class BookValue(object):
    def __init__(self):
        self.expand = False

    @property
    def expand_neg(self):
        return not self.expand

def make_book(book):
    book_value = BookValue()
    def copy_click() -> None:
        # print(tabs.value)
        data = book
        paragraph_full = []
        for s in data["paragraph_full"]:
            paragraph_full.append(s['tr'] if tabs.value == "日" else s['s'])
        paragraph_full = '\n'.join(paragraph_full)
        copy_data = f"《{data['title_full']}》——{data['author']}({data['state']})\n{paragraph_full}"
        rp.debug("复制到剪切板\n" + copy_data)
        ui.run_javascript(f'clipboard(`{copy_data}`)')
        ui.notify('已写入剪切板', type='positive')
    with ui.item():
        ui.link_target(book["title_full"])

        ui.button(icon="content_copy", on_click=copy_click).props("round dense flat").classes(
            "absolute right-2 top-2 z-30 opacity-20 hover:opacity-80")

        with ui.row().classes("w-full gap-y-0.5 pt-2"):
            with ui.element('div').classes("w-full transition-all hover:scale-110"):
                ui.html(f"""
                《{book["title"]}》<span style="font-size:medium">——{book["author"]}</span><span class="text-gray-400 text-sm">({book["state"]})</span>
                """).classes("text-center text-indigo-5").style("font-size:x-large").bind_visibility_from(book_value, "expand_neg")
                ui.html(f"""
                《{book["title_full"]}》<span style="font-size:medium">——{book["author"]}</span><span class="text-gray-400 text-sm">({book["state"]})</span>
                """).classes("text-center text-indigo-5").style("font-size:x-large").bind_visibility_from(book_value, "expand")


            with ui.element('div').classes("w-full").style("margin-top: 10px; padding: 5px; margin-bottom: 10px;"):
                with ui.splitter(value=6).props(':limits="[6, 6]"').classes('w-full') as splitter:
                    with splitter.before:
                        with ui.tabs().props('vertical dense indicator-color="indigo-5"').classes('w-full') as tabs:
                            zh = ui.tab('中').classes('text-indigo-3')
                            tr = ui.tab('日').classes('text-indigo-3')
                    with splitter.after:
                        with ui.element('div').classes("w-full").style("background-color: #f6f8fa;") as show_div:
                            with ui.tab_panels(tabs, value=zh) \
                                    .props('vertical').classes('w-full h-full'):
                                with ui.tab_panel(zh).style("background-color: #f6f8fa;"):
                                    for paragraph in book["paragraph_full"]:
                                        _class = "w-full text-center transition-all hover:text-indigo-400" if paragraph["f"] else "w-full text-center text-gray-400 transition-all hover:text-indigo-400"
                                        l = ui.label(paragraph["s"]).classes(_class).style("font-size:large")
                                        if not paragraph["f"]:
                                            l.bind_visibility_from(book_value, "expand")

                                with ui.tab_panel(tr).style("background-color: #f6f8fa;"):
                                    for paragraph in book["paragraph_full"]:
                                        _class = "w-full text-center transition-all hover:text-indigo-400" if paragraph["f"] else "w-full text-center text-gray-400 transition-all hover:text-indigo-400"
                                        l = ui.label(paragraph["tr"]).classes(_class).style("font-size:large")
                                        if not paragraph["f"]:
                                            l.bind_visibility_from(book_value, "expand")

                            ui.tooltip('点击查看完整诗词，双击可以隐藏~').classes('bg-indigo-400').props('delay=1000 transition-show=rotate anchor="bottom middle" self="top middle"')
                            #
                            ui.label('点击查看完整诗词...').classes("w-full text-center text-gray-400").bind_visibility_from(book_value, "expand_neg")

        def show_div_click(plus=False):
            book_value.expand = book_value.expand_neg if plus else True

        show_div.on("click", lambda: show_div_click())
        show_div.on("dblclick", lambda: show_div_click(True))


def make_history_link(h_index, h_text):
    def history_select() -> None:
        input_search.value = h_text

    def history_select_plus() -> None:
        input_search.value = h_text
        value.backtrack(h_text)


    h_label = ui.label(f"{h_index+1}. "+h_text).classes("text-gray-600 hover:text-indigo-400")

    h_label.on("click", history_select)
    h_label.on("dblclick", history_select_plus)
    # ui.separator()

@ui.refreshable
def search_result():
    # 加载数据
    rows = []
    book_links = []
    for book in value.search_rtn:
        title= book["title"]
        if len(title)>13:
            title = title[:12]+"..."
        paragraph_full = [{"s":s,"tr":tr, "f": s in book["target_sentences"]} for s,tr in zip(book["paragraphs"], book["paragraphs_tr"])]
        rows.append({"title":title,"author":book["author"], "book_id":f'{book["title"]}|{book["author"]}',
                     "title_full":book["title"], "paragraph_full": paragraph_full,"state":book["state"]})
        book_links.append((title,book["title"]))

    # 模组1
    # with ui.element('div').classes('w-2/3 self-center px-4'):
    #     with ui.card().classes('w-full p-2'):
    #         ui.label(value.search_tag).classes("text-indigo-5")
    #         ui.tooltip('在搜索栏输入些什么吧~').classes('bg-indigo-400').props('delay=1000 transition-show=rotate anchor="bottom start" self="bottom right"')


    with ui.element('div').classes('w-2/3 self-center row'):
        # 主模块
        with ui.element('div').classes('w-3/4 px-4'):
            with ui.card().classes('w-full'):
                with ui.list().classes('w-full').props('dense separator'):
                    ui.item_label(value.search_tag).props('header').classes('text-bold text-indigo-5')
                    ui.separator()
                    for book in rows:
                        make_book(book)

        # 侧栏
        with ui.element('div').classes('w-1/4 px-4'):
            # 历史记录
            with ui.card().classes('w-full'):
                with ui.element('div').classes('w-full row'):
                    ui.element('span').style('display: inline-block;width: 8px;height: 18px;margin-right: 5px;background-color: #5c6bc0;position: absolute;left: 6px;')
                    ui.label("历史搜索").classes("text-indigo-5 text-bold").tooltip('双击直接跳转到该历史结果')
                    with ui.list().classes('w-full').props('separator'):
                        for h_index, h_text in enumerate(value.history):
                            make_history_link(h_index, h_text)

            # 跳转链接
            with ui.card().classes('w-full mt-4 gap-y-0.5'):
                with ui.element('div').classes('w-full row'):
                    ui.element('span').style('display: inline-block;width: 8px;height: 18px;margin-right: 5px;background-color: #5c6bc0;position: absolute;left: 6px;')
                    ui.label(" 跳转").classes("text-indigo-5 text-bold").tooltip('跳转至某首诗歌')
                for show,link in book_links:
                    ui.link(show,f"#{link}").classes("text-indigo-4 hover:-translate-x-2")

            # 简介
            with ui.card().classes('w-full mt-4'):
                with ui.element('div').classes('w-full row'):
                    ui.element('span').style('display: inline-block;width: 8px;height: 18px;margin-right: 5px;background-color: #5c6bc0;position: absolute;left: 6px;')
                    ui.label(" 简介").classes("text-indigo-5 text-bold")
                info = settings.info
                for s in info.split("\n"):
                    ui.label(s)
                ui.separator()
                ui.label("项目基于：")
                ui.link('[GUI]NiceGUI', 'https://github.com/zauberzeug/nicegui')
                ui.link('[向量数据库]faiss', 'https://github.com/facebookresearch/faiss')
                ui.link('[Bert]BERT-CCPoem', 'https://github.com/THUNLP-AIPoet/BERT-CCPoem')
                ui.link('[数据集]chinese-poetry', 'https://github.com/chinese-poetry/chinese-poetry')
                ui.link('[翻译]Kanbun-LM', 'https://github.com/nlp-waseda/Kanbun-LM')


    #
    # def history_select(e: events.GenericEventArguments) -> None:
    #     input_search.value = e.args["text"]
    #
    # def history_select_plus(e: events.GenericEventArguments) -> None:
    #     input_search.value = e.args["text"]
    #     value.backtrack(e.args["text"])


with ui.header(elevated=True).style('background-color: #fff9').classes('items-center justify-between backdrop-blur'):
    ui.label(' ')
    input_search = ui.input(None, placeholder="输入你想要查询的诗词") \
        .props('clearable dense standout="bg-indigo-2 text-indigo-9"') \
        .classes('w-[20rem] self-center w-1/2')

    def make_search_menu_item(t):
        def func_t():
            input_search.value = t
        ui.menu_item(t, func_t)

    with input_search.add_slot("append"):
        with ui.button(icon='menu').props("round dense flat").classes("text-indigo-5"):
            with ui.menu():
                for t in settings.suggest:
                    make_search_menu_item(t)
        def search_click():
            value.search(input_search.value)
        ui.button(icon="search", on_click=search_click).props("round dense flat").classes("text-indigo-5")

    with ui.element('div').classes("row transition-all hover:scale-110") as icon_:
        ui.icon("search").classes("text-4xl text-primary text-indigo-5")
        ui.label('梅宿莺').classes("text-2xl text-primary text-indigo-5")
        ui.tooltip('单击我回到顶端').classes('bg-indigo-400')

    def icon_click():
        ui.run_javascript(f'back_to_top();')

    icon_.on("click",icon_click)

search_result()

ui.add_body_html('''

<script>
  // 添加以下JavaScript代码
  // 当用户滚动一定距离时显示按钮
  back_to_top = function() {
    scrollToptimer = setInterval(function () {
            console.log("定时循环回到顶部")
            var top = document.body.scrollTop || document.documentElement.scrollTop;
            var speed = top / 4;
            if (document.body.scrollTop!=0) {
                document.body.scrollTop -= speed;
            }else {
                document.documentElement.scrollTop -= speed;
            }
            if (top == 0) {
                clearInterval(scrollToptimer);
            }
        }, 30); 
    
    
  };
  clipboard = function(text) {
        if (navigator.clipboard) {{
            navigator.clipboard.writeText(text)
        }}
        else {{
            console.error('Clipboard API is only available in secure contexts (HTTPS or localhost).')
        }}
  };

</script>
''')

ui.run(port=8083)




