from tkinter import *
from tkinter import ttk

import POSdatabase


class PaymentHistory:
    def __init__(self, frame):
        self.frame = frame

        pay_hist_frame = Frame(self.frame, bg="white", highlightbackground="black", highlightthickness=2)
        pay_hist_frame.place(x=10, y=10, height=610, width=1030)

        scroll_y = Scrollbar(pay_hist_frame, orient=VERTICAL)

        heading_bg = ttk.Style()
        heading_bg.theme_use("clam")
        heading_bg.configure('Treeview.Heading', background="black", foreground="white", font=("Bebas Neue", 13))

        self.pay_hist_table = ttk.Treeview(pay_hist_frame, columns=("pay_id", "trans_id", "pay_date", "total_cost",
                                                                    "vat", "vat_sale", "amount", "change"))
        self.pay_hist_table.config(yscrollcommand=scroll_y)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.pay_hist_table.yview)
        self.pay_hist_table.heading("pay_id", text="PAYMENT ID")
        self.pay_hist_table.heading("trans_id", text="TRANSACT ID")
        self.pay_hist_table.heading("pay_date", text="DATE")
        self.pay_hist_table.heading("total_cost", text="TOTAL COST")
        self.pay_hist_table.heading("vat", text="VAT")
        self.pay_hist_table.heading("vat_sale", text="VATABLE SALE")
        self.pay_hist_table.heading("amount", text="AMOUNT PAID")
        self.pay_hist_table.heading("change", text="CHANGE")
        self.pay_hist_table['show'] = 'headings'
        self.pay_hist_table.column("pay_id", anchor="center", width=150)
        self.pay_hist_table.column("trans_id", anchor="center", width=150)
        self.pay_hist_table.column("pay_date", anchor="center", width=150)
        self.pay_hist_table.column("total_cost", anchor="center", width=114)
        self.pay_hist_table.column("vat", anchor="center", width=114)
        self.pay_hist_table.column("vat_sale", anchor="center", width=114)
        self.pay_hist_table.column("amount", anchor="center", width=114)
        self.pay_hist_table.column("change", anchor="center", width=114)
        self.pay_hist_table.pack(fill=BOTH, expand=1)

        pay_hist = POSdatabase.payment_history("")
        self.pay_hist_table.delete(*self.pay_hist_table.get_children())
        for pay in pay_hist:
            self.pay_hist_table.insert('', END, values=(pay[0], pay[1], pay[2], "{:.2f}".format(pay[3]),
                                                        "{:.2f}".format(pay[6]), "{:.2f}".format(pay[7]),
                                                        "{:.2f}".format(pay[4]), "{:.2f}".format(pay[5])))
