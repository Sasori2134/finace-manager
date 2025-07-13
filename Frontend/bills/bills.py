from PyQt5.QtWidgets import QWidget
from bills.bills_frame import BillsFrame


class Bills_Frame(QWidget):
    def __init__(self,category,price,date,item_data,remove_callback):
        super().__init__()
        self.ui = BillsFrame()
        self.ui.setupUi(self)

        self.ui.Day.setText(f"Day: {date}")
        self.ui.bills_label.setText(f"{category.capitalize()}")
        self.ui.price.setText(f"Amount: ₾{price}")
        
        self.item_data = item_data
        self.remove_callback = remove_callback

        self.ui.remove_bills.clicked.connect(self.handle_remove)

    def handle_remove(self):
        self.remove_callback(self.item_data['pk'], self)

