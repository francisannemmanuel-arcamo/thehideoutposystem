from tkinter import *
from tkinter import ttk

import POSdatabase


class SalesHistory:
    def __init__(self, frame):
        self.frame = frame

        sales_list_frame = Frame(self.frame, bg="white", highlightbackground="black", highlightthickness=2)
        sales_list_frame.place(x=10, y=50, height=570, width=1030)

        scroll_y = Scrollbar(sales_list_frame, orient=VERTICAL)

        self.trans_id = StringVar()
        self.trans_date = StringVar()
        self.prod_id = StringVar()

        srch_icon = PhotoImage(file=r"images\blacksearch.png").subsample(2, 2)
        srch_transid_lbl = Label(self.frame, bg="#0A100d", fg="white", font=("Bebas Neue", 14),
                                 image=srch_icon, text=" TR ID", compound="left", anchor="w")
        srch_transid_lbl.img = srch_icon
        trans_id = Entry(self.frame, highlightbackground="black", highlightthickness=2, font=("Blinker", 15, "bold"),
                         textvariable=self.trans_id)
        srch_transdate_lbl = Label(self.frame, bg="#0A100d", fg="white", font=("Bebas Neue", 14),
                                   image=srch_icon, text=" TR DATE", compound="left", anchor="w")
        srch_transdate_lbl.img = srch_icon
        srch_prodid_lbl = Label(self.frame, bg="#0A100d", fg="white", font=("Bebas Neue", 14),
                                image=srch_icon, text=" PROD ID", compound="left", anchor="w")
        srch_prodid_lbl.img = srch_icon
        prod_id = Entry(self.frame, highlightbackground="black", highlightthickness=2, font=("Blinker", 15, "bold"),
                        textvariable=self.prod_id)

        srch_transid_lbl.place(height=33, width=70, y=6, x=10)
        trans_id.place(height=33, width=160, y=6, x=80)
        srch_prodid_lbl.place(height=33, width=80, y=6, x=245)
        prod_id.place(height=33, width=160, y=6, x=325)
        srch_transdate_lbl.place(height=33, width=90, y=6, x=490)

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

        self.trans_id.trace("w", lambda name, index, mode, sv=self.trans_id: self.display_sales_hist())
        self.prod_id.trace("w", lambda name, index, mode, sv=self.prod_id: self.display_sales_hist())
        self.display_sales_hist()

    def display_sales_hist(self):
        sales = POSdatabase.trans_show(self.trans_id.get(), self.prod_id.get())
        self.sales_table.delete(*self.sales_table.get_children())
        if not sales:
            return
        else:
            for ent in sales:
                trans_det = POSdatabase.trans_details(ent[0])[1]
                prod_name = POSdatabase.search_prod_db_by_id(ent[1])[1]
                self.sales_table.insert('', END, values=(ent[0], trans_det, ent[1], prod_name, ent[2], ent[3], ent[5]))
