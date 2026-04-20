import tkinter as tk
from tkinter import ttk
from bibliotheque import Bibliotheque

BG        = "#F4F6FB"
SURFACE   = "#FFFFFF"
BORDER    = "#C8D3E8"
HEADER_BG = "#1A3A6B"
ACCENT    = "#1A3A6B"
ACCENT_H  = "#254EA0"
RED       = "#CC2222"
RED_H     = "#E53535"
SUCCESS   = "#1A7A3C"
WARNING   = "#B85C00"
DANGER    = "#CC2222"
TEXT      = "#0D1B2E"
MUTED     = "#6B7A99"
TEXT_INV  = "#FFFFFF"

FONT_H1   = ("Segoe UI", 17, "bold")
FONT_H2   = ("Segoe UI", 12, "bold")
FONT_BODY = ("Segoe UI", 10)
FONT_SM   = ("Segoe UI", 9)
PAD = 14

app = Bibliotheque()
app.ajouter_livre("Python Fluent",          "Luciano Ramalho",   "Informatique",     4)
app.ajouter_livre("Algorithmes en Python",  "Brad Miller",       "Informatique",     3)
app.ajouter_livre("Clean Code",             "Robert C. Martin",  "Génie logiciel",   5)
app.ajouter_livre("Design Patterns",        "Gang of Four",      "Architecture",     2)
app.ajouter_livre("Deep Learning",          "Ian Goodfellow",    "IA / ML",          3)
app.ajouter_livre("SQL Performance",        "Markus Winand",     "Bases de données", 4)

def card(parent, **kwargs):
    return tk.Frame(parent, bg=SURFACE, bd=0,
                    highlightbackground=BORDER, highlightthickness=1, **kwargs)

def label(parent, text, font=FONT_BODY, fg=TEXT, bg=SURFACE, **kw):
    return tk.Label(parent, text=text, font=font, fg=fg, bg=bg, **kw)

def section_title(parent, text):
    f = tk.Frame(parent, bg=SURFACE)
    f.pack(fill="x", padx=PAD, pady=(PAD, 6))
    tk.Frame(f, bg=RED, width=4, height=18).pack(side="left", padx=(0, 8))
    tk.Label(f, text=text, font=FONT_H2, fg=ACCENT, bg=SURFACE).pack(side="left")

def styled_entry(parent, placeholder=""):
    var = tk.StringVar()
    e = tk.Entry(parent, textvariable=var, font=FONT_BODY,
                 bg="#EEF2FA", fg=TEXT, insertbackground=ACCENT,
                 relief="flat", bd=0,
                 highlightbackground=BORDER, highlightthickness=1)

    def on_focus_in(evt):
        e.config(highlightbackground=ACCENT, highlightthickness=2)
        if var.get() == placeholder:
            var.set("")
            e.config(fg=TEXT)

    def on_focus_out(evt):
        e.config(highlightbackground=BORDER, highlightthickness=1)
        if var.get() == "":
            var.set(placeholder)
            e.config(fg=MUTED)

    if placeholder:
        var.set(placeholder)
        e.config(fg=MUTED)

    e.bind("<FocusIn>",  on_focus_in)
    e.bind("<FocusOut>", on_focus_out)
    e._placeholder = placeholder
    e._var = var
    return e

def get_val(entry):
    val = entry._var.get()
    return "" if val == entry._placeholder else val.strip()

def make_btn(parent, text, command, bg_color, hover_color):
    b = tk.Button(parent, text=text, font=("Segoe UI", 10, "bold"),
                  bg=bg_color, fg=TEXT_INV,
                  activebackground=hover_color, activeforeground=TEXT_INV,
                  relief="flat", bd=0, padx=PAD, pady=9,
                  cursor="hand2", command=command)
    b.bind("<Enter>", lambda e: b.config(bg=hover_color))
    b.bind("<Leave>", lambda e: b.config(bg=bg_color))
    return b

def notify(msg, kind="ok"):
    color = SUCCESS if kind == "ok" else (WARNING if kind == "warn" else DANGER)
    icon  = "✓" if kind == "ok" else ("⚠" if kind == "warn" else "✗")
    _notif_bar.config(text=f"  {icon}  {msg}", fg=color)
    root.after(4500, lambda: _notif_bar.config(text=""))


def do_inscrire():
    ok, msg = app.inscrire(get_val(e_nom), get_val(e_prenom), get_val(e_email))
    notify(msg, "ok" if ok else "err")
    if ok:
        update_stats()

def do_login():
    ok, msg = app.login(get_val(e_email_login))
    notify(msg, "ok" if ok else "err")
    if ok:
        lbl_user.config(
            text=f"  ● {app.user_connecte['prenom']} {app.user_connecte['nom']}",
            fg="#7FFFC4")
        update_emprunts()

def do_logout():
    app.logout()
    lbl_user.config(text="  ○ Non connecté", fg="#A0B8D8")
    update_emprunts()
    notify("Déconnecté.", "warn")

def do_emprunter():
    sel = tree_livres.selection()
    if not sel:
        notify("Sélectionnez un livre dans le catalogue.", "warn")
        return
    livre_id = int(tree_livres.item(sel[0])["values"][0])
    status, msg = app.emprunter(livre_id)
    notify(msg, "ok" if status == "ok" else ("warn" if status == "no_user" else "err"))
    if status == "ok":
        refresh_livres()
        update_emprunts()
        update_stats()

def do_retourner():
    sel = tree_emprunts.selection()
    if not sel:
        notify("Sélectionnez un emprunt à retourner.", "warn")
        return
    livre_id = int(tree_emprunts.item(sel[0])["values"][0])
    ok, msg = app.retourner(livre_id)
    notify(msg, "ok" if ok else "err")
    if ok:
        refresh_livres()
        update_emprunts()
        update_stats()

def refresh_livres():
    for row in tree_livres.get_children():
        tree_livres.delete(row)
    for l in app.livres:
        dispo = l["quantite"]
        tag = "dispo" if dispo > 0 else "indispo"
        tree_livres.insert("", "end",
            values=(l["id"], l["titre"], l["auteur"], l["genre"],
                    f"{dispo}/{l['quantite_initiale']}"),
            tags=(tag,))

def update_emprunts():
    for row in tree_emprunts.get_children():
        tree_emprunts.delete(row)
    if app.user_connecte:
        for em in app.user_connecte["emprunts"]:
            tree_emprunts.insert("", "end",
                values=(em["id"], em["titre"], em["auteur"],
                        em.get("date_emprunt", "—")))

def update_stats():
    s = app.stats()
    lbl_s1.config(text=str(s["total_titres"]))
    lbl_s2.config(text=str(s["total_exemplaires"]))
    lbl_s3.config(text=str(s["empruntes"]))
    lbl_s4.config(text=str(s["membres"]))


root = tk.Tk()
root.title("Bibliothèque Numérique")
root.geometry("1080x720")
root.minsize(920, 640)
root.configure(bg=BG)
root.resizable(True, True)


header = tk.Frame(root, bg=HEADER_BG, padx=PAD*2, pady=14)
header.pack(fill="x")

# Logo JR circulaire
logo_c = tk.Canvas(header, width=46, height=46, bg=HEADER_BG, highlightthickness=0)
logo_c.pack(side="left", padx=(0, 10))
logo_c.create_oval(2, 2, 44, 44, fill=RED, outline="")
logo_c.create_text(23, 23, text="JR", font=("Segoe UI", 14, "bold"), fill=TEXT_INV)
tk.Label(header, text="Bibliothèque Numérique",
         font=FONT_H1, fg=TEXT_INV, bg=HEADER_BG).pack(side="left")
tk.Frame(header, bg=RED, width=5, height=30).pack(side="left", padx=16)

lbl_user = tk.Label(header, text="○ Non connecté",
                    font=FONT_BODY, fg="#A0B8D8", bg=HEADER_BG)
lbl_user.pack(side="right", padx=(0, 8))

b_deco = tk.Button(header, text="Déconnexion", font=FONT_SM,
                   bg=RED, fg=TEXT_INV, activebackground=RED_H,
                   activeforeground=TEXT_INV, relief="flat", bd=0,
                   padx=10, pady=5, cursor="hand2", command=do_logout)
b_deco.pack(side="right", padx=4)
b_deco.bind("<Enter>", lambda e: b_deco.config(bg=RED_H))
b_deco.bind("<Leave>", lambda e: b_deco.config(bg=RED))


notif_frame = tk.Frame(root, bg=BG, pady=3)
notif_frame.pack(fill="x", padx=PAD)
_notif_bar = tk.Label(notif_frame, text="", font=FONT_BODY,
                      bg=BG, fg=SUCCESS, anchor="w")
_notif_bar.pack(fill="x")


body = tk.Frame(root, bg=BG)
body.pack(fill="both", expand=True, padx=PAD, pady=(0, PAD))
body.columnconfigure(0, weight=0, minsize=285)
body.columnconfigure(1, weight=1)
body.rowconfigure(0, weight=1)


