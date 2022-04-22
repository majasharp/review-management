import string
from tkinter import *
import random

@staticmethod
def populate_menu(currentMenuItem, controller, parent, startingRow, views):
    label = Label(parent, text ="REVIEW MANAGEMENT")
    label.grid(row = 0, column = 0, padx = 5, pady = 5)

    for idx, (title, view) in enumerate(views.items()):
        if currentMenuItem != view:                
            #lambda requires v = view to store value of iteration
            Button(parent, text = title, command = lambda v = view:controller.show_frame(v, None)).grid(row = startingRow + idx + 1, column = 0, padx = 5, pady = 5)

@staticmethod
def populate_table(data, table):
    table.heading("#0",text="",anchor=CENTER)
    table.column("#0", width=0,  stretch=NO)
    cols= []

    for attr, value in data[0].__dict__.items():
        if attr != 'id':
            cols.append(attr)

    table['columns']= tuple(cols)

    for col in cols:
        if attr != 'id':
            table.column(col,anchor=CENTER, width=80)
            table.heading(col,text=col.replace("_", " ").upper(),anchor=CENTER, command=lambda _col=col: \
            treeview_sort_column(table, _col, False))


    for i in range(len(data)):
        rowData = []
        for attr in cols:
            rowData.append(getattr(data[i], attr))
        table.insert(parent='',index='end', iid=i, text='', values=tuple(rowData))

@staticmethod
def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse, key = lambda tup : int(tup[0]) if tup[0].isdigit() else tup[0])

    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    tv.heading(col, text=col, command=lambda _col=col: \
        treeview_sort_column(tv, _col, not reverse))

@staticmethod
def validate_coupon_amount(amount, isTl, isPremierCustomer):
    letters = string.ascii_lowercase
    if amount.isdigit(): 
            couponValue = int(amount)
            couponCode = None
            
            allowedCouponValue = 10 * (2.5 if isTl else 1) * (2 if isPremierCustomer == 1 else 1)
            if couponValue > allowedCouponValue:
                raise Exception(f'The max coupon value available is £{int(allowedCouponValue)}') 
            else:    
                couponCode = ''.join(random.choice(letters) for i in range(10))
                return couponCode
    else:
        raise Exception("You must enter a number as a coupon value")

@staticmethod
def calculate_importance_score(customerReview, sentimentScore):
    star_rating = customerReview.get_star_rating()
    premier = customerReview.get_premier()

    base_score = 0 if star_rating > 3 else 4 - star_rating

    sentiment_multiplier = abs(sentimentScore) + 1 if sentimentScore < -0.005 else 1 #NTLK considers compound score < -0.005 to be negative.

    return (base_score * sentiment_multiplier) + (premier * 2)