from PyQt5.QtWidgets import QMainWindow
from final import Ui_MainWindow
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from final import Ui_MainWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from recent_transactions.recent_transactions_widget import Recent_transactions
from PyQt5.QtCore import Qt
from budget.budget import Budget
from bills.bills import Bills_Frame
from transactions.transactions import Transaction_Frame
from more_button import MoreButton

class main_window(QMainWindow):
    def __init__(self, user):
        global expense_categories
        expense_categories = [
        "Rent",
        "Utilities",
        "Groceries",
        "Transportation",
        "Fuel",
        "Internet",
        "Phone Bill",
        "Insurance",
        "Medical",
        "Dining Out",
        "Clothing",
        "Entertainment",
        "Subscriptions",
        "Education",
        "Childcare",
        "Household Items",
        "Travel",
        "Gifts & Donations",
        "Personal Care",
        "Pets",
        "Loans",
        "Credit Card Payments",
        "Taxes",
        "Miscellaneous"
        ]
        global income_categories
        income_categories = [
        "Salary",
        "Bonus",
        "Freelance",
        "Business",
        "Investment Income",
        "Rental Income",
        "Dividends",
        "Interest Income",
        "Capital Gains",
        "Pension",
        "Social Security",
        "Government Assistance",
        "Child Support",
        "Alimony",
        "Gifts Received",
        "Selling Items",
        "Royalties",
        ]
        global All
        All = expense_categories + income_categories


        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('./newlogo.png'))
        self.user = user
        self.ui.tabWidget.currentChanged.connect(self.on_tab_change)
        self.ui.add_budget.clicked.connect(self.add_budget)
        self.more_button = MoreButton()
        self.button_widget = QWidget()
        self.button_widget_layout = QVBoxLayout(self.button_widget)
        self.button_widget_layout.setSpacing = 0
        self.button_widget_layout.addWidget(self.more_button,alignment=Qt.AlignHCenter)
        if self.ui.tabWidget.currentIndex() == 2:
            self.on_tab_change(self.ui.tabWidget.currentIndex(), self.ui.tabWidget_2.currentIndex())
        else:
            self.on_tab_change(self.ui.tabWidget.currentIndex())
        self.ui.days.currentTextChanged.connect(self.analytics)
        self.ui.transaction_filter_button.clicked.connect(self.fetch_transaction)
        self.ui.transaction_add_button.clicked.connect(self.add_transaction)
        self.ui.log_out.clicked.connect(self.log_out)
        self.ui.add_bill.clicked.connect(self.add_bills)
        self.ui.budget_category.clear()
        self.ui.budget_category.addItem('Select category')
        self.ui.budget_category.addItems(expense_categories)
        self.ui.transaction_add_category.clear()
        self.ui.transaction_category.clear()
        self.ui.transaction_add_category.addItem('Select category ')
        self.ui.transaction_add_type.currentTextChanged.connect(self.change_category_transactions)
        self.ui.transaction_type.currentTextChanged.connect(self.change_filter_transaction_category)
        self.ui.transaction_add_type.setCurrentText('Income')
        self.ui.transaction_type.setCurrentText('All')
        self.ui.category_bills.clear()
        self.ui.category_bills.addItem('Select category ')
        self.ui.category_bills.addItems(expense_categories)
        self.change_filter_transaction_category()
        self.change_category_transactions()
        self.more_button.clicked.connect(self.fetch_transaction)
        



    def change_filter_transaction_category(self):
        chosen = self.ui.transaction_type.currentText()

        if chosen == "All":
            self.ui.transaction_category.clear()
            self.ui.transaction_category.addItem("Select category ")
            self.ui.transaction_category.addItems(All)
        if chosen == "Expense":
            self.ui.transaction_category.clear()
            self.ui.transaction_category.addItem("Select category ")
            self.ui.transaction_category.addItems(expense_categories)
        if chosen == "Income":
            self.ui.transaction_category.clear()
            self.ui.transaction_category.addItem("Select category ")
            self.ui.transaction_category.addItems(income_categories)


    def change_category_transactions(self):
        chosen = self.ui.transaction_add_type.currentText()

        if chosen == 'Expense':
            self.ui.transaction_add_category.clear()
            self.ui.transaction_add_category.addItem('Select category ')
            self.ui.transaction_add_category.addItems(expense_categories)
        elif chosen == 'Income':
            self.ui.transaction_add_category.clear()
            self.ui.transaction_add_category.addItem('Select category ')
            self.ui.transaction_add_category.addItems(income_categories)

    def dashboard(self):
        dashboard_data = self.user.dashboard()
        self.ui.total_income.setText(f"₾{dashboard_data['total_stats']['total_income']}")
        if dashboard_data['total_stats']['balance'] < 0:
            self.ui.balance.setStyleSheet("color:rgb(170, 0, 0);font-size:15pt")
            self.ui.balance.setText(f"₾{dashboard_data['total_stats']['balance']}")
        else:
            self.ui.balance.setStyleSheet("color:rgb(0,170,0); font-size:15pt")
            self.ui.balance.setText(f"₾{dashboard_data['total_stats']['balance']}")
        self.ui.total_expense.setText(f"₾{dashboard_data['total_stats']['total_expense']}")
        self.ui.average_expense.setText(f"₾{dashboard_data['monthly_average']['expense_average']}")
        self.ui.average_income.setText(f"₾{dashboard_data['monthly_average']['income_average']}")
        self.bar_chart(dashboard_data)
        self.piechart(dashboard_data)
        self.load_recent_transactions(dashboard_data)
    
    def load_recent_transactions(self,dashboard_data):
        layout = self.ui.recenttransactionlayout.layout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                    widget.deleteLater()

        for transaction in dashboard_data['recent_transactions']:
            layout.addWidget(Recent_transactions(transaction['itemname'],transaction['category'],transaction['date'],transaction['price'],transaction['transaction_type']))


    def bar_chart(self,dashboard_data):
        
        months = list(dashboard_data['monthly_data']['monthly_expense'].keys())
        income = list(dashboard_data['monthly_data']['monthly_income'].values())
        expenses = list(dashboard_data['monthly_data']['monthly_expense'].values())

        figure = Figure(figsize=(6, 4))
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)

        bar_width = 0.35
        x = range(len(months))
        soft_income_color = "#70AF89"
        soft_expense_color = "#F39477"

        ax.bar([i - bar_width/2 for i in x], income, width=bar_width, label='Income', color=soft_income_color)
        ax.bar([i + bar_width/2 for i in x], expenses, width=bar_width, label='Expenses', color=soft_expense_color)

        ax.set_xticks(x)
        ax.set_xticklabels(months)
        ax.set_title("Monthly Income vs Expenses")
        ax.set_ylabel("Amount")
        ax.set_xlabel("Month")
        ax.legend()

        figure.tight_layout()

        layout = self.ui.monthlyoverview_graph.layout()
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        layout.addWidget(canvas)

    def piechart(self,dashboard_data):
        soft_colors = [
        "#70AF89",  
        "#F39477", 
        "#A8DADC",   
        "#FFBCBC",  
        "#FFC75F",  
        "#C2F784",  
        "#B5EAEA",  
        "#F7D9C4",  
        "#CBAACB",  
        "#FFDAC1",  
        ]
        layout = self.ui.spending_piechart.layout()
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                    widget.deleteLater()
        labels = [i['category'] for i in dashboard_data['piechart']]
        sizes = [i['expense'] for i in dashboard_data['piechart']]
        fig = Figure(figsize=(4, 4))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%',
            startangle=90,
            colors=soft_colors,
            wedgeprops=dict(width=0.4),
            pctdistance=0.80
        )
        ax.axis('equal')
        layout.addWidget(canvas)


    def analytics(self):
        days = self.ui.days.currentText()
        match days:
            case"Last 30 Days":
                days = 30
            case "Last 60 Days":
                days = 60
            case "Last 90 Days":
                days = 90
        analytics_data = self.user.analytics(days)
        self.ui.average_income_analytics.setText(f"₾{analytics_data['stats']['income_average']}")
        self.ui.average_expense_analytics.setText(f"₾{analytics_data['stats']['expense_average']}")
        self.ui.total_income_analytics.setText(f'₾{analytics_data['stats']['total_income']}')
        self.ui.total_expense_analytics.setText(f'₾{analytics_data['stats']['total_expense']}')
        self.analytics_barchart(analytics_data)
        self.analytics_piechart(analytics_data)
        
    def analytics_barchart(self,analytics_data):
        months = list(analytics_data['analytics_data']['daily_income'].keys())
        income = list(analytics_data['analytics_data']['daily_income'].values())
        expenses = list(analytics_data['analytics_data']['daily_expense'].values())

        figure = Figure(figsize=(6, 4))
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)
        bar_width = 0.35
        x = range(len(months))
        soft_income_color = "#70AF89" 
        soft_expense_color = "#F39477"
        ax.bar([i - bar_width/2 for i in x], income, width=bar_width, label='Income', color=soft_income_color)
        ax.bar([i + bar_width/2 for i in x], expenses, width=bar_width, label='Expenses', color=soft_expense_color)
        ax.set_xticks(x)
        ax.set_xticklabels(months)
        ax.tick_params(axis='x', labelrotation=60, labelsize=6)
        ax.set_title("Monthly Income vs Expenses")
        ax.set_ylabel("Amount")
        ax.set_xlabel("Month")
        ax.legend()
        figure.tight_layout()

        layout = self.ui.analytics_graph.layout()
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        layout.addWidget(canvas)

    def analytics_piechart(self,analytics_data):
        soft_colors = [
        "#70AF89",  
        "#F39477", 
        "#A8DADC",   
        "#FFBCBC",  
        "#FFC75F",  
        "#C2F784",  
        "#B5EAEA",  
        "#F7D9C4",  
        "#CBAACB",  
        "#FFDAC1",  
        ]
        layout = self.ui.analytics_piechart.layout()
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                    widget.deleteLater()
        labels = [i['category'] for i in analytics_data['piechart']]
        sizes = [i['expense'] for i in analytics_data['piechart']]
        fig = Figure(figsize=(4, 4))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%',
            colors=soft_colors,
            startangle=90,
            wedgeprops=dict(width=0.4),
            pctdistance=0.80
        )
        ax.axis('equal')
        layout.addWidget(canvas)

    def fetch_budget(self):
        budgets = self.user.get_budget()
        layout = self.ui.budget_area.layout()
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                    widget.deleteLater()
        if budgets:
            for budget in budgets:
                widget = Budget(int(float(budget['spent'])),int(float(budget['budget'])),budget['category'],budget['status'],budget, self.remove_budget)
                layout.addWidget(widget)
    
    def remove_budget(self,item_id,widget):
        self.user.delete_budget(item_id)
        widget.setParent(None)
    
    def add_budget(self):
        self.ui.wrong_amount.setText('')
        budget = self.ui.budget_amount.text()
        category = self.ui.budget_category.currentText()
        if category == 'Select category':
            category = ''
        addbudget = self.user.add_budget(budget,category)
        if addbudget.get('category'):
            self.ui.wrong_amount.setText(addbudget['category'][0])
        elif addbudget.get('budget'):
            self.ui.wrong_amount.setText(addbudget['budget'][0])
        elif addbudget.get('non_field_errors'):
            self.ui.wrong_amount.setText(addbudget['non_field_errors'][0])
        else:
            self.fetch_budget()

    def fetch_bills(self):
        bills = self.user.get_recurring_bills()
        layout = self.ui.bills_scroll.layout()
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                    widget.deleteLater()
        for bill in bills:
            bill_frame = Bills_Frame(bill['category'],int(float(bill['price'])),bill['date'],bill, self.remove_bills)
            layout.addWidget(bill_frame)

    def remove_bills(self,item_id,widget):
        self.user.delete_recurring_bills(item_id)
        widget.setParent(None)

    def add_bills(self):
        self.ui.wrong_amount_bills.setText('')
        category = self.ui.category_bills.currentText()
        if category == 'Select category ':
            category = ''
        price = self.ui.amount_bills.text()
        date = self.ui.date_bills.text()
        data = self.user.create_recurring_bills(category,price,date)
        if data.get('non_field_errors'):
            self.ui.wrong_amount_bills.setText(data.get('non_field_errors')[0])
        elif data.get('category'):
            self.ui.wrong_amount_bills.setText(data.get('category')[0])
        elif data.get('price'):
            self.ui.wrong_amount_bills.setText(data.get('price')[0])
        elif data.get('date'):
            self.ui.wrong_amount_bills.setText(data.get('date')[0])

        self.fetch_bills()

    def fetch_transaction(self):
        layout = self.ui.transaction_area.layout()
        category = self.ui.transaction_category.currentText()
        if category == 'Select category ':
            category = ''
        transaction_type = self.ui.transaction_type.currentText()
        if transaction_type == "All":
            transaction_type = ''
        from_date = self.ui.from_date.date().toString('yyyy-MM-dd')
        to_date = self.ui.to_date.date().toString('yyyy-MM-dd')
        
        if self.sender() != self.more_button:
            self.user.page = 1
            transactions = self.user.filter_expenses(from_date,to_date,category,transaction_type)
            next_page = transactions.get('next')
            if layout is not None:
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        if widget == self.button_widget:
                            continue
                        widget.setParent(None)
                        widget.deleteLater()
            for transaction in transactions['results']:
                widget = Transaction_Frame(transaction['date'],transaction['itemname'],transaction['category'],transaction['transaction_type'],transaction['price'],transaction,self.remove_transaction)
                layout.addWidget(widget)
            if next_page == None:
                self.button_widget.hide()
            else:
                self.button_widget.show()
                layout.addWidget(self.button_widget)
        else:
            transactions = self.user.filter_expenses(from_date,to_date,category,transaction_type)
            next_page = transactions.get('next')
            for transaction in transactions['results']:
                widget = Transaction_Frame(transaction['date'],transaction['itemname'],transaction['category'],transaction['transaction_type'],transaction['price'],transaction,self.remove_transaction)
                layout.addWidget(widget)
            if next_page == None:
                self.button_widget.hide()
            else:
                self.button_widget.show()
                layout.addWidget(self.button_widget)


    def add_transaction(self):
        self.ui.transaction_add_wrong_itemname.setText("")
        self.ui.transaction_add_wrong_amount.setText("")
        category = self.ui.transaction_add_category.currentText()
        if category == 'Select category ':
            category = ''
        transaction_type = self.ui.transaction_add_type.currentText()
        amount = self.ui.transaction_add_amount.text()
        item = self.ui.transaction_add_item.text()
        added_transaction = self.user.add_transaction(category,item,amount,transaction_type)
        if added_transaction.get('category'):
            self.ui.transaction_add_wrong_itemname.setText(added_transaction.get('category')[0])
        elif added_transaction.get('price'):
            self.ui.transaction_add_wrong_amount.setText(added_transaction.get('price')[0])
        elif added_transaction.get('itemname'):
            self.ui.transaction_add_wrong_itemname.setText(added_transaction.get('itemname')[0])
        elif added_transaction.get('non_field_errors'):
            self.ui.transaction_add_wrong_itemname.setText(added_transaction.get('non_field_errors')[0])

    def remove_transaction(self,item_id,widget):
        self.user.delete_transaction(item_id)
        widget.setParent(None)

    def log_out(self):
        from login.login_window import LoginWindow
        self.user.log_out()
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()


    def on_tab_change(self, index, index_2=None):
        match index:
            case 0:
                self.dashboard()
            case 1:
                self.fetch_budget()
            case 2:
                match index_2:
                    case 1:
                        self.fetch_transaction()
            case 3:
                self.analytics()
            case 4:
                self.fetch_bills()