left_outer = tk.Frame(body, bg=BG)
left_outer.grid(row=0, column=0, sticky="nsew", padx=(0, PAD))
left_outer.rowconfigure(0, weight=1)
left_outer.columnconfigure(0, weight=1)

left_canvas = tk.Canvas(left_outer, bg=BG, highlightthickness=0)
left_canvas.grid(row=0, column=0, sticky="nsew")

left_scroll = ttk.Scrollbar(left_outer, orient="vertical", command=left_canvas.yview)
left_scroll.grid(row=0, column=1, sticky="ns")
left_canvas.configure(yscrollcommand=left_scroll.set)

left = tk.Frame(left_canvas, bg=BG)
left_win = left_canvas.create_window((0, 0), window=left, anchor="nw")

def _on_left_configure(evt):
    left_canvas.configure(scrollregion=left_canvas.bbox("all"))
    left_canvas.itemconfig(left_win, width=left_canvas.winfo_width())

left.bind("<Configure>", _on_left_configure)
left_canvas.bind("<Configure>", lambda e: left_canvas.itemconfig(left_win, width=e.width))

def _on_mousewheel(evt):
    left_canvas.yview_scroll(int(-1*(evt.delta/120)), "units")
left_canvas.bind_all("<MouseWheel>", _on_mousewheel)

# -- Statistiques --
stats_card = card(left)
stats_card.pack(fill="x", pady=(0, 10))
section_title(stats_card, "Statistiques")

grid_stats = tk.Frame(stats_card, bg=SURFACE)
grid_stats.pack(fill="x", padx=PAD, pady=(0, PAD))
grid_stats.columnconfigure((0, 1), weight=1)

def stat_cell(parent, row, col, big, sub, accent_color=ACCENT):
    f = tk.Frame(parent, bg=BG, padx=6, pady=8,
                 highlightbackground=BORDER, highlightthickness=1)
    f.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")
    lbl = tk.Label(f, text=big, font=("Segoe UI", 18, "bold"),
                   fg=accent_color, bg=BG)
    lbl.pack()
    tk.Label(f, text=sub, font=FONT_SM, fg=MUTED, bg=BG).pack()
    return lbl

lbl_s1 = stat_cell(grid_stats, 0, 0, "0", "Titres",       ACCENT)
lbl_s2 = stat_cell(grid_stats, 0, 1, "0", "Exemplaires",  ACCENT)
lbl_s3 = stat_cell(grid_stats, 1, 0, "0", "Empruntés",    RED)
lbl_s4 = stat_cell(grid_stats, 1, 1, "0", "Membres",      ACCENT)

# -- Inscription --
insc_card = card(left)
insc_card.pack(fill="x", pady=(0, 10))
section_title(insc_card, "Nouvelle inscription")

for placeholder, attr in [("Nom", "e_nom"), ("Prénom", "e_prenom"), ("Email", "e_email")]:
    e = styled_entry(insc_card, placeholder)
    e.pack(fill="x", padx=PAD, pady=3, ipady=7)
    globals()[attr] = e

make_btn(insc_card, "Créer mon compte  →", do_inscrire, ACCENT, ACCENT_H
         ).pack(fill="x", padx=PAD, pady=(10, PAD))

# -- Connexion --
login_card = card(left)
login_card.pack(fill="x", pady=(0, 10))
section_title(login_card, "Connexion")

e_email_login = styled_entry(login_card, "Adresse email")
e_email_login.pack(fill="x", padx=PAD, pady=3, ipady=7)

# Bouton connexion — fond rouge vif pour être toujours visible
b_login = tk.Button(login_card,
          text="Se connecter  →",
          font=("Segoe UI", 11, "bold"),
          bg=RED, fg=TEXT_INV,
          activebackground=RED_H, activeforeground=TEXT_INV,
          relief="flat", bd=0, padx=PAD, pady=10,
          cursor="hand2",
          command=do_login)
b_login.pack(fill="x", padx=PAD, pady=(10, PAD))
b_login.bind("<Enter>", lambda e: b_login.config(bg=RED_H))
b_login.bind("<Leave>", lambda e: b_login.config(bg=RED))


right = tk.Frame(body, bg=BG)
right.grid(row=0, column=1, sticky="nsew")
right.rowconfigure(1, weight=3)
right.rowconfigure(4, weight=2)
right.columnconfigure(0, weight=1)


