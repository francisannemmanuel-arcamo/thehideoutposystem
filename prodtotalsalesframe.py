from tkinter import *
from tkinter import ttk
import POSdatabase


class ProdTotalSales:
    def __init__(self, frame):
        self.frame = frame

        prod_list_frame = Frame(self.frame, bg="white", highlightbackground="black", highlightthickness=2)
        prod_list_frame.place(x=10, y=50, height=570, width=1030)

        scroll_y = Scrollbar(prod_list_frame, orient=VERTICAL)

        self.search_name = StringVar()
        self.search_categ = StringVar()

        srch_icon = PhotoImage(file=r"images\blacksearch.png").subsample(2, 2)

        srch_name_lbl = Label(self.frame, bg="#0A100d", fg="white", font=("Bebas Neue", 14), image=srch_icon,
                              text=" Name", compound="left", anchor="w")
        srch_name_lbl.img = srch_icon
        srch_name = Entry(self.frame, highlightbackground="black", highlightthickness=2, font=("Blinker", 15, "bold"),
                          textvariable=self.search_name)
        srch_categ_lbl = Label(self.frame, bg="#0A100d", fg="white", font=("Bebas Neue", 14), image=srch_icon,
                               text=" Category", compound="left", anchor="w")
        srch_categ = ttk.Combobox(self.frame, textvariable=self.search_categ, font=("Bebas Neue", 14),
                                  values=["All", "Coffee (Hot/Iced)", "Add Ons", "Non-coffee", "Snacks",
                                          "Homemade Ice Cream"])
        self.search_categ.set("All")
        srch_name_lbl.place(height=33, width=70, y=6, x=10)
        srch_name.place(x=80, y=6, height=33, width=220)
        srch_categ_lbl.place(width=100, height=33, y=6, x=305)
        srch_categ.place(height=33, width=160, x=405, y=6)

        self.search_name.trace("w", lambda name, index, mode, sv=self.search_name: self.display_prodsearchnamecateg())
        self.search_categ.trace("w", lambda name, index, mode, sv=self.search_categ: self.display_prodsearchnamecateg())

        heading_bg = ttk.Style()
        heading_bg.theme_use("clam")
        heading_bg.configure('Treeview.Heading', background="black", foreground="white", font=("Bebas Neue", 13))

        self.prod_total_table = ttk.Treeview(prod_list_frame, columns=("prod_id", "prod_name", "prod_categ",
                                                                       "prod_qty", "prod_sales"))
        self.prod_total_table.config(yscrollcommand=scroll_y)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.prod_total_table.yview)
        self.prod_total_table.heading("prod_id", text="PRODUCT ID")
        self.prod_total_table.heading("prod_name", text="PRODUCT NAME")
        self.prod_total_table.heading("prod_categ", text="PRODUCT CATEGORY")
        self.prod_total_table.heading("prod_qty", text="TOTAL QUANTITY SOLD")
        self.prod_total_table.heading("prod_sales", text="TOTAL SALES")
        self.prod_total_table['show'] = 'headings'
        self.prod_total_table.column("prod_id", width=160, anchor="center")
        self.prod_total_table.column("prod_name", width=300)
        self.prod_total_table.column("prod_categ", width=215)
        self.prod_total_table.column("prod_qty", width=170, anchor="center")
        self.prod_total_table.column("prod_sales", width=170, anchor="center")
        self.prod_total_table.pack(fill=BOTH, expand=1)

        self.display_prodsearchnamecateg()

    def display_prodsearchnamecateg(self):
        if self.search_categ.get() == "All":
            result = POSdatabase.search_prod_db_by_namecateg(self.search_name.get(), "")
        else:
            result = POSdatabase.search_prod_db_by_namecateg(self.search_name.get(), self.search_categ.get())
        self.prod_total_table.delete(*self.prod_total_table.get_children())
        if not result:
            return
        else:
            for x in result:
                quant = POSdatabase.total_quantity_prod(x[0])
                stot = POSdatabase.tot_sales_prod(x[0])
                if quant != 0:
                    self.prod_total_table.insert('', END, values=(x[0], x[1], x[2], quant, "{:.2f}".format(stot)))
