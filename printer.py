class Document:
    def __init__(self, name, pages):
        name = name.strip()
        if not name:
            raise ValueError("Введите название документа.")
        if pages <= 0:
            raise ValueError("Количество страниц должно быть больше нуля.")

        self.name = name
        self.pages = pages

    def sheets_required(self):
        return self.pages


class DuplexDocument(Document):
    def sheets_required(self):
        return (self.pages + 1) // 2


class Printer:
    def __init__(self):
        self.paper = 10
        self.queue = []

    def add_document(self, document):
        self.queue.append(document)

    def add_paper(self, sheets):
        if sheets <= 0:
            raise ValueError("Количество листов должно быть больше нуля.")
        self.paper += sheets

    def print_next(self):
        if not self.queue:
            return "Очередь пуста. Сначала добавьте документ."

        document = self.queue[0]
        sheets = document.sheets_required()
        if sheets > self.paper:
            return f"Недостаточно бумаги: нужно {sheets}, есть {self.paper}."

        self.paper -= sheets
        self.queue.pop(0)
        return (
            f"Напечатан документ «{document.name}», страниц: {document.pages}, "
            f"израсходовано листов: {sheets}."
        )

    def cancel_document(self, index):
        document = self.queue.pop(index)
        return f"Документ «{document.name}» убран из очереди."
