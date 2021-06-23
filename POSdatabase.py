from tkinter import messagebox
import sqlite3
import string
import random


def db_table_create():
    db = sqlite3.connect("pos.db")
    db.execute("CREATE TABLE IF NOT EXISTS CASHIER(c_username VARCHAR(10) PRIMARY KEY, c_pass VARCHAR(100))")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM CASHIER where c_username='admin'")
    check = cursor.fetchone()
    if not check:
        db.execute("INSERT INTO CASHIER VALUES(?,?)", ("admin", "thehideoutcoffeeshopadmin"))
    db.execute("CREATE TABLE IF NOT EXISTS PRODUCTS(product_id VARCHAR(10) NOT NULL PRIMARY KEY,"
               "product_name VARCHAR(10) NOT NULL, product_categ VARCHAR(10) NOT NULL, product_price DOUBLE NOT NULL)")
    db.execute("CREATE TABLE IF NOT EXISTS TRANSACTIONS(transact_id VARCHAR(10) NOT NULL PRIMARY KEY,"
               "order_date DATE NOT NULL, c_username VARCHAR(10) NOT NULL,"
               "FOREIGN KEY (c_username)"
               "REFERENCES CASHIER(c_username)"
               "    ON DELETE SET NULL"
               "    ON UPDATE CASCADE)")
    db.execute("CREATE TABLE IF NOT EXISTS PAYMENT(pay_id VARCHAR(10) NOT NULL PRIMARY KEY, "
               "transact_id VARCHAR(10) NOT NULL,"
               "payment_date DATE NOT NULL,"
               "total_cost DOUBLE NOT NULL,"
               "amount DOUBLE NOT NULL,"
               "change AS (amount - total_cost),"
               "vat AS (round(total_cost*0.12, 2)),"
               "vatable_sale AS (round(total_cost-vat, 2)), "
               "FOREIGN KEY (transact_id)"
               "REFERENCES TRANSACTIONS(transact_id))")
    db.execute("CREATE TABLE IF NOT EXISTS contains(transact_id VARCHAR(10) NOT NULL,"
               "product_id VARCHAR(10) NOT NULL,"
               "prod_price NOT NULL,"
               "item_quantity INTEGER NOT NULL,"
               "discount DOUBLE NOT NULL,"
               "item_subtotal AS (prod_price*item_quantity - discount),"
               "PRIMARY KEY (transact_id, product_id)"
               "FOREIGN KEY (product_id) "
               "REFERENCES PRODUCTS(product_id)"
               "    ON DELETE SET NULL"
               "    ON UPDATE CASCADE,"
               "FOREIGN KEY (transact_id)"
               "REFERENCES TRANSACTIONS(transact_id)"
               "    ON DELETE CASCADE)")
    db.commit()
    db.close()


def log_in(username, password):
    db = sqlite3.connect("pos.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM CASHIER where c_username=? AND c_pass=?",
                   (username, password))
    row = cursor.fetchone()
    db.commit()
    db.close()
    return row


def add_prod_db(prod_id, name, categ, price):
    db = sqlite3.connect("pos.db")
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    try:
        cur.execute("INSERT INTO PRODUCTS VALUES(?, ?, ?, ?)", (prod_id, name, categ, price))
        db.commit()
        db.close()
        return True
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Product ID already in database")
        return False


def search_prod_db_by_name(prod_name):
    db = sqlite3.connect("pos.db")
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    cur.execute("SELECT * FROM PRODUCTS WHERE product_name LIKE ?", ('%' + prod_name + '%',))
    result = cur.fetchall()
    db.commit()
    db.close()
    return result


def search_prod_db_by_id(prod_id):
    db = sqlite3.connect("pos.db")
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    cur.execute("SELECT * FROM PRODUCTS WHERE product_id=?", (prod_id,))
    result = cur.fetchone()
    db.commit()
    db.close()
    return result


