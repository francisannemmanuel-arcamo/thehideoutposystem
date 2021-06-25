from tkinter import messagebox
import sqlite3
import string
import random


def db_table_create():
    db = sqlite3.connect("pos.db")
    db.execute("CREATE TABLE IF NOT EXISTS USERS(c_username VARCHAR(20) NOT NULL DEFAULT '', "
               "c_pass VARCHAR(30) NOT NULL DEFAULT '',"
               "c_role VARCHAR(5) NOT NULL DEFAULT '',"
               "PRIMARY KEY (c_username))")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM USERS where c_role='admin'")
    check = cursor.fetchone()
    if not check:
        db.execute("INSERT INTO USERS VALUES(?,?,?)", ("admin", "thehideoutcoffeeshopadmin", "admin"))
    db.execute("CREATE TABLE IF NOT EXISTS PRODUCT(product_id VARCHAR(10) NOT NULL DEFAULT '',"
               "product_price DOUBLE NOT NULL DEFAULT 0,"
               "product_name VARCHAR(50) NOT NULL DEFAULT '', "
               "product_categ VARCHAR(50) NOT NULL DEFAULT '',"
               "PRIMARY KEY (product_id))")
    db.execute("CREATE TABLE IF NOT EXISTS TRANSACTIONS(transact_id VARCHAR(10) NOT NULL,"
               "order_date DATE NOT NULL, "
               "c_username VARCHAR(10) NOT NULL DEFAULT '',"
               "PRIMARY KEY (transact_id),"
               "FOREIGN KEY (c_username) REFERENCES USERS(c_username)"
               "    ON DELETE NO ACTION"
               "    ON UPDATE CASCADE)")
    db.execute("CREATE TABLE IF NOT EXISTS TRANSACTED_PRODUCTS(transact_id VARCHAR(10) NOT NULL,"
               "product_id VARCHAR(10) NOT NULL,"
               "prod_price NOT NULL DEFAULT 0,"
               "item_quantity INTEGER NOT NULL DEFAULT 1,"
               "discount DOUBLE NOT NULL DEFAULT 0,"
               "item_subtotal AS (prod_price*item_quantity - discount),"
               "PRIMARY KEY (transact_id, product_id),"
               "FOREIGN KEY (product_id) REFERENCES PRODUCT(product_id)"
               "    ON DELETE NO ACTION"
               "    ON UPDATE CASCADE,"
               "FOREIGN KEY (transact_id)"
               "REFERENCES TRANSACTIONS(transact_id)"
               "    ON DELETE CASCADE)")
    db.execute("CREATE TABLE IF NOT EXISTS PAYMENT(pay_id VARCHAR(10) NOT NULL, "
               "transact_id VARCHAR(10) NOT NULL,"
               "payment_date DATE NOT NULL,"
               "total_cost DOUBLE NOT NULL DEFAULT 0,"
               "amount DOUBLE NOT NULL DEFAULT 0,"
               "change AS (amount - total_cost),"
               "vat AS (round(total_cost*0.12, 2)),"
               "vatable_sale AS (round(total_cost-vat, 2)),"
               "PRIMARY KEY(pay_id),"
               "FOREIGN KEY (transact_id)"
               "REFERENCES TRANSACTIONS(transact_id)"
               "    ON DELETE CASCADE)")
    db.commit()
    db.close()


def log_in(username, password):
    db = sqlite3.connect("pos.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM USERS where c_username=? AND c_pass=?",
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
        cur.execute("INSERT INTO PRODUCT VALUES(?, ?, ?, ?)", (prod_id, price, name, categ))
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
    cur.execute("SELECT * FROM PRODUCT WHERE product_name LIKE ?", ('%' + prod_name + '%',))
    result = cur.fetchall()
    db.commit()
    db.close()
    return result


def search_prod_db_by_id(prod_id):
    db = sqlite3.connect("pos.db")
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    cur.execute("SELECT * FROM PRODUCT WHERE product_id=?", (prod_id,))
    result = cur.fetchone()
    db.commit()
    db.close()
    return result


def search_prod_db_by_namecateg(prod_name, prod_categ):
    db = sqlite3.connect("pos.db")
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    cur.execute("SELECT * FROM PRODUCT WHERE product_categ LIKE ? AND product_name LIKE ?",
                ('%' + prod_categ + '%', '%' + prod_name + '%',))
    result = cur.fetchall()
    db.commit()
    db.close()
    return result


def delete_prod_db(prod_id):
    db = sqlite3.connect("pos.db")
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    try:
        cur.execute("DELETE FROM PRODUCT WHERE product_id=?", (prod_id,))
        db.commit()
        db.close()
        return True
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "You cannot delete this product")
        return False


