from PyQt5.QtWidgets import QWidget
from recent_transactions.recenttransactions import RecentTransactions



class Recent_transactions(QWidget):
    def __init__(self,itemname,category,date,price,transaction_type):
        super().__init__()
        self.ui = RecentTransactions()
        self.ui.setupUi(self)

        self.ui.itemname.setText(itemname)
        self.ui.category.setText(category)
        self.ui.date.setText(date)
        if transaction_type == 'income':
            self.ui.price.setStyleSheet('color:rgb(0, 170, 0); font-size:12pt')
        self.ui.price.setText(f'₾{price}')