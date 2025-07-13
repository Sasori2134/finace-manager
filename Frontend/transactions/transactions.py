from PyQt5.QtWidgets import QWidget
from transactions.transaction_frame import TransactionFrame



class Transaction_Frame(QWidget):
    def __init__(self,date,itemname,category,transaction_type,price,item_data,remove_callback):
        super().__init__()
        self.ui = TransactionFrame()
        self.ui.setupUi(self)

        self.ui.label.setText(itemname.capitalize())
        self.ui.category.setText(category.capitalize())
        if transaction_type == 'income':
            self.ui.price.setStyleSheet('color:rgb(0, 170, 0);font-size:15pt')
            self.ui.price.setText(f"₾{price}")
        else:
            self.ui.price.setStyleSheet('color:rgb(170, 0, 0);font-size:15pt')
            self.ui.price.setText(f"₾{price}")
        self.ui.date.setText(date)


        self.item_data = item_data
        self.remove_callback = remove_callback
        self.ui.transaction_remove.clicked.connect(self.handle_remove)

    def handle_remove(self):
        self.remove_callback(self.item_data['pk'], self)


