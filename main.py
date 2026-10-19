import flet as ft

from printer import Document, DuplexDocument, Printer


class PrinterApp:
    def __init__(self, page):
        self.page = page
        self.printer = Printer()

        page.title = "Симулятор принтера"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 24
        page.scroll = ft.ScrollMode.AUTO

        self.name_input = ft.TextField(label="Название документа")
        self.pages_input = ft.TextField(label="Количество страниц", value="1")
        self.duplex_input = ft.Checkbox(label="Двусторонняя печать", value=False)
        self.paper_input = ft.TextField(label="Сколько листов добавить", value="10")
        self.paper_text = ft.Text()
        self.queue_column = ft.Column(spacing=8)
        self.message = ft.Text("Добавьте первый документ.")

        self.refresh()
        page.add(
            ft.Column(
                width=620,
                spacing=16,
                controls=[
                    ft.Text("Симулятор принтера", size=26, weight=ft.FontWeight.BOLD),
                    self.paper_text,
                    self.name_input,
                    self.pages_input,
                    self.duplex_input,
                    ft.Button("Добавить в очередь", on_click=self.add_document),
                    ft.Divider(),
                    self.paper_input,
                    ft.Button("Пополнить бумагу", on_click=self.add_paper),
                    ft.Divider(),
                    ft.Text("Очередь печати", size=20),
                    self.queue_column,
                    ft.Button("Напечатать следующий", on_click=self.print_next),
                    self.message,
                ],
            )
        )

    def add_document(self, event):
        try:
            pages = int(self.pages_input.value or "")
        except ValueError:
            self.message.value = "Введите целое число страниц"
            self.page.update()
            return

        try:
            if self.duplex_input.value:
                document = DuplexDocument(self.name_input.value or "", pages)
            else:
                document = Document(self.name_input.value or "", pages)
        except ValueError as error:
            self.message.value = str(error)
            self.page.update()
            return

        self.printer.add_document(document)
        self.name_input.value = ""
        self.pages_input.value = "1"
        self.message.value = f"Документ «{document.name}» добавлен."

        self.refresh()
        self.page.update()

    def add_paper(self, event):
        try:
            sheets = int(self.paper_input.value or "")
        except ValueError:
            self.message.value = "Введите целое число листов"
            self.page.update()
            return

        try:
            self.printer.add_paper(sheets)
        except ValueError as error:
            self.message.value = str(error)
            self.page.update()
            return

        self.message.value = f"Добавлено листов: {sheets}."
        self.refresh()
        self.page.update()

    def print_next(self, event):
        self.message.value = self.printer.print_next()
        self.refresh()
        self.page.update()

    def cancel_document(self, event):
        index = event.control.data
        self.message.value = self.printer.cancel_document(index)
        self.refresh()
        self.page.update()

    def refresh(self):
        self.paper_text.value = f"Бумаги в принтере: {self.printer.paper} листов"
        self.queue_column.controls.clear()

        for index, document in enumerate(self.printer.queue):
            text = ft.Text(
                f"{index + 1}. {document.name} — {document.pages} стр., "
                f"листов: {document.sheets_required()}",
                expand=True,
            )
            cancel_button = ft.TextButton(
                "Отменить", data=index, on_click=self.cancel_document
            )
            row = ft.Row(controls=[text, cancel_button])
            self.queue_column.controls.append(row)

        if not self.printer.queue:
            self.queue_column.controls.append(ft.Text("Нет документов в очереди."))


def main(page):
    PrinterApp(page)


if __name__ == "__main__":
    ft.run(main)