def search_prod_db_by_namecateg(prod_name, prod_categ):
    db = sqlite3.connect("pos.db")
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    cur.execute("SELECT * FROM PRODUCTS WHERE product_categ LIKE ? AND product_name LIKE ?",
                ('%' + prod_categ + '%', '%' + prod_name + '%',))
    result = cur.fetchall()
    db.commit()
    db.close()
    return result


def delete_prod_db(prod_id):
    db = sqlite3.connect("pos.db")
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    cur.execute("DELETE FROM PRODUCTS WHERE product_id=?", (prod_id,))
    db.commit()
    db.close()


def update_product_db(key, prod_id, prod_name, prod_categ, prod_price):
    db = sqlite3.connect("pos.db")
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    try:
        if key != prod_id:
            cur.execute("UPDATE PRODUCTS SET product_id=?, product_name=?, product_categ=?, product_price=?"
                        "WHERE product_id=?", (prod_id, prod_name, prod_categ, prod_price, key))
        else:
            cur.execute("UPDATE PRODUCTS SET product_name=?, product_categ=?, product_price=?"
                        "WHERE product_id=?", (prod_name, prod_categ, prod_price, prod_id))
        db.commit()
        db.close()
        return True
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Product ID already in database!")
        return False


def search_user_db(username):
    db = sqlite3.connect("pos.db")
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    cur.execute("SELECT * FROM CASHIER WHERE c_username LIKE ?", ('%' + username + '%',))
    result = cur.fetchall()
    db.commit()
    db.close()
    return result


def add_user_db(uname, cpass):
    db = sqlite3.connect("pos.db")
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    try:
        cur.execute("INSERT INTO CASHIER VALUES(?,?)", (uname, cpass))
        db.commit()
        db.close()
        return True
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already in database")
        return False


def delete_user_db(uname):
    db = sqlite3.connect("pos.db")
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    cur.execute("DELETE FROM CASHIER WHERE c_username=?", (uname,))
    db.commit()
    db.close()


def update_user_db(key, uname, cpass):
    db = sqlite3.connect("pos.db")
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    try:
        if key != uname:
            cur.execute("UPDATE CASHIER SET c_username=?, c_pass=? WHERE c_username=?", (uname, cpass, key))
        else:
            cur.execute("UPDATE CASHIER SET c_pass=? WHERE c_username=?", (cpass, uname))
        db.commit()
        db.close()
        return True
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already in database")
        return False


def add_new_transact(date, cashier):
    db = sqlite3.connect("pos.db")
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    transactid = ""
    while True:
        try:
            transactid = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            cur.execute("INSERT INTO TRANSACTIONS VALUES(?, ?, ?)", (transactid, date, cashier))
            break
        except sqlite3.IntegrityError:
            continue
    db.commit()
    db.close()
    return transactid


def delete_transact(trans_id):
    db = sqlite3.connect("pos.db")
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    cur.execute("DELETE FROM TRANSACTIONS WHERE transact_id=?", (trans_id,))
    db.commit()
    db.close()


def add_prod_to_trans(trans_id, prod_id, prod_price, quantity, discount):
    db = sqlite3.connect("pos.db")
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    try:
        cur.execute("INSERT INTO contains VALUES(?, ?, ?, ?, ?)",
                    (trans_id, prod_id, prod_price, quantity, discount))
    except sqlite3.IntegrityError:
        cur.execute("SELECT item_quantity FROM contains WHERE (transact_id=? AND product_id=?)", (trans_id, prod_id))
        new_quant = cur.fetchone()[0] + 1
        cur.execute("UPDATE contains SET item_quantity=? WHERE (transact_id=? AND product_id=?)",
                    (new_quant, trans_id, prod_id))
    db.commit()
    db.close()


def trans_product_show(trans_id):
    db = sqlite3.connect("pos.db")
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    cur.execute("SELECT * FROM contains WHERE transact_id=?", (trans_id,))
    trans_prods = cur.fetchall()
    db.commit()
    db.close()
    return trans_prods


