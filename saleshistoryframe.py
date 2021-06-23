from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import POSdatabase


class SalesHistory:
    def __init__(self, frame):
        self.frame = frame

        sales_list_frame = Frame(self.frame, bg="white", highlightbackground="black", highlightthickness=2)
        sales_list_frame.place(x=10, y=50, height=570, width=1030)

        scroll_y = Scrollbar(sales_list_frame, orient=VERTICAL)

        self.trans_id = StringVar()

        heading_bg = ttk.Style()
        heading_bg.theme_use("clam")
        heading_bg.configure('Treeview.Heading', background="black", foreground="white", font=("Bebas Neue", 13))

        self.sales_table = ttk.Treeview(sales_list_frame, columns=("trans_id", "trans_date", "prod_id", "prod_name",
                                                                   "prod_price", "prod_qty", "subtotal"))
        self.sales_table.config(yscrollcommand=scroll_y)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.sales_table.yview)
        self.sales_table.heading("trans_id", text="TRANSACT ID")
        self.sales_table.heading("trans_date", text="TRANSACT DATE")
        self.sales_table.heading("prod_id", text="PRODUCT ID")
        self.sales_table.heading("prod_name", text="PRODUCT NAME")
        self.sales_table.heading("prod_price", text="PRODUCT PRICE")
        self.sales_table.heading("prod_qty", text="QUANTITY")
        self.sales_table.heading("subtotal", text="SUBTOTAL")
        self.sales_table['show'] = 'headings'
        self.sales_table.column("trans_id", width=135, anchor="center")
        self.sales_table.column("trans_date", width=150, anchor="center")
        self.sales_table.column("prod_id", width=135, anchor="center")
        self.sales_table.column("prod_name", width=210)
        self.sales_table.column("prod_price", width=130, anchor="center")
        self.sales_table.column("prod_qty", width=80, anchor="center")
        self.sales_table.column("subtotal", width=130, anchor="center")
        self.sales_table.pack(fill=BOTH, expand=1)

        self.trans_id.trace("w", lambda name, index, mode, sv=self.trans_id: self.display_sales_hist_by_trans())
        self.display_sales_hist_by_trans()

    def display_sales_hist_by_trans(self):
        sales = POSdatabase.trans_show(self.trans_id.get())
        self.sales_table.delete(*self.sales_table.get_children())
        if not sales:
            return
        else:
            for ent in sales:
                trans_det = POSdatabase.trans_details(ent[0])[1]
                prod_name = POSdatabase.search_prod_db_by_id(ent[1])[1]
                self.sales_table.insert('', END, values=(ent[0], trans_det, ent[1], prod_name, ent[2], ent[3], ent[5]))
