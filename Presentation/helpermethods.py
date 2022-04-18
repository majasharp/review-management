from tkinter import *
from copy import *

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
