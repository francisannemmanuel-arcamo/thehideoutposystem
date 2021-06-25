from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import sqlite3
import POSdatabase


class UserSettingsFrame:
    def __init__(self, frame):
        self.user_frame = frame

        self.admin_old_pass = StringVar()
        self.admin_new_pass = StringVar()
        self.admin_re_ent_pass = StringVar()

        self.rows = []

        self.cash_username = StringVar()
        self.cash_pass = StringVar()
        self.cash_re_ent_pass = StringVar()
        self.cash_role = StringVar()

        self.search_user = StringVar()

        self.change_pass_admin_frame()

        self.cashier_user_frame = Frame(self.user_frame, bg="white", highlightcolor="black", highlightthickness=2)
        self.cashier_user_frame.place(x=10, y=10, width=500, height=300)

        user_details_label = Label(self.cashier_user_frame, text="USER DETAILS",
                                   font=("Blinker", 15, "underline", "bold"), bg="white")
        user_details_label.place(x=10, y=5, height=40)

        self.add_user_img = PhotoImage(file=r"images\adduser.png")
        self.edit_user_img = PhotoImage(file=r"images\upduser.png")
        self.delete_user_img = PhotoImage(file=r"images\deluser.png")

        add_img = self.add_user_img.subsample(4, 4)
        edit_img = self.edit_user_img.subsample(4, 4)
        del_img = self.delete_user_img.subsample(4, 4)

        self.add_user_button = Button(self.cashier_user_frame, image=add_img, command=self.add_user_gui, relief=FLAT,
                                      bg="black", fg="white")
        self.add_user_button.img = add_img
        self.edit_user_button = Button(self.cashier_user_frame, image=edit_img, command=self.edit_user_gui, relief=FLAT,
                                       bg="black", fg="white")
        self.edit_user_button.img = edit_img
        self.delete_user_button = Button(self.cashier_user_frame, image=del_img, command=self.delete_user, relief=FLAT,
                                         bg="black", fg="white")
        self.delete_user_button.img = del_img

        user_view_table_frame = Frame(self.user_frame, bg="white", highlightcolor="black", highlightthickness=2)
        user_view_table_frame.place(x=520, y=10, height=610, width=520)
        user_list_label = Label(user_view_table_frame, text="USER LIST", font=("Blinker", 15, "underline", "bold"),
                                bg="white")
        user_list_label.place(x=10, y=5, height=40)
        srch_icon = PhotoImage(file=r"images\blacksearch.png").subsample(2, 2)
        srch_cuname_lbl = Label(user_view_table_frame, bg="#0A100d", fg="white", font=("Bebas Neue", 14),
                                image=srch_icon, text=" USERNAME", compound="left", anchor="w")
        srch_cuname_lbl.img = srch_icon
        srch_cuname_lbl.place(width=100, x=210, height=30, y=40)
        user_search_entry = Entry(user_view_table_frame, textvariable=self.search_user, font=("Blinker", 15),
                                  highlightbackground="black", highlightthickness=2)
        user_search_entry.place(x=310, y=40, height=30, width=200)

        user_table_frame = Frame(user_view_table_frame)
        user_table_frame.place(x=10, y=80, width=500, height=520)

        x = Scrollbar(user_table_frame, orient=HORIZONTAL)
        y = Scrollbar(user_table_frame, orient=VERTICAL)

        self.user_table = ttk.Treeview(user_table_frame, columns=("username", "password"))
        heading_bg = ttk.Style()
        heading_bg.theme_use("clam")
        heading_bg.configure('Treeview.Heading', background="black", foreground="white", font=("Bebas Neue", 13))

        self.user_table.config(xscrollcommand=x, yscrollcommand=y)
        x.pack(side=BOTTOM, fill=X)
        y.pack(side=RIGHT, fill=Y)
        x.config(command=self.user_table.xview)
        y.config(command=self.user_table.yview)
        self.user_table.heading("username", text="CASHIER USERNAME")
        self.user_table.heading("password", text="CASHIER PASSWORD")
        self.user_table['show'] = 'headings'
        self.user_table.column("password", anchor="center")
        self.user_table.pack(fill=BOTH, expand=1)

        self.features_frame = Frame(self.cashier_user_frame, bg="white")
        self.add_user_frame = Frame(self.cashier_user_frame, bg="white")
        self.edit_user_frame = Frame(self.cashier_user_frame, bg="white")

        self.search_user.trace("w", lambda name, index, mode, sv=self.search_user: self.display_users_search())
        self.display_users_search()
        self.user_features()

    def hide_widgets(self):
        self.features_frame.place_forget()
        self.add_user_frame.place_forget()
        self.edit_user_frame.place_forget()

        self.add_user_button.place(x=355, y=10, width=35, height=35)
        self.edit_user_button.place(x=400, y=10, width=35, height=35)
        self.delete_user_button.place(x=445, y=10, width=35, height=35)
        self.clear_data()

    def user_features(self):
        self.hide_widgets()
        self.add_user_button.place_forget()
        self.edit_user_button.place_forget()
        self.delete_user_button.place_forget()

        self.features_frame.place(x=10, y=60, width=480, height=230)
        add_user_btn = Button(self.features_frame, bg="black", fg="white", image=self.add_user_img,
                              command=self.add_user_gui)
        add_user_btn.img = self.add_user_img
        add_user_btn.place(x=20, y=25, width=140, height=140)
        add_label = Label(self.features_frame, bg="white", fg="black", text="Add User", font=("Blinker", 14, "bold"))
        add_label.place(x=20, y=170, width=140)

        edit_user_btn = Button(self.features_frame, bg="black", fg="white", image=self.edit_user_img,
                               command=self.edit_user_gui)
        edit_user_btn.img = self.edit_user_img
        edit_user_btn.place(x=170, y=25, width=140, height=140)
        edit_label = Label(self.features_frame, bg="white", fg="black", text="Edit User", font=("Blinker", 14, "bold"))
        edit_label.place(x=170, y=170, width=140)

        delete_user_btn = Button(self.features_frame, bg="black", fg="white", image=self.delete_user_img,
                                 command=self.delete_user)
        delete_user_btn.img = self.delete_user_img
        delete_user_btn.place(x=320, y=25, width=140, height=140)
        delete_label = Label(self.features_frame, bg="white", fg="black", text="Delete User",
                             font=("Blinker", 14, "bold"))
        delete_label.place(x=320, y=170, width=140)

    def add_user_gui(self):
        self.user_table.unbind("<ButtonRelease-1>")
        self.hide_widgets()
        self.add_user_frame.place(x=10, y=60, width=480, height=230)

        label = Label(self.add_user_frame, text="ADD USER", fg="white", bg="black", font=("Blinker", 15, "bold"))
        label.place(x=190, y=10, height=30, width=100)

        add_username_label = Label(self.add_user_frame, text="Username", bg="black", fg="white",
                                   font=("Bebas Neue", 15))
        add_username_label.place(x=10, y=50, height=30, width=100)
        add_username_entry = Entry(self.add_user_frame, font=("Blinker", 13), highlightbackground="black",
                                   highlightthickness=2, textvariable=self.cash_username)
        add_username_entry.place(x=110, y=50, width=350, height=30)

        add_pass_label = Label(self.add_user_frame, text="Password", bg="black", fg="white", font=("Bebas Neue", 15))
        add_pass_label.place(x=10, y=85, height=30, width=100)
        add_pass_entry = Entry(self.add_user_frame, font=("Blinker", 13), highlightbackground="black", show="*",
                               highlightthickness=2, textvariable=self.cash_pass)
        add_pass_entry.place(x=110, y=85, height=30, width=350)
        add_re_ent_pass_label = Label(self.add_user_frame, text="Re-Enter Password", bg="black", fg="white",
                                      font=("Bebas Neue", 13))
        add_re_ent_pass_label.place(x=10, y=120, height=30, width=120)
        add_re_ent_pass_entry = Entry(self.add_user_frame, font=("Blinker", 13), highlightbackground="black", show="*",
                                      highlightthickness=2, textvariable=self.cash_re_ent_pass)
        add_re_ent_pass_entry.place(x=130, y=120, height=30, width=330)

        add_role_label = Label(self.add_user_frame, text="Role",  bg="black", fg="white", font=("Bebas Neue", 13))
        add_role_label.place(x=10, y=170, width=40, height=30)
        roles_combo = ttk.Combobox(self.add_user_frame, textvariable=self.cash_role, font=("Bebas Neue", 13),
                                   values=["admin", "clerk"])
        roles_combo.place(x=50, y=170, width=100, height=30)
        add_button = Button(self.add_user_frame, command=self.add_user, text="ADD", bg="black", fg="white",
                            activebackground="black", activeforeground="white", font=("Bebas Neue", 17))
        add_button.place(x=300, y=170, height=30, width=70)
        clear_button = Button(self.add_user_frame, command=self.clear_data, text="CLEAR", bg="black", fg="white",
                              activebackground="black", activeforeground="white", font=("Bebas Neue", 17))
        clear_button.place(x=380, y=170, height=30, width=70)

    def add_user(self):
        if (self.cash_username.get() == "" or self.cash_pass.get() == "" or self.cash_re_ent_pass.get() == ""
                or self.cash_role.get() == ""):
            messagebox.showerror("Add User Error", "Please fill out all fields")
            return
        elif self.cash_pass.get() != self.cash_re_ent_pass.get():
            messagebox.showerror("Add User Error", "Password do not match")
            return
        else:
            if self.cash_role.get() == "admin":
                messagebox.showwarning("Warning", "You are adding a user as an admin! ")
            if messagebox.askyesno("Add User", "Do you want to add the user? They can log in into the POS System."):
                if POSdatabase.add_user_db(self.cash_username.get(), self.cash_pass.get(), self.cash_role.get()):
                    self.clear_data()
                    messagebox.showinfo("Add Success", "User added to database")
                    self.display_users_search()

    def edit_user_gui(self):
        self.user_table.bind("<ButtonRelease-1>", self.select_user)
        self.rows = []
        self.hide_widgets()
        self.edit_user_frame.place(x=10, y=60, width=480, height=230)

        label = Label(self.edit_user_frame, text="EDIT USER", fg="white", bg="black", font=("Blinker", 15, "bold"))
        label.place(x=190, y=10, height=30, width=100)

        username_label = Label(self.edit_user_frame, text="Username", bg="black", fg="white", font=("Bebas Neue", 15))
        username_label.place(x=10, y=50, height=30, width=100)
        username_entry = Entry(self.edit_user_frame, font=("Blinker", 13), highlightbackground="black",
                               highlightthickness=2, textvariable=self.cash_username)
        username_entry.place(x=110, y=50, width=350, height=30)

        pass_label = Label(self.edit_user_frame, text="Password", bg="black", fg="white", font=("Bebas Neue", 15))
        pass_label.place(x=10, y=85, height=30, width=100)
        pass_entry = Entry(self.edit_user_frame, font=("Blinker", 13), highlightbackground="black", show="*",
                           highlightthickness=2, textvariable=self.cash_pass)
        pass_entry.place(x=110, y=85, height=30, width=350)
        re_ent_pass_label = Label(self.edit_user_frame, text="Re-Enter Password", bg="black", fg="white",
                                  font=("Bebas Neue", 13))
        re_ent_pass_label.place(x=10, y=120, height=30, width=120)
        re_ent_pass_entry = Entry(self.edit_user_frame, font=("Blinker", 13), highlightbackground="black", show="*",
                                  highlightthickness=2, textvariable=self.cash_re_ent_pass)
        re_ent_pass_entry.place(x=130, y=120, height=30, width=330)
        edit_role_label = Label(self.add_user_frame, text="Role", bg="black", fg="white", font=("Bebas Neue", 13))
        edit_role_label.place(x=10, y=170, width=40, height=30)
        roles_combo = ttk.Combobox(self.edit_user_frame, textvariable=self.cash_role, font=("Bebas Neue", 13),
                                   values=["admin", "clerk"])
        roles_combo.place(x=50, y=170, width=100, height=30)

        edit_button = Button(self.edit_user_frame, command=self.update_user, text="UPDATE", bg="black", fg="white",
                             activebackground="black", activeforeground="white", font=("Bebas Neue", 17))
        edit_button.place(x=300, y=170, height=30, width=70)
        clear_button = Button(self.edit_user_frame, command=self.clear_data, text="CLEAR", bg="black", fg="white",
                              activebackground="black", activeforeground="white", font=("Bebas Neue", 17))
        clear_button.place(x=380, y=170, height=30, width=70)

    def update_user(self):
        if (self.cash_username.get() == "" or self.cash_pass.get() == "" or self.cash_re_ent_pass.get() == ""
                or self.cash_role.get() == ""):
            messagebox.showerror("Update User Error", "Please fill out all fields")
            return
        elif self.cash_pass.get() != self.cash_re_ent_pass.get():
            messagebox.showerror("Update User Error", "Password do not match")
            return
        else:
            if self.cash_role.get() == "admin":
                messagebox.showwarning("Warning", "You are adding a user as an admin! ")
            if messagebox.askyesno("Update User", "Do you want to update the user details?"):
                if POSdatabase.update_user_db(self.rows[0], self.cash_username.get(), self.cash_pass.get(),
                                              self.cash_role.get()):
                    self.clear_data()
                    messagebox.showinfo("Update Success", "User information has been updated!")
                    self.rows = []
                    self.display_users_search()
                    return
                else:
                    return

    def delete_user(self):
        select = self.user_table.focus()
        contents = self.user_table.item(select)
        user_select = contents['values']

        if not user_select:
            messagebox.showerror("Delete User Error", "Select a user first.")
            return
        else:
            if messagebox.askyesno("Delete User", "Are you sure you want to remove this user?"):
                if POSdatabase.delete_user_db(user_select[0]):
                    messagebox.showinfo("Delete Success", "User deleted in database!")
                    self.user_features()
                    self.display_users_search()
                    return
                else:
                    return
            else:
                return

    def change_pass_admin_frame(self):
        change_pass_admin_frame = Frame(self.user_frame, bg="white", highlightcolor="black", highlightthickness=2)
        change_pass_admin_frame.place(x=10, y=320, height=300, width=500)

        change_pass_label = Label(change_pass_admin_frame, text="ADMIN CHANGE PASSWORD",
                                  font=("Blinker", 15, "underline", "bold"), bg="white")
        change_pass_label.place(x=10, y=10, height=40)

        admin_user_label = Label(change_pass_admin_frame, text="Username: ", bg="black", fg="white",
                                 font=("Bebas Neue", 15))
        admin_user_label.place(x=20, y=80, height=30, width=100)
        adminuser_entry = Entry(change_pass_admin_frame, font=("Blinker", 15), highlightbackground="black",
                                highlightthickness=2)
        adminuser_entry.insert(0, "admin")
        adminuser_entry.config(state=DISABLED)
        adminuser_entry.place(x=120, y=80, width=350, height=30)

        old_pass_label = Label(change_pass_admin_frame, text="Old Password:", bg="black", fg="white",
                               font=("Bebas Neue", 13))
        old_pass_label.place(x=20, y=120, height=30, width=100)
        old_pass_entry = Entry(change_pass_admin_frame, font=("Blinker", 15), highlightbackground="black",
                               highlightthickness=2, show="*", textvariable=self.admin_old_pass)
        old_pass_entry.place(x=120, y=120, width=350, heigh=30)

        new_pass_label = Label(change_pass_admin_frame, text="New Password:", bg="black", fg="white",
                               font=("Bebas Neue", 13))
        new_pass_label.place(x=20, y=160, height=30, width=100)
        new_pass_entry = Entry(change_pass_admin_frame, font=("Blinker", 15), highlightbackground="black",
                               highlightthickness=2, show="*", textvariable=self.admin_new_pass)
        new_pass_entry.place(x=120, y=160, width=350, height=30)

        re_ent_pass_label = Label(change_pass_admin_frame, text="Re-Enter Password:", bg="black", fg="white",
                                  font=("Bebas Neue", 13))
        re_ent_pass_label.place(x=20, y=200, width=120, height=30)
        re_ent_pass_entry = Entry(change_pass_admin_frame, font=("Blinker", 15), highlightbackground="black",
                                  highlightthickness=2, show="*", textvariable=self.admin_re_ent_pass)
        re_ent_pass_entry.place(x=140, y=200, width=330, height=30)

        change_pass_button = Button(change_pass_admin_frame, command=self.change_pass_admin, text="CHANGE PASSWORD",
                                    bg="black", fg="white",
                                    activebackground="black", activeforeground="white", font=("Bebas Neue", 15))
        change_pass_button.place(x=320, y=245, width=150, height=30)

    def change_pass_admin(self):
        if self.admin_old_pass.get() == "" or self.admin_new_pass.get() == "" or self.admin_re_ent_pass.get() == "":
            messagebox.showerror("Admin Change Password Error", "Please fill out all fields")
        else:
            db = sqlite3.connect("pos.db")
            cursor = db.cursor()
            cursor.execute("SELECT * FROM USERS where c_username='admin'")
            user = cursor.fetchone()
            if user[1] != self.admin_old_pass.get():
                messagebox.showerror("Admin Change Password Error", "Wrong Password")
                return
            elif self.admin_new_pass.get() != self.admin_re_ent_pass.get():
                messagebox.showerror("Admin Change Password Error", "Password do not match")
                return
            else:
                if messagebox.askyesno("Change Password", "Are you sure you want to modify your password?"):
                    cursor.execute("UPDATE USERS SET c_pass=? WHERE c_username=?", (self.admin_new_pass.get(),
                                                                                    'admin'))
                    messagebox.showinfo("Success", "Password has been updated!")
                    self.clear_data()
                    db.commit()
                    db.close()
                    return
                else:
                    return

    def display_users_search(self):
        result = POSdatabase.search_user_db(self.search_user.get())
        self.user_table.delete(*self.user_table.get_children())
        if not result:
            return
        else:
            for x in result:
                if x[0] != "admin":
                    self.user_table.insert('', 0, values=(x[0], x[1]))

    def clear_data(self):
        self.admin_old_pass.set("")
        self.admin_new_pass.set("")
        self.admin_re_ent_pass.set("")
        self.cash_username.set("")
        self.cash_pass.set("")
        self.cash_re_ent_pass.set("")
        self.cash_role.set("")

    def select_user(self, ev):
        cursor_row = self.user_table.focus()
        contents = self.user_table.item(cursor_row)
        self.rows = contents['values']
        self.clear_data()
        if not self.rows:
            return
        else:
            self.cash_username.set(self.rows[0])
            self.cash_pass.set(self.rows[1])