def clear_cart(trans_id):
    db = sqlite3.connect("pos.db")
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    cur.execute("DELETE FROM contains WHERE transact_id=?", (trans_id,))
    db.commit()
    db.close()


def remove_prod_from_trans(trans_id, prod_id):
    db = sqlite3.connect("pos.db")
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    cur.execute("DELETE FROM contains WHERE (transact_id=? AND product_id=?)", (trans_id, prod_id))
    db.commit()
    db.close()


def edit_quantity(trans_id, prod_id, quantity):
    db = sqlite3.connect("pos.db")
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    cur.execute("UPDATE contains SET item_quantity=? WHERE (transact_id=? AND product_id=?)",
                (quantity, trans_id, prod_id))
    db.commit()
    db.close()


def total_cost(trans_id):
    db = sqlite3.connect("pos.db")
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    cur.execute("SELECT item_subtotal FROM contains WHERE transact_id=?", (trans_id,))
    stot = cur.fetchall()
    db.commit()
    db.close()
    return stot


def add_discount(trans_id, prod_id, discount):
    db = sqlite3.connect("pos.db")
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    cur.execute("UPDATE contains SET discount=? WHERE (transact_id=? AND product_id=?)",
                (discount, trans_id, prod_id))
    db.commit()
    db.close()


def add_payment(trans_id, paydate, amount, totalcost):
    db = sqlite3.connect("pos.db")
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    while True:
        try:
            payid = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            cur.execute("INSERT INTO PAYMENT VALUES (?, ?, ?, ?, ?)", (payid, trans_id, paydate, totalcost, amount))
            break
        except sqlite3.IntegrityError:
            continue
    db.commit()
    db.close()


def trans_details(trans_id):
    db = sqlite3.connect("pos.db")
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    cur.execute("SELECT * FROM TRANSACTIONS WHERE transact_id=?", (trans_id,))
    det = cur.fetchone()
    db.commit()
    db.close()
    return det


def trans_show(trans_id, prod_id):
    db = sqlite3.connect("pos.db")
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    cur.execute("SELECT * FROM contains WHERE transact_id LIKE ? AND product_id LIKE ?",
                ('%' + trans_id + '%', '%' + prod_id + '%'))
    trans_prods = cur.fetchall()
    db.commit()
    db.close()
    return trans_prods


def total_quantity_prod(prod_id):
    db = sqlite3.connect("pos.db")
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    cur.execute("SELECT item_quantity FROM contains WHERE product_id=?", (prod_id,))
    prods = cur.fetchall()
    db.commit()
    db.close()
    tot_qty = 0
    if not prods:
        return 0
    else:
        for x in prods:
            tot_qty += x[0]
        return tot_qty


def tot_sales_prod(prod_id):
    db = sqlite3.connect("pos.db")
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    cur.execute("SELECT item_subtotal FROM contains WHERE product_id=?", (prod_id,))
    prods = cur.fetchall()
    db.commit()
    db.close()
    tot_sales = 0
    if not prods:
        return 0
    else:
        for x in prods:
            tot_sales += x[0]
        return tot_sales


def trans_srch_by_cashier(cash_username):
    db = sqlite3.connect("pos.db")
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    cur.execute("SELECT * FROM TRANSACTIONS WHERE c_username LIKE ?", ('%' + cash_username + '%',))
    trans = cur.fetchall()
    db.commit()
    db.close()
    return trans


def payment_history(trans_id):
    db = sqlite3.connect("pos.db")
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    if trans_id == "":
        cur.execute("SELECT * FROM PAYMENT")
    else:
        cur.execute("SELECT * FROM PAYMENT WHERE transact_id=?", (trans_id,))
    pay_hist = cur.fetchall()
    db.commit()
    db.close()
    return pay_hist