style = ttk.Style()
style.theme_use("clam")
style.configure("Lib.Treeview",
                background=SURFACE, fieldbackground=SURFACE,
                foreground=TEXT, rowheight=26,
                borderwidth=0, font=FONT_BODY)
style.configure("Lib.Treeview.Heading",
                background="#DDE4F0", foreground=ACCENT,
                font=("Segoe UI", 9, "bold"), relief="flat", borderwidth=0)
style.map("Lib.Treeview",
          background=[("selected", ACCENT)],
          foreground=[("selected", TEXT_INV)])

# -- Catalogue --
row_cat = tk.Frame(right, bg=BG)
row_cat.grid(row=0, column=0, sticky="ew", pady=(0, 4))
tk.Label(row_cat, text="Catalogue des livres", font=FONT_H2,
         fg=ACCENT, bg=BG).pack(side="left")

b_ref = tk.Button(row_cat, text="↻ Rafraîchir", font=FONT_SM,
                  bg=SURFACE, fg=MUTED, activebackground=BG,
                  relief="flat", bd=0, padx=8, pady=4,
                  highlightbackground=BORDER, highlightthickness=1,
                  cursor="hand2", command=refresh_livres)
b_ref.pack(side="right")

cat_card = card(right)
cat_card.grid(row=1, column=0, sticky="nsew", pady=(0, 6))
cat_card.rowconfigure(0, weight=1)
cat_card.columnconfigure(0, weight=1)

cols_cat = ("ID", "Titre", "Auteur", "Genre", "Dispo")
tree_livres = ttk.Treeview(cat_card, columns=cols_cat, show="headings",
                            style="Lib.Treeview", selectmode="browse")
tree_livres.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)

for col, w in zip(cols_cat, (40, 210, 155, 130, 65)):
    tree_livres.heading(col, text=col)
    anchor = "center" if col in ("ID", "Dispo") else "w"
    tree_livres.column(col, width=w, stretch=(col == "Titre"), anchor=anchor)

tree_livres.tag_configure("dispo",   foreground=TEXT)
tree_livres.tag_configure("indispo", foreground="#B0B8CC")

vsb1 = ttk.Scrollbar(cat_card, orient="vertical", command=tree_livres.yview)
vsb1.grid(row=0, column=1, sticky="ns", pady=1)
tree_livres.configure(yscrollcommand=vsb1.set)

make_btn(right, "⤓   Emprunter le livre sélectionné", do_emprunter, ACCENT, ACCENT_H
         ).grid(row=2, column=0, sticky="ew", pady=(0, PAD))

# -- Mes Emprunts --
row_emp = tk.Frame(right, bg=BG)
row_emp.grid(row=3, column=0, sticky="ew", pady=(0, 4))
tk.Label(row_emp, text="Mes emprunts en cours", font=FONT_H2,
         fg=ACCENT, bg=BG).pack(side="left")

emp_card = card(right)
emp_card.grid(row=4, column=0, sticky="nsew")
emp_card.rowconfigure(0, weight=1)
emp_card.columnconfigure(0, weight=1)

cols_emp = ("ID", "Titre", "Auteur", "Date emprunt")
tree_emprunts = ttk.Treeview(emp_card, columns=cols_emp, show="headings",
                              style="Lib.Treeview", selectmode="browse")
tree_emprunts.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)

for col, w in zip(cols_emp, (40, 230, 165, 110)):
    tree_emprunts.heading(col, text=col)
    anchor = "center" if col == "ID" else "w"
    tree_emprunts.column(col, width=w, stretch=(col == "Titre"), anchor=anchor)

vsb2 = ttk.Scrollbar(emp_card, orient="vertical", command=tree_emprunts.yview)
vsb2.grid(row=0, column=1, sticky="ns", pady=1)
tree_emprunts.configure(yscrollcommand=vsb2.set)

make_btn(right, "↩   Retourner l'emprunt sélectionné", do_retourner, RED, RED_H
         ).grid(row=5, column=0, sticky="ew", pady=(6, 0))


status_bar = tk.Frame(root, bg=HEADER_BG, padx=PAD, pady=6)
status_bar.pack(fill="x", side="bottom")
tk.Label(status_bar, text="Bibliothèque Numérique  v2.1",
         font=FONT_SM, fg="#A0B8D8", bg=HEADER_BG).pack(side="left")
tk.Label(status_bar, text="© 2025 – Tous droits réservés",
         font=FONT_SM, fg="#A0B8D8", bg=HEADER_BG).pack(side="right")


refresh_livres()
update_stats()

root.mainloop()
