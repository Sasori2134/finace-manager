import requests
import json

class User:
    global endpoint
    endpoint = 'http://127.0.0.1:8000/'
    def __init__(self,access_token,refresh_token):
        self.access_token = access_token
        self.refresh_token = refresh_token
    
    def add_transaction(self,category,itemname,price,transaction_type):
        response = requests.post(f'{endpoint}add_transaction', json={'category' : category, 'itemname' : itemname, 'price' : price, 'transaction_type' : transaction_type}, headers = {'Authorization' : f'Bearer {self.access_token}'})
        return response.json(),response.status_code
    
    def delete_transaction(self,pk):
        response = requests.delete(f'{endpoint}delete_transaction/{pk}',headers = {'Authorization' : f'Bearer {self.access_token}'})
        return response.status_code

    def filter_expenses(self,from_date = None,to_date = None,category = None,transaction_type = None):
        response = requests.get(f'{endpoint}expenses', params={'from_date' : from_date, 'to_date' : to_date, 'category' : category, 'transaction_type' : transaction_type}, headers = {'Authorization' : f'Bearer {self.access_token}'})
        return response.json()

    def add_budget(self,budget,category):
        response = requests.post(f'{endpoint}add_budget', json={'budget' : budget, 'category' : category}, headers = {'Authorization' : f'Bearer {self.access_token}'})
        return response.json()

    def delete_budget(self,pk):
        response = requests.delete(f'{endpoint}delete_budget/{pk}', headers = {'Authorization' : f'Bearer {self.access_token}'})
        return response.status_code

    def get_budget(self):
        response = requests.get(f'{endpoint}get_budget', headers = {'Authorization' : f'Bearer {self.access_token}'})
        return response.json()
    def create_recurring_bills(self,category,price,date):
        response = requests.post(f'{endpoint}/recurring_bills', json={'category' : category, 'price' : price, 'date' : date}, headers = {'Authorization' : f'Bearer {self.access_token}'})
        return response.json()

    def delete_recurring_bills(self,pk):
        response = requests.delete(f'{endpoint}delete_recurring_bills/{pk}', headers = {'Authorization' : f'Bearer {self.access_token}'})
        return response.status_code

    def dashboard_monthly_average(self):
        response = requests.get(f'{endpoint}dashboard/monthly_average', headers = {'Authorization' : f'Bearer {self.access_token}'})
        return response.json()
    def dashboard_monthly_data(self):
        response = requests.get(f'{endpoint}dashboard/monthly_data', headers = {'Authorization' : f'Bearer {self.access_token}'})
        return response.json()

    def dashboard_total_stats(self):
        response = requests.get(f'{endpoint}dashboard/total_stats', headers = {'Authorization' : f'Bearer {self.access_token}'})
        return response.json()

    def dashboard_recent_transactions(self):
        response = requests.get(f'{endpoint}dashboard/recent_transactions', headers = {'Authorization' : f'Bearer {self.access_token}'})
        return response.json()

    def dashboard_data_for_piechart_total(self):
        response = requests.get(f'{endpoint}dashboard/data_for_piechart_total', headers = {'Authorization' : f'Bearer {self.access_token}'})
        return response.json()

    def analytics_data(self,days):
        response = requests.get(f'{endpoint}analytics/analytics_data',params={'days' : days},headers = {'Authorization' : f'Bearer {self.access_token}'})
        return response.json()

    def analytics_stats(self,days):
        response = requests.get(f'{endpoint}analytics/analytics_stats', params={'days' : days}, headers = {'Authorization' : f'Bearer {self.access_token}'})
        return response.json()

    def data_for_piechart_analytics(self):
        response = reqeusts.get(f'{endpoint}analytics/analytics_data_for_piechart_analytics', params={'days' : days}, headers = {'Authorization' : f'Bearer {self.access_token}'})
        return response.json()
    def log_out(self):
        response = requests.post(f'{endpoint}api/log_out', json = {'refresh' : self.refresh_token}, headers = {'Authorization' : f'Bearer {self.access_token}'})
        return response.status_code
tokens = requests.post(f'{endpoint}api/token/', json={'username' : 'alex', 'password' : 'alex'})
user = User(tokens.json()['access'],tokens.json()['refresh'])
print(user.log_out())