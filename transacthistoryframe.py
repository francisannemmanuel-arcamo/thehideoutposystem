from tkinter import *
from tkinter import ttk


class TransactHistory:
    def __init__(self, frame):
        self.frame = frame

        trans_hist_frame = Frame(self.frame, bg="white", highlightbackground="black", highlightthickness=2)
        trans_hist_frame.place(x=10, y=10, height=610, width=1030)

        scroll_y = Scrollbar(trans_hist_frame, orient=VERTICAL)

        heading_bg = ttk.Style()
        heading_bg.theme_use("clam")
        heading_bg.configure('Treeview.Heading', background="black", foreground="white", font=("Bebas Neue", 13))

        self.trans_hist_table = ttk.Treeview(trans_hist_frame, columns=("trans_id", "trans_date", "cashier", "pay_id",
                                                                        "total", "amount", "change"))
        self.trans_hist_table.config(yscrollcommand=scroll_y)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.trans_hist_table.yview)
        self.trans_hist_table.heading("trans_id", text="TRANSACT ID")
        self.trans_hist_table.heading("trans_date", text="TRANSACT DATE")
        self.trans_hist_table.heading("cashier", text="CASHIER")
        self.trans_hist_table.heading("pay_id", text="PAYMENT ID")
        self.trans_hist_table.heading("total", text="TOTAL COST")
        self.trans_hist_table.heading("amount", text="AMOUNT PAID")
        self.trans_hist_table.heading("change", text="CHANGE")
        self.trans_hist_table['show'] = 'headings'
        self.trans_hist_table.column("trans_id", anchor="center", width=150)
        self.trans_hist_table.column("trans_date", anchor="center", width=160)
        self.trans_hist_table.column("cashier", anchor="w", width=220)
        self.trans_hist_table.column("pay_id", anchor="center", width=150)
        self.trans_hist_table.column("total", anchor="center", width=110)
        self.trans_hist_table.column("amount", anchor="center", width=110)
        self.trans_hist_table.column("change", anchor="center", width=110)
        self.trans_hist_table.pack(fill=BOTH, expand=1)