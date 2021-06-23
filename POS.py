# modules
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from time import strftime
import datetime as dt

# local files
from usersettingsframe import UserSettingsFrame
from prodtotalsalesframe import ProdTotalSales
from saleshistoryframe import SalesHistory
from paymenthistoryframe import PaymentHistory
from transacthistoryframe import TransactHistory
import POSdatabase


class LogIn:
    def __init__(self):
        POSdatabase.db_table_create()

        self.main_window = Tk()
        self.main_window.title('Log in')
        self.main_window.geometry('350x500+525+100')
        self.main_window.config(bg='white')
        self.main_window.iconbitmap(r"images\logo.ico")

        self.user_input = StringVar()
        self.pass_input = StringVar()

        logo_img = PhotoImage(file=r"images\logo.png").subsample(2, 2)
        info_label = Label(self.main_window, image=logo_img)
        info_label.place(x=75, y=30, width=200, height=200)
        info_label.img = logo_img

        info_user = Label(self.main_window, text='USERNAME', font=('Bebas Neue', 14), fg='black',
                          bg='white')
        info_user.place(x=30, y=260)
        self.userinput = Entry(self.main_window, font=('Calibri', 14), bd=1, textvariable=self.user_input,
                               highlightbackground="black", highlightthickness=2)
        self.userinput.place(x=30, y=290, width=290, height=30)

        info_pass = Label(self.main_window, text='PASSWORD', font=('Bebas Neue', 14), fg='black',
                          bg='white')
        info_pass.place(x=30, y=330)
        self.passinput = Entry(self.main_window, font=('Calibri', 14), bd=1, textvariable=self.pass_input, show="*",
                               highlightbackground="black", highlightthickness=2)
        self.passinput.place(x=30, y=360, width=290, height=30)

        login_btn = Button(self.main_window, text='L O G I N', fg='white', command=self.login,
                           activebackground="grey",
                           font=("Calibri", 15, "bold"), bd=0, bg="black", )
        login_btn.place(x=100, y=430, width=150, height=40)

        self.main_window.protocol("WM_DELETE_WINDOW", self.exit_handler)
        self.main_window.mainloop()

    def login(self):
        if POSdatabase.log_in(self.user_input.get(), self.pass_input.get()):
            if self.user_input.get() == "admin":
                if messagebox.askyesno("Administrator", "Do you want to log in to the admin-only site?"):
                    self.main_window.destroy()
                    ManagerMain()
                else:
                    self.main_window.destroy()
                    SalesRegister(self.user_input.get())
            else:
                self.main_window.destroy()
                SalesRegister(self.user_input.get())

        else:
            self.userinput.config(highlightbackground='red', highlightthickness=2)
            self.passinput.config(highlightbackground='red', highlightthickness=2)
            messagebox.showerror('Log-in Error', 'Login failed. Please provide correct details')

    def exit_handler(self):
        if messagebox.askyesno("Exit", "Do you want to exit?"):
            self.main_window.destroy()
        else:
            return