def update_product_db(key, prod_id, prod_name, prod_categ, prod_price):
    db = sqlite3.connect("pos.db")
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    try:
        if key != prod_id:
            cur.execute("UPDATE PRODUCT SET product_id=?, product_name=?, product_categ=?, product_price=?"
                        "WHERE product_id=?", (prod_id, prod_name, prod_categ, prod_price, key))
        else:
            cur.execute("UPDATE PRODUCT SET product_name=?, product_categ=?, product_price=?"
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
    cur.execute("SELECT * FROM USERS WHERE c_username LIKE ?", ('%' + username + '%',))
    result = cur.fetchall()
    db.commit()
    db.close()
    return result


def add_user_db(uname, cpass, role):
    db = sqlite3.connect("pos.db")
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    try:
        cur.execute("INSERT INTO USERS VALUES(?,?, ?)", (uname, cpass, role))
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
    try:
        cur.execute("DELETE FROM USERS WHERE c_username=?", (uname,))
        db.commit()
        db.close()
        return True
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "You cannot delete this user")
        return False


def update_user_db(key, uname, cpass, role):
    db = sqlite3.connect("pos.db")
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    try:
        if key != uname:
            cur.execute("UPDATE USERS SET c_username=?, c_pass=?, c_role=?, WHERE c_username=?",
                        (uname, cpass, role, key))
        else:
            cur.execute("UPDATE USERS SET c_pass=?, c_role=?, WHERE c_username=?", (cpass, uname, role))
        db.commit()
        db.close()
        return True
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already in database")
        return False


def add_new_transact(date, user):
    db = sqlite3.connect("pos.db")
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    transactid = ""
    while True:
        try:
            transactid = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            cur.execute("INSERT INTO TRANSACTIONS VALUES(?, ?, ?)", (transactid, date, user))
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
        cur.execute("INSERT INTO TRANSACTED_PRODUCTS VALUES(?, ?, ?, ?, ?)",
                    (trans_id, prod_id, prod_price, quantity, discount))
    except sqlite3.IntegrityError:
        cur.execute("SELECT item_quantity FROM TRANSACTED_PRODUCTS WHERE (transact_id=? AND product_id=?)", (trans_id, prod_id))
        new_quant = cur.fetchone()[0] + 1
        cur.execute("UPDATE TRANSACTED_PRODUCTS SET item_quantity=? WHERE (transact_id=? AND product_id=?)",
                    (new_quant, trans_id, prod_id))
    db.commit()
    db.close()


def trans_product_show(trans_id):
    db = sqlite3.connect("pos.db")
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    cur.execute("SELECT * FROM TRANSACTED_PRODUCTS WHERE transact_id=?", (trans_id,))
    trans_prods = cur.fetchall()
    db.commit()
    db.close()
    return trans_prods


def clear_cart(trans_id):
    db = sqlite3.connect("pos.db")
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    cur.execute("DELETE FROM TRANSACTED_PRODUCTS WHERE transact_id=?", (trans_id,))
    db.commit()
    db.close()


def remove_prod_from_trans(trans_id, prod_id):
    db = sqlite3.connect("pos.db")
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    cur.execute("DELETE FROM TRANSACTED_PRODUCTS WHERE (transact_id=? AND product_id=?)", (trans_id, prod_id))
    db.commit()
    db.close()


def edit_quantity(trans_id, prod_id, quantity):
    db = sqlite3.connect("pos.db")
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    cur.execute("UPDATE TRANSACTED_PRODUCTS SET item_quantity=? WHERE (transact_id=? AND product_id=?)",
                (quantity, trans_id, prod_id))
    db.commit()
    db.close()


def total_cost(trans_id):
    db = sqlite3.connect("pos.db")
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    cur.execute("SELECT item_subtotal FROM TRANSACTED_PRODUCTS WHERE transact_id=?", (trans_id,))
    stot = cur.fetchall()
    db.commit()
    db.close()
    return stot


def add_discount(trans_id, prod_id, discount):
    db = sqlite3.connect("pos.db")
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    cur.execute("UPDATE TRANSACTED_PRODUCTS SET discount=? WHERE (transact_id=? AND product_id=?)",
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
    cur.execute("SELECT * FROM TRANSACTED_PRODUCTS WHERE transact_id LIKE ? AND product_id LIKE ?",
                ('%' + trans_id + '%', '%' + prod_id + '%'))
    trans_prods = cur.fetchall()
    db.commit()
    db.close()
    return trans_prods


def total_quantity_prod(prod_id):
    db = sqlite3.connect("pos.db")
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    cur.execute("SELECT item_quantity FROM TRANSACTED_PRODUCTS WHERE product_id=?", (prod_id,))
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
    cur.execute("SELECT item_subtotal FROM TRANSACTED_PRODUCTS WHERE product_id=?", (prod_id,))
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