class ManagerMain:
    def __init__(self):
        self.frame = Tk()
        self.frame.title("The Hideout Point-of-Sale (POS) System")
        self.frame.geometry("1350x690+0+0")
        self.frame.resizable(False, False)
        self.frame.iconbitmap(r"images\logo.ico")

        self.product_id = StringVar()
        self.product_name = StringVar()
        self.product_categ = StringVar()
        self.product_price = DoubleVar()
        self.prod_srch_categ = StringVar()

        self.search_product = StringVar()

        # background frames
        bg_frame = Frame(self.frame, bg="white")
        bg_frame.place(x=0, y=0, width=1350, height=690)

        # navigation frame
        self.nav_frame = Frame(bg_frame, bg="#0a100d")
        self.nav_frame.place(x=0, y=0, width=280, height=690)

        # contents frame
        self.right_frame = Frame(bg_frame, bg="white")
        self.right_frame.place(x=280, y=0, width=1070, height=690)

        admin_img = PhotoImage(file=r"images\admin.png").subsample(3, 3)
        admin_name = Label(self.nav_frame, image=admin_img, bg="#0a100d")
        admin_name.img = admin_img
        admin_name.place(x=65, y=25, width=150, height=150)

        prodnavimg = PhotoImage(file=r"images\prodnav.png")
        prodtotalnavimg = PhotoImage(file=r"images\prodtotalnav.png")
        salesnavimg = PhotoImage(file=r"images\salesnav.png")
        transnavimg = PhotoImage(file=r"images\transnav.png")
        paynavimg = PhotoImage(file=r"images\paynav.png")
        usernavimg = PhotoImage(file=r"images\usernav.png")
        outnavimg = PhotoImage(file=r"images\outnav.png")

        prod_list = Button(self.nav_frame, text="   PRODUCTS", relief=FLAT, font=("Blinker", 15, "bold"),
                           bg="#0a100d", fg="white", activebackground="#0a100d", activeforeground="white",
                           image=prodnavimg, anchor="w", compound="left", command=self.products)
        prod_list.img = prodnavimg
        prod_list.place(x=0, y=200, width=280, height=50)
        prod_total = Button(self.nav_frame, text="   PRODUCT TOTAL SALES", relief=FLAT, font=("Blinker", 15, "bold"),
                            bg="#0a100d", fg="white", activebackground="#0a100d", activeforeground="white",
                            image=prodtotalnavimg, anchor="w", compound="left", command=self.prod_total_sales)
        prod_total.img = prodtotalnavimg
        prod_total.place(x=0, y=250, width=280, height=50)
        sales_hist = Button(self.nav_frame, text="   SALES HISTORY", relief=FLAT, font=("Blinker", 15, "bold"),
                            bg="#0a100d", fg="white", activebackground="#0a100d", activeforeground="white",
                            anchor="w", compound="left", image=salesnavimg, command=self.sales_history)
        sales_hist.img = salesnavimg
        sales_hist.place(x=0, y=300, width=280, height=50)
        transact_hist = Button(self.nav_frame, text="   TRANSACTION HISTORY", relief=FLAT, font=("Blinker", 15, "bold"),
                               bg="#0a100d", fg="white", activebackground="#0a100d", activeforeground="white",
                               image=transnavimg, anchor="w", compound="left", command=self.trans_history)
        transact_hist.img = transnavimg
        transact_hist.place(x=0, y=350, width=280, height=50)
        pay_hist = Button(self.nav_frame, text="   PAYMENT HISTORY", relief=FLAT, font=("Blinker", 15, "bold"),
                          bg="#0a100d", fg="white", activebackground="#0a100d", activeforeground="white",
                          image=paynavimg, anchor="w", compound="left", command=self.pay_history)
        pay_hist.img = paynavimg
        pay_hist.place(x=0, y=400, width=280, height=50)
        user_set = Button(self.nav_frame, text="   USER SETTINGS", relief=FLAT, font=("Blinker", 15, "bold"),
                          bg="#0a100d", fg="white", activebackground="#0a100d", activeforeground="white",
                          image=usernavimg, anchor="w", compound="left", command=self.user_settings)
        user_set.img = usernavimg
        user_set.place(x=0, y=450, width=280, height=50)
        log_out = Button(self.nav_frame, text="   LOG OUT", relief=FLAT, font=("Blinker", 15, "bold"),
                         bg="#0a100d", fg="white", activebackground="#0a100d", activeforeground="white",
                         image=outnavimg, anchor="w", compound="left", command=self.logout)
        log_out.img = outnavimg
        log_out.place(x=0, y=500, width=280, height=50)

        self.product_frame = Frame(self.right_frame)
        self.prod_total_sales_frame = Frame(self.right_frame)
        self.sales_hist_frame = Frame(self.right_frame)
        self.trans_hist_frame = Frame(self.right_frame)
        self.pay_hist_frame = Frame(self.right_frame)
        self.user_frame = Frame(self.right_frame)

        self.heading = Label(self.right_frame, text="", font=("Blinker", 15, "bold"), bg="white", anchor="w")
        self.heading.place(x=10, y=5, width=200, height=40)

        # products
        self.search_prod = Entry(self.product_frame, highlightbackground="black", highlightthickness=2,
                                 font=("Blinker", 15, "bold"), textvariable=self.search_product)
        self.prod_list_frame = Frame(self.product_frame, bg="grey", highlightbackground="black", highlightthickness=2)
        self.product_table = ttk.Treeview(self.prod_list_frame, columns=("prod_id",
                                                                         "prod_name",
                                                                         "prod_categ",
                                                                         "prod_price"),
                                          )
        self.scroll_x_prod = Scrollbar(self.prod_list_frame, orient=HORIZONTAL)
        self.scroll_y_prod = Scrollbar(self.prod_list_frame, orient=VERTICAL)

        self.frame.protocol("WM_DELETE_WINDOW", self.exit_handler)
        self.frame.mainloop()

    def hide_widgets(self):
        self.product_frame.place_forget()
        self.prod_total_sales_frame.place_forget()
        self.sales_hist_frame.place_forget()
        self.trans_hist_frame.place_forget()
        self.pay_hist_frame.place_forget()
        self.user_frame.place_forget()
        self.prod_list_frame.place_forget()
        self.product_table.pack_forget()

    def products(self):
        self.hide_widgets()
        self.product_frame.place(x=10, y=50, width=1050, height=630)
        self.heading.config(text="PRODUCT LIST")

        srch_icon = PhotoImage(file=r"images\blacksearch.png").subsample(2, 2)
        srch_categ_lbl = Label(self.product_frame, bg="#0A100d", fg="white", font=("Bebas Neue", 14),
                               image=srch_icon, text=" Category", compound="left", anchor="w")
        srch_categ = ttk.Combobox(self.product_frame, textvariable=self.prod_srch_categ, font=("Bebas Neue", 14),
                                  values=["All", "Coffee (Hot/Iced)", "Add Ons", "Non-coffee", "Snacks",
                                          "Homemade Ice Cream"])
        self.prod_srch_categ.set("All")
        self.prod_srch_categ.trace("w", lambda name, index, mode,
                                   sv=self.prod_srch_categ: self.display_prodsearchnamecateg())

        srch_name_lbl = Label(self.product_frame, bg="#0A100d", fg="white", font=("Bebas Neue", 14),
                              image=srch_icon, text=" Name", compound="left", anchor="w")
        srch_name_lbl.img = srch_icon

        srch_name_lbl.place(height=33, width=70, y=6, x=10)
        self.search_prod.place(x=80, y=6, height=33, width=220)
        srch_categ_lbl.place(width=100, height=33, y=6, x=305)
        srch_categ.place(height=33, width=160, x=405, y=6)

        add_prod_img = PhotoImage(file=r"images/addprod.png").subsample(2, 2)
        add_prod_btn = Button(self.product_frame, image=add_prod_img, command=self.add_product_frame)
        add_prod_btn.img = add_prod_img
        edit_prod_img = PhotoImage(file=r"images/editprod.png").subsample(2, 2)
        edit_prod_btn = Button(self.product_frame, image=edit_prod_img, command=self.edit_product_frame)
        edit_prod_btn.img = edit_prod_img
        del_prod_img = PhotoImage(file=r"images/deleteprod.png").subsample(2, 2)
        delete_prod_btn = Button(self.product_frame, image=del_prod_img, command=self.delete_product)
        delete_prod_btn.img = del_prod_img

        add_prod_btn.place(x=920, y=5, width=35, height=35)
        edit_prod_btn.place(x=960, y=5, width=35, height=35)
        delete_prod_btn.place(x=1000, y=5, width=35, height=35)

        self.prod_list_frame.place(x=10, y=50, width=1030, height=570)

        heading_bg = ttk.Style()
        heading_bg.theme_use("clam")
        heading_bg.configure('Treeview.Heading', background="black", foreground="white", font=("Bebas Neue", 13))

        self.product_table.config(xscrollcommand=self.scroll_x_prod.set,  yscrollcommand=self.scroll_y_prod.set)
        self.scroll_x_prod.pack(side=BOTTOM, fill=X)
        self.scroll_y_prod.pack(side=RIGHT, fill=Y)
        self.scroll_x_prod.config(command=self.product_table.xview)
        self.scroll_y_prod.config(command=self.product_table.yview)
        self.product_table.heading("prod_id", text="PRODUCT ID")
        self.product_table.heading("prod_name", text="PRODUCT NAME")
        self.product_table.heading("prod_categ", text="PRODUCT CATEGORY")
        self.product_table.heading("prod_price", text="PRODUCT PRICE")
        self.product_table.column("prod_id", anchor="center", width=185)
        self.product_table.column("prod_name", width=380)
        self.product_table.column("prod_categ", width=300)
        self.product_table.column("prod_price", anchor="center", width=140)
        self.product_table['show'] = 'headings'
        self.product_table.pack(fill=BOTH, expand=1)

        self.display_prodsearchnamecateg()
        self.search_product.trace("w", lambda name, index, mode,
                                  sv=self.search_product: self.display_prodsearchnamecateg())

    def add_product_frame(self):
        self.add_prod_window = Toplevel()
        self.add_prod_window.title("Add Product")
        self.add_prod_window.geometry("450x400+590+155")
        self.add_prod_window.resizable(False, False)
        self.add_prod_window.config(bg="white")
        self.add_prod_window.iconbitmap(r"images\logo.ico")

        id_label = Label(self.add_prod_window, text="ID", font=("Bebas Neue", 17), bg="black", fg="white")
        id_label.place(x=15, y=125, width=90, height=40)
        prod_id_entry = Entry(self.add_prod_window, textvariable=self.product_id, highlightthickness=2,
                              highlightbackground="black", font=("Bebas Neue", 18))
        prod_id_entry.place(x=105, y=125, width=320, height=40)

        name_label = Label(self.add_prod_window, text="NAME", font=("Bebas Neue", 17), bg="black", fg="white")
        name_label.place(x=15, y=175, width=90, height=40)
        prod_name_entry = Entry(self.add_prod_window, textvariable=self.product_name, highlightthickness=2,
                                highlightbackground="black", font=("Bebas Neue", 18))
        prod_name_entry.place(x=105, y=175, width=320, height=40)

        categ_label = Label(self.add_prod_window, text="CATEGORY", font=("Bebas Neue", 17), bg="black", fg="white")
        categ_label.place(x=15, y=225, width=90, height=40)
        prod_categ_combo = ttk.Combobox(self.add_prod_window, textvariable=self.product_categ, font=("Bebas Neue", 18),
                                        values=["Coffee (Hot/Iced)",
                                                "Add Ons",
                                                "Non-coffee",
                                                "Snacks",
                                                "Homemade Ice Cream"])
        prod_categ_combo.place(x=105, y=225, width=320, height=40)

        price_label = Label(self.add_prod_window, text="PRICE", font=("Bebas Neue", 17), bg="black", fg="white")
        price_label.place(x=15, y=275, width=90, height=40)
        prod_price_entry = Entry(self.add_prod_window, textvariable=self.product_price, highlightthickness=2,
                                 highlightbackground="black", font=("Bebas Neue", 18))
        prod_price_entry.place(x=105, y=275, width=320, height=40)

        add_prod_button = Button(self.add_prod_window, command=self.add_product, text="ADD",
                                 bg="black", fg="white", activebackground="green", activeforeground="black",
                                 font=("Bebas Neue", 20))
        add_prod_button.place(x=245, y=335, width=80, height=40)
        clear_info_button = Button(self.add_prod_window, command=self.clear_data, text="CLEAR",
                                   bg="black", fg="white", activebackground="green", activeforeground="black",
                                   font=("Bebas Neue", 20))
        clear_info_button.place(x=335, y=335, width=80, height=40)

        prod_id_entry.delete(0, END)
        prod_name_entry.delete(0, END)
        prod_categ_combo.delete(0, END)
        prod_price_entry.delete(0, END)
        prod_price_entry.insert(0, 0.0)

    def add_product(self):
        if self.product_id.get() == "" or self.product_name.get() == "" or self.product_categ.get() == "":
            messagebox.showerror("Error", "Please fill out all fields")
            return
        else:
            try:
                self.product_price.get()
                if messagebox.askyesno("Confirmation", "Are you sure you want to add the product into the database?"):
                    if POSdatabase.add_prod_db(self.product_id.get().upper(), self.product_name.get().title(),
                                               self.product_categ.get(), self.product_price.get()):
                        self.clear_data()
                        messagebox.showinfo("Success", "Product added in database.")
                        self.add_prod_window.destroy()
                        self.display_prodsearchnamecateg()
                        return
                    else:
                        return
                else:
                    return
            except TclError:
                messagebox.showerror("error", "please provide valid price")

    def clear_data(self):
        self.product_id.set("")
        self.product_name.set("")
        self.product_categ.set("")
        self.product_price.set(0.0)

    def edit_product_frame(self):
        self.clear_data()

        selected = self.product_table.focus()
        contents = self.product_table.item(selected)
        self.prod_select = contents['values']

        if not self.prod_select:
            messagebox.showerror("Error", "Select a product first.")
            return
        else:
            self.edit_prod_window = Toplevel()
            self.edit_prod_window.title("EDIT PRODUCT")
            self.edit_prod_window.geometry("450x400+590+155")
            self.edit_prod_window.resizable(False, False)
            self.edit_prod_window.config(bg="white")
            self.edit_prod_window.iconbitmap(r"images\logo.ico")

            id_label = Label(self.edit_prod_window, text="ID", font=("Bebas Neue", 17), bg="black", fg="white")
            id_label.place(x=15, y=125, width=90, height=40)
            prod_id_entry = Entry(self.edit_prod_window, textvariable=self.product_id, highlightthickness=2,
                                  highlightbackground="black", font=("Bebas Neue", 18))
            prod_id_entry.place(x=105, y=125, width=320, height=40)

            name_label = Label(self.edit_prod_window, text="NAME", font=("Bebas Neue", 17), bg="black", fg="white")
            name_label.place(x=15, y=175, width=90, height=40)
            prod_name_entry = Entry(self.edit_prod_window, textvariable=self.product_name, highlightthickness=2,
                                    highlightbackground="black", font=("Bebas Neue", 18))
            prod_name_entry.place(x=105, y=175, width=320, height=40)

            categ_label = Label(self.edit_prod_window, text="CATEGORY", font=("Bebas Neue", 17), bg="black", fg="white")
            categ_label.place(x=15, y=225, width=90, height=40)
            prod_categ_combo = ttk.Combobox(self.edit_prod_window, textvariable=self.product_categ,
                                            font=("Bebas Neue", 18), values=["Coffee (Hot/Iced)",
                                                                             "Add Ons",
                                                                             "Non-coffee",
                                                                             "Snacks",
                                                                             "Homemade Ice Cream"])
            prod_categ_combo.place(x=105, y=225, width=320, height=40)

            price_label = Label(self.edit_prod_window, text="PRICE", font=("Bebas Neue", 17), bg="black", fg="white")
            price_label.place(x=15, y=275, width=90, height=40)
            prod_price_entry = Entry(self.edit_prod_window, textvariable=self.product_price, highlightthickness=2,
                                     highlightbackground="black", font=("Bebas Neue", 18))
            prod_price_entry.place(x=105, y=275, width=320, height=40)

            edit_info_button = Button(self.edit_prod_window, command=self.update_product, text="EDIT",
                                      bg="black", fg="white", activebackground="green", activeforeground="black",
                                      font=("Bebas Neue", 20))
            edit_info_button.place(x=255, y=335, width=80, height=40)
            clear_info_button = Button(self.edit_prod_window, command=self.clear_data, text="CLEAR",
                                       bg="black", fg="white", activebackground="green", activeforeground="black",
                                       font=("Bebas Neue", 20))
            clear_info_button.place(x=345, y=335, width=80, height=40)

            prod_id_entry.delete(0, END)
            prod_name_entry.delete(0, END)
            prod_categ_combo.delete(0, END)
            prod_price_entry.delete(0, END)

            prod_id_entry.insert(0, self.prod_select[0])
            prod_name_entry.insert(0, self.prod_select[1])
            prod_categ_combo.insert(0, self.prod_select[2])
            prod_price_entry.insert(0, self.prod_select[3])

    def update_product(self):
        try:
            if self.product_id.get() == "" or self.product_name.get() == "" or self.product_categ.get() == "":
                messagebox.showerror("Update Product Error", "Please fill out all fields")
                return
            else:
                if messagebox.askyesno("Update Product?", "Do you want to update the product details?"):
                    if POSdatabase.update_product_db(self.prod_select[0], self.product_id.get().upper(),
                                                     self.product_name.get().title(), self.product_categ.get(),
                                                     self.product_price.get()):
                        messagebox.showinfo("Success", "Information has been updated!")
                        self.clear_data()
                        self.edit_prod_window.destroy()
                        self.display_prodsearchnamecateg()
                        return
                    else:
                        return
                else:
                    return
        except TclError:
            messagebox.showerror("Error", "Please enter valid price.")
            return

    def delete_product(self):
        selected = self.product_table.focus()
        contents = self.product_table.item(selected)
        prod_select = contents['values']
        if not prod_select:
            messagebox.showerror("Error", "Choose a product first.")
            return
        else:
            if messagebox.askyesno("Delete Product", "Do you wish to remove this product?"):
                POSdatabase.delete_prod_db(prod_select[0])
                messagebox.showinfo("Success", "Product removed in database")
                self.display_prodsearchnamecateg()
                return
            else:
                return

    def display_prodsearchnamecateg(self):
        if self.prod_srch_categ.get() == "All":
            result = POSdatabase.search_prod_db_by_namecateg(self.search_product.get(), "")
        else:
            result = POSdatabase.search_prod_db_by_namecateg(self.search_product.get(), self.prod_srch_categ.get())
        self.product_table.delete(*self.product_table.get_children())
        if not result:
            return
        else:
            for x in result:
                self.product_table.insert('', END, values=(x[0], x[1], x[2], x[3]))

    def prod_total_sales(self):
        self.hide_widgets()
        self.prod_total_sales_frame.place(x=10, y=50, width=1050, height=630)
        self.heading.config(text="TOTAL SALES")
        ProdTotalSales(self.prod_total_sales_frame)

    def sales_history(self):
        self.hide_widgets()
        self.sales_hist_frame.place(x=10, y=50, width=1050, height=630)
        self.heading.config(text="SALES HISTORY")
        SalesHistory(self.sales_hist_frame)

    def trans_history(self):
        self.hide_widgets()
        self.trans_hist_frame.place(x=10, y=50, width=1050, height=630)
        self.heading.config(text="TRANSACTION HISTORY")
        TransactHistory(self.trans_hist_frame)

    def pay_history(self):
        self.hide_widgets()
        self.pay_hist_frame.place(x=10, y=50, width=1050, height=630)
        self.heading.config(text="PAYMENT HISTORY")
        PaymentHistory(self.pay_hist_frame)

    def user_settings(self):
        self.hide_widgets()
        self.user_frame.place(x=10, y=50, width=1050, height=630)
        self.heading.config(text="USER SETTINGS")
        UserSettingsFrame(self.user_frame)

    def logout(self):
        if messagebox.askyesno("Log-out", "Do you want to log out?"):
            self.frame.destroy()
            LogIn()

    def exit_handler(self):
        if messagebox.askyesno("Exit", "Do you want to exit?"):
            self.frame.destroy()
        else:
            return


class SalesRegister:
    def __init__(self, c_uname):
        self.POS_window = Tk()
        self.cash_uname = c_uname

        self.POS_window.title("The Hideout Sales Register")
        self.POS_window.geometry("1350x690+0+0")
        self.POS_window.resizable(False, False)
        self.POS_window.iconbitmap(r"images\logo.ico")

        self.prod_id = StringVar()
        self.trans_id = StringVar()
        self.edit_quant = IntVar()
        self.price_prod = DoubleVar()
        self.disc_amount = DoubleVar()
        self.disc_perc = DoubleVar()
        self.sub_tot = DoubleVar()
        self.total_cost = DoubleVar()
        self.amount_paid = DoubleVar()
        self.change_amt = DoubleVar()

        self.heading_frame = Frame(self.POS_window, bg="#3b3b3b")
        self.heading_frame.place(x=0, y=0, height=60, width=1350)
        self.logo = PhotoImage(file=r"images\logo.png").subsample(9, 9)

        label_logo = Label(self.heading_frame, image=self.logo, bg="white")
        label_logo.img = self.logo
        label_logo.place(x=3, y=3, width=52, height=52)

        pos_label = Label(self.heading_frame, bg="#3b3b3b", fg="white", font=("Blinker", 12, "bold"),
                          text="The Hideout  Point-of Sale System")
        pos_label.place(x=60, y=5, height=25)
        cash_name_label = Label(self.heading_frame, bg="#3b3b3b", fg="white", font=("Blinker", 12, "bold"),
                                text=("Cashier   |    " + self.cash_uname))
        cash_name_label.place(x=60, y=30, height=25)

        self.total_cost_label = Label(self.heading_frame, fg="yellow green", bg="#3b3b3b", font=("Calibri", 38, "bold"),
                                      text="0.00", anchor="e")
        self.total_cost_label.place(x=1180, y=2, width=150, height=56)

        sales_frame = Frame(self.POS_window, bg="white")
        sales_frame.place(x=0, y=60, width=1050, height=630)

        trans_code_label = Label(sales_frame, text="TRANSACTION NO.: ", anchor="w", font=("Calibri", 11, "bold"),
                                 bg="white", fg="black")
        trans_code_label.place(x=25, y=10, height=20, width=150)
        self.trans_code = Label(sales_frame, text="", anchor="w", font=("Calibri", 11, "bold"), bg="white", fg="green")
        self.trans_code.place(x=180, y=10, height=20, width=200)
        trans_date_label = Label(sales_frame, text="TRANSACTION DATE: ", anchor="w", font=("Calibri", 11, "bold"),
                                 bg="white", fg="black")
        trans_date_label.place(x=520, y=10, height=20, width=150)
        self.trans_date = Label(sales_frame, text="", anchor="w", font=("Calibri", 11, "bold"), bg="white", fg="blue")
        self.trans_date.place(x=680, y=10, height=20, width=200)
        ent_prod_id_label = Label(sales_frame, text="PRODUCT ID: ", anchor="w", font=("Calibri", 11, "bold"),
                                  bg="white", fg="black")
        ent_prod_id_label.place(x=25, y=40, height=20, width=100)
        prod_id_ent = Entry(sales_frame, textvariable=self.prod_id, highlightthickness=1, highlightbackground="black",
                            font=("Calibri", 11, "bold"))
        prod_id_ent.place(x=125, y=40, height=20, width=375)
        add_img = PhotoImage(file=r"images\add.png").subsample(2, 2)
        add_prod_btn = Button(sales_frame, command=self.add_prod, image=add_img, relief=FLAT)
        add_prod_btn.img = add_img
        add_prod_btn.place(x=505, y=40, height=20, width=40)
        remove_img = PhotoImage(file=r"images\remove.png").subsample(2, 2)
        remove_prod_btn = Button(sales_frame, command=self.remove_prod, image=remove_img, relief=FLAT)
        remove_prod_btn.img = remove_img
        remove_prod_btn.place(x=550, y=40, height=20, width=40)

        trans_reg_frame = Frame(sales_frame, bg="white", highlightbackground="black", highlightthickness=2)
        trans_reg_frame.place(x=10, y=70, width=1030, height=450)

        reg_y = Scrollbar(trans_reg_frame, orient=VERTICAL)
        self.trans_reg_table = ttk.Treeview(trans_reg_frame, columns=("prod_id", "prod_name", "prod_price",
                                                                      "quantity", "discount", "subtotal"))
        heading_bg = ttk.Style()
        heading_bg.theme_use("clam")
        heading_bg.configure('Treeview.Heading', background="black", foreground="white", font=("Bebas Neue", 13))

        self.trans_reg_table.config(yscrollcommand=reg_y)
        reg_y.pack(side=RIGHT, fill=Y)
        reg_y.config(command=self.trans_reg_table.yview)
        self.trans_reg_table.heading("prod_id", text="ID")
        self.trans_reg_table.heading("prod_name", text="NAME")
        self.trans_reg_table.heading("prod_price", text="PRICE")
        self.trans_reg_table.heading("quantity", text="QUANTITY")
        self.trans_reg_table.heading("discount", text="DISCOUNT")
        self.trans_reg_table.heading("subtotal", text="SUBTOTAL")
        self.trans_reg_table['show'] = 'headings'
        self.trans_reg_table.column("prod_id", width=170)
        self.trans_reg_table.column("prod_name", width=410)
        self.trans_reg_table.column("prod_price", width=100)
        self.trans_reg_table.column("quantity", width=100)
        self.trans_reg_table.column("discount", width=100)
        self.trans_reg_table.column("subtotal", width=130)
        self.trans_reg_table.pack(fill=BOTH, expand=1)
        self.trans_reg_table.bind("<Double-1>", self.edit_qty_frame)

        self.time_label = Label(sales_frame, font=("Blinker", 50, "bold"), anchor='w', bg="white")
        self.time_label.place(x=10, y=520, width=400, height=75)
        self.time()
        date_label = Label(sales_frame, font=("Helvetica", 15, "bold"), text=f"{dt.datetime.now():%a, %b %d %Y}",
                           bg="white", anchor="w")
        date_label.place(x=10, y=595, height=30, width=450)

        sales_tot_lbl = Label(sales_frame, font=("Calibri", 11), text="SALES TOTAL", bg="white")
        sales_tot_lbl.place(width=100, height=35, x=710, y=520)
        self.sales_amt = Label(sales_frame, font=("Calibri", 11, "bold"), text="0.00", anchor="e", bg="white")
        self.sales_amt.place(width=200, height=35, x=810, y=520)
        vat_lbl = Label(sales_frame, font=("Calibri", 11), text="VAT", bg="white")
        vat_lbl.place(width=100, height=35, x=710, y=555)
        self.vat_amt = Label(sales_frame, font=("Calibri", 11, "bold"), text="0.00", anchor="e", bg="white")
        self.vat_amt.place(width=200, height=35, x=810, y=555)
        vatable_lbl = Label(sales_frame, font=("Calibri", 11), text="VATABLE", bg="white")
        vatable_lbl.place(width=100, height=35, x=710, y=590)
        self.vatable_amt = Label(sales_frame, font=("Calibri", 11, "bold"), text="0.00", anchor="e", bg="white")
        self.vatable_amt.place(width=200, height=35, x=810, y=590)

        feature_frame = Frame(self.POS_window, bg="white")
        feature_frame.place(height=630, width=298, x=1050, y=62)
        
        new_trans_img = PhotoImage(file=r"images\newtrans.png").subsample(2, 2)
        add_disc_img = PhotoImage(file=r"images\adddisc.png").subsample(2, 2)
        clear_cart_img = PhotoImage(file=r"images\clearcart.png").subsample(2, 2)
        set_pay_img = PhotoImage(file=r"images\setpay.png").subsample(2, 2)
        log_out_img = PhotoImage(file=r"images\logout.png").subsample(2, 2)
        
        new_trans_btn = Button(feature_frame, bg="#38b6ff", fg="white", text="   NEW TRANSACTION", relief=FLAT,
                               font=("Blinker", 15, "bold"), activebackground="#38b6ff", activeforeground="white",
                               command=self.new_transact, image=new_trans_img, anchor="w", compound="left")
        new_trans_btn.img = new_trans_img
        add_disc_btn = Button(feature_frame, bg="#38b6ff", fg="white", text="   ADD DISCOUNT", relief=FLAT,
                              font=("Blinker", 15, "bold"), activebackground="#38b6ff", activeforeground="white",
                              command=self.add_discount_frame, image=add_disc_img, anchor="w", compound="left")
        add_disc_btn.img = add_disc_img
        clear_cart_btn = Button(feature_frame, bg="#38b6ff", fg="white", text="   CLEAR CART", relief=FLAT,
                                font=("Blinker", 15, "bold"), activebackground="#38b6ff", activeforeground="white",
                                command=self.clear_cart, image=clear_cart_img, anchor="w", compound="left")
        clear_cart_btn.img = clear_cart_img
        set_pay_btn = Button(feature_frame, bg="#38b6ff", fg="white", text="   SETTLE PAYMENT", relief=FLAT,
                             font=("Blinker", 15, "bold"), activebackground="#38b6ff", activeforeground="white",
                             command=self.set_pay_frame, image=set_pay_img, anchor="w", compound="left")
        set_pay_btn.img = set_pay_img
        log_out_btn = Button(feature_frame, bg="#38b6ff", fg="white", text="   LOG OUT", relief=FLAT,
                             font=("Blinker", 15, "bold"), activebackground="#38b6ff", activeforeground="white",
                             command=self.log_out, image=log_out_img,  anchor="w", compound="left")
        log_out_btn.img = log_out_img

        new_trans_btn.place(x=0, y=5, height=45, width=295)
        add_disc_btn.place(x=0, y=50, height=45, width=295)
        clear_cart_btn.place(x=0, y=95, height=45, width=295)
        set_pay_btn.place(x=0, y=140, height=45, width=295)
        log_out_btn.place(x=0, y=185, height=45, width=295)

        search_lbl = Label(feature_frame, bg="white", fg="#38b6ff", font=("Blinker", 15, "bold"),
                           text="LIST OF PRODUCTS")
        search_lbl.place(x=0, y=255, height=25, width=295)

        self.prod_name_search = StringVar()
        srch_prod_img = PhotoImage(file=r"images\blacksearch.png").subsample(2, 2)
        lbl_srch_name = Label(feature_frame, image=srch_prod_img, text="  Name", bg="#0a100d", fg="white",
                              font=("Bebas Neue", 14), anchor='w', compound='left')
        lbl_srch_name.place(x=0, y=295, width=75, height=25)
        lbl_srch_name.img = srch_prod_img
        search_prod_ent = Entry(feature_frame, highlightthickness=1, highlightbackground="#0a100d",
                                font=("Calibri", 13, "bold"), textvariable=self.prod_name_search)
        search_prod_ent.place(width=215, height=25, x=75, y=295)
        self.prod_name_search.trace("w", lambda name, index, mode,
                                    sv=self.prod_name_search: self.search_prod())

        self.prod_list_frame = Frame(feature_frame, bg="green")
        self.prod_list_frame.place(x=0, y=330, height=280, width=295)

        scr_y = Scrollbar(self.prod_list_frame, orient=VERTICAL)
        self.prod_list = ttk.Treeview(self.prod_list_frame, columns=("prod_id", "prod_name"))
        self.prod_list.config(yscrollcommand=scr_y)
        scr_y.pack(side=RIGHT, fill=Y)
        scr_y.config(command=self.prod_list.yview)

        self.prod_list.heading("prod_id", text="PRODUCT ID")
        self.prod_list.heading("prod_name", text="NAME")
        self.prod_list['show'] = 'headings'
        self.prod_list.column("prod_id", width=90)
        self.prod_list.column("prod_name", width=150)
        self.prod_list.pack(fill=BOTH, expand=1)
        self.prod_list.bind("<Double-1>", self.add_prod_dbclick)

        self.search_prod()

        self.POS_window.protocol("WM_DELETE_WINDOW", self.exit_handler)
        self.conf_img = PhotoImage(file=r"images\confirm.png").subsample(2, 2)

    def refresh(self):
        self.prod_id.set("")
        self.trans_reg_show()
        self.show_total()

    def new_transact(self):
        trans_date = f"{dt.datetime.now():%a, %b %d %Y}"
        if self.trans_id.get() != "":
            if messagebox.askyesno("Add Another Transaction", "Do you want to add another transaction? You have not "
                                                              "paid the current transaction yet! Clicking 'Yes' would "
                                                              "cancel the transaction!"):
                POSdatabase.delete_transact(self.trans_id.get())
                self.trans_id.set(POSdatabase.add_new_transact(trans_date, self.cash_uname))
                self.trans_code.config(text=self.trans_id.get())
                self.trans_date.config(text=trans_date)
        else:
            self.trans_id.set(POSdatabase.add_new_transact(trans_date, self.cash_uname))
            self.trans_code.config(text=self.trans_id.get())
            self.trans_date.config(text=trans_date)
        self.refresh()
        self.amount_paid.set = 0.0

    def add_prod(self):
        if self.trans_id.get() == "":
            messagebox.showerror("Transaction Error", "Add a new transaction first!")
            return
        elif self.prod_id.get() == "":
            messagebox.showerror("Add Product Error", "Invalid Product ID")
            return
        else:
            prod = POSdatabase.search_prod_db_by_id(self.prod_id.get().upper())
            if not prod:
                messagebox.showerror("Add Product Error", "Invalid Product ID")
                return
            else:
                POSdatabase.add_prod_to_trans(self.trans_id.get(), prod[0], prod[3], 1, 0)
                self.refresh()

    def add_prod_dbclick(self, ev):
        item = self.prod_list.focus()
        contents = self.prod_list.item(item)
        if self.trans_id.get() == "":
            messagebox.showerror("Transaction Error", "Add a new transaction first!")
            return
        else:
            prod_det = POSdatabase.search_prod_db_by_id(contents['values'][0])
            POSdatabase.add_prod_to_trans(self.trans_id.get(), prod_det[0], prod_det[3], 1, 0)
            self.refresh()

    def trans_reg_show(self):
        reg = POSdatabase.trans_product_show(self.trans_id.get())
        self.trans_reg_table.delete(*self.trans_reg_table.get_children())
        if not reg:
            return
        else:
            for x in reg:
                prod_name = POSdatabase.search_prod_db_by_id(x[1])[1]
                self.trans_reg_table.insert('', END, values=(x[1], prod_name, x[2], x[3], x[4], x[5]))

    def edit_qty_frame(self, ev):
        item = self.trans_reg_table.focus()
        contents = self.trans_reg_table.item(item)
        prod_sel = contents['values']

        if not prod_sel:
            messagebox.showerror("Edit Quantity Error", "Select a product in the transaction first!")
            return
        else:
            self.edit_quant_window = Toplevel()
            self.edit_quant_window.title("Edit Quantity")
            self.edit_quant_window.geometry("420x210+465+240")
            self.edit_quant_window.resizable(False, False)
            self.edit_quant_window.config(bg="white")
            self.edit_quant_window.iconbitmap(r"images\logo.ico")

            self.edit_quant.set(prod_sel[3])
            self.price_prod.set(prod_sel[2])
            self.prod_id.set(prod_sel[0])

            label_name = Label(self.edit_quant_window, text="Product Name: ", font=("Bebas Neue", 17), bg="black",
                               fg="white")
            label_name.place(x=10, y=10, width=150, height=30)
            prod_name = Entry(self.edit_quant_window, font=("Bebas Neue", 16), bg="white", fg="black")
            prod_name.insert(0, prod_sel[1])
            prod_name.place(x=160, y=10, height=30, width=250)
            prod_name.config(state=DISABLED)
            label_price = Label(self.edit_quant_window, text="Price: ", font=("Bebas Neue", 17), bg="black", fg="white")
            label_price.place(x=10, y=50, width=150, height=30)
            prod_price = Entry(self.edit_quant_window, font=("Bebas Neue", 16), bg="white", fg="black",
                               textvariable=self.price_prod)
            prod_price.place(x=160, y=50, height=30, width=250)
            prod_price.config(state=DISABLED)
            label_quant = Label(self.edit_quant_window, text="Quantity: ", font=("Bebas Neue", 17), bg="black",
                                fg="white")
            label_quant.place(x=10, y=90, width=150, height=30)
            prod_qty = Entry(self.edit_quant_window, textvariable=self.edit_quant, highlightbackground="black",
                             highlightthickness=2, font=("Bebas Neue", 16))
            prod_qty.place(x=160, y=90, height=30, width=250)
            label_subtotal = Label(self.edit_quant_window, text="Subtotal: ", font=("Bebas Neue", 17), bg="black",
                                   fg="white")
            label_subtotal.place(x=10, y=130, width=150, height=30)
            self.subtotal = Label(self.edit_quant_window, anchor='w', font=("Bebas Neue", 17), bg="white", fg="black",
                                  text=self.price_prod.get() * self.edit_quant.get())
            self.subtotal.place(x=160, y=130, height=30, width=250)

            edit_quantity_btn = Button(self.edit_quant_window, command=self.edit_quantity, image=self.conf_img)
            edit_quantity_btn.img = self.conf_img
            edit_quantity_btn.place(x=310, y=170, width=100, height=30)

            self.edit_quant.trace("w", lambda name, index, mode, sv=self.edit_quant: self.edit_quant_auto_subtotal())

    def edit_quant_auto_subtotal(self):
        try:
            self.subtotal.config(text=(self.price_prod.get() * self.edit_quant.get()))
        except TclError:
            self.subtotal.config(text="Error!")

    def edit_quantity(self):
        try:
            POSdatabase.edit_quantity(self.trans_id.get(), self.prod_id.get(), self.edit_quant.get())
            self.edit_quant.set(0)
            self.edit_quant_window.destroy()
            self.refresh()
            return
        except TclError:
            messagebox.showerror("Error", "Input valid quantity.")
            return

    def remove_prod(self):
        selected = self.trans_reg_table.focus()
        contents = self.trans_reg_table.item(selected)
        prod_trans_sel = contents['values']
        if not prod_trans_sel:
            messagebox.showerror("Error", "Choose a product first.")
            return
        else:
            POSdatabase.remove_prod_from_trans(self.trans_id.get(), prod_trans_sel[0])
            self.refresh()
            return
        
    def search_prod(self):
        res_prod = POSdatabase.search_prod_db_by_name(self.prod_name_search.get())
        self.prod_list.delete(*self.prod_list.get_children())
        if not res_prod:
            return
        else:
            for prod in res_prod:
                self.prod_list.insert('', END, values=(prod[0], prod[1]))

    def add_discount_frame(self):
        item = self.trans_reg_table.focus()
        contents = self.trans_reg_table.item(item)
        prod_sel = contents['values']

        if not prod_sel:
            messagebox.showerror("Error", "Please select an item in the register first!")
            return
        else:
            self.add_disc_window = Toplevel()
            self.add_disc_window.title("Add Discount")
            self.add_disc_window.geometry("350x180+500+240")
            self.add_disc_window.resizable(False, False)
            self.add_disc_window.config(bg="white")
            self.add_disc_window.iconbitmap(r"images\logo.ico")
            self.sub_tot.set(prod_sel[5])
            self.prod_id.set(prod_sel[0])

            total_label = Label(self.add_disc_window, text="Subtotal", font=("Bebas Neue", 14), bg="black", fg="white")
            total = Entry(self.add_disc_window, textvariable=self.sub_tot, highlightbackground="black",
                          highlightthickness=2, font=("Bebas Neue", 14))
            disc_perc_label = Label(self.add_disc_window, text="% Discount", font=("Bebas Neue", 14), bg="black",
                                    fg="white")
            disc_perc = Entry(self.add_disc_window, textvariable=self.disc_perc, highlightbackground="black",
                              highlightthickness=2, font=("Bebas Neue", 14))
            disc_amt_label = Label(self.add_disc_window, text="Amount", font=("Bebas Neue", 14), bg="black",
                                   fg="white")
            disc_amt = Entry(self.add_disc_window, textvariable=self.disc_amount, highlightbackground="black",
                             highlightthickness=2, font=("Bebas Neue", 14))

            total_label.place(x=10, y=30, width=100, height=30)
            disc_perc_label.place(x=10, y=65, width=100, height=30)
            disc_amt_label.place(x=10, y=100, width=100, height=30)
            total.place(x=110, y=30, width=230, height=30)
            total.config(state=DISABLED)
            disc_perc.place(x=110, y=65, width=230, height=30)
            disc_amt.place(x=110, y=100, width=230, height=30)

            add_disc_btn = Button(self.add_disc_window, command=self.add_discount, image=self.conf_img)
            add_disc_btn.img = self.conf_img
            add_disc_btn.place(width=100, height=30, x=240, y=140)

            self.disc_perc.trace("w", lambda name, index, mode, sv=self.disc_perc: self.add_disc_auto_amt())

    def add_disc_auto_amt(self):
        try:
            if self.disc_perc.get() < 0 or self.disc_perc.get() > 100:
                self.disc_amount.set("Error!")
            elif self.disc_perc.get() > 1:
                self.disc_amount.set((self.disc_perc.get()/100) * self.sub_tot.get())
            else:
                self.disc_amount.set(self.disc_perc.get() * self.sub_tot.get())
        except TclError:
            self.disc_amount.set("Error!")

    def add_discount(self):
        try:
            if messagebox.askyesno("Add Discount", "Confirm adding discount?"):
                POSdatabase.add_discount(self.trans_id.get(), self.prod_id.get(), self.disc_amount.get())
                self.disc_amount.set(0)
                self.disc_perc.set(0)
                self.add_disc_window.destroy()
                self.refresh()
                return
            else:
                return
        except TclError:
            messagebox.showerror("Error", "Input valid discount percent.")
            return

    def show_total(self):
        stot = POSdatabase.total_cost(self.trans_id.get())
        total = 0.0
        for x in stot:
            total += x[0]
        self.total_cost.set(total)
        self.total_cost_label.config(text=self.total_cost.get())
        self.sales_amt.config(text=total)
        self.vat_amt.config(text=total * 0.12)
        self.vatable_amt.config(text=total*0.88)

    def clear_cart(self):
        POSdatabase.clear_cart(self.trans_id.get())
        self.refresh()

    def set_pay_frame(self):
        if self.total_cost.get() == 0:
            messagebox.showerror("Error", "Please add items in the transaction!")
            return
        else:
            self.set_pay_window = Toplevel()
            self.set_pay_window.title("Settle Payment")
            self.set_pay_window.geometry("350x170+500+260")
            self.set_pay_window.resizable(False, False)
            self.set_pay_window.config(bg="white")
            self.set_pay_window.iconbitmap(r"images\logo.ico")

            total_lbl = Label(self.set_pay_window, text="Total Cost", font=("Bebas Neue", 14), bg="black", fg="white")
            total_amt = Entry(self.set_pay_window, textvariable=self.total_cost, highlightbackground="black",
                              highlightthickness=2, font=("Bebas Neue", 14))
            amount_lbl = Label(self.set_pay_window, text="Amount Paid", font=("Bebas Neue", 14), bg="black", fg="white")
            amount = Entry(self.set_pay_window, textvariable=self.amount_paid, highlightbackground="black",
                           highlightthickness=2, font=("Bebas Neue", 14))
            change_lbl = Label(self.set_pay_window, text="Change", font=("Bebas Neue", 14), bg="black", fg="white")
            self.change = Entry(self.set_pay_window, textvariable=self.change_amt, highlightbackground="black",
                                highlightthickness=2, font=("Bebas Neue", 14))

            total_lbl.place(x=10, y=20, height=30, width=100)
            total_amt.place(x=110, y=20, height=30, width=230)
            total_amt.config(state=DISABLED)
            amount_lbl.place(x=10, y=55, width=100, height=30)
            amount.place(x=110, y=55, width=230, height=30)
            change_lbl.place(x=10, y=90, width=100, height=30)
            self.change.place(x=110, y=90, width=230, height=30)
            self.change_amt.set((self.amount_paid.get()-self.total_cost.get()))
            self.change.config(state=DISABLED)

            conf_pay = Button(self.set_pay_window, command=self.settle_payment, image=self.conf_img)
            conf_pay.img = self.conf_img
            conf_pay.place(width=100, height=30, x=240, y=130)

            self.amount_paid.trace("w", lambda name, index, mode, sv=self.amount_paid: self.set_pay_auto_change())

    def set_pay_auto_change(self):
        self.change.config(state=NORMAL)
        try:
            self.change_amt.set((self.amount_paid.get() - self.total_cost.get()))
        except TclError:
            self.change_amt.set("ERROR!")
        self.change.config(state=DISABLED)

    def settle_payment(self):
        pay_date = f"{dt.datetime.now():%a, %b %d %Y}"
        try:
            if self.amount_paid.get() < self.total_cost.get():
                messagebox.showerror("Payment Error", "Invalid payment amount")
                return
            else:
                if messagebox.askyesno("Settle Payment", "Do you want to account the payment?"):
                    POSdatabase.add_payment(self.trans_id.get(), pay_date, self.amount_paid.get(),
                                            self.total_cost.get())
                    messagebox.showinfo("Success", "Payment has been accounted!")
                    self.set_pay_window.destroy()
                    self.trans_id.set("")
                    self.trans_code.config(text="")
                    self.trans_date.config(text="")
                    self.new_transact()
                    return
                else:
                    return
        except TclError:
            messagebox.showerror("Payment Error", "Invalid payment amount")
            return

    def log_out(self):
        if self.trans_id.get() != "":
            if messagebox.showwarning("Unfinished Transaction", "Do you want to log out? You have not "
                                      "paid the current transaction yet. Clicking 'Yes' would "
                                      "cancel the transaction."):
                POSdatabase.delete_transact(self.trans_id.get())
            else:
                return
        if messagebox.askyesno("Log-out", "Do you want to log out?"):
            self.POS_window.destroy()
            LogIn()

    def time(self):
        string = strftime('%I:%M:%S %p')
        self.time_label.config(text=string)
        self.time_label.after(200, self.time)

    def exit_handler(self):
        if self.trans_id.get() != "":
            if messagebox.askyesno("Unfinished Transaction", "Do you want to exit? You have not paid the current "
                                                             "transaction yet. Clicking 'Yes' would cancel the "
                                                             "transaction."):
                POSdatabase.delete_transact(self.trans_id.get())
            else:
                return
        self.POS_window.destroy()


LogIn()
