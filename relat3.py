import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, Frame, Label, Text, TOP, LEFT, BOTH, X, Y, W, EW, NSEW, RIGHT, END, \
    YES, SUNKEN, BOTTOM, VERTICAL, Toplevel, RAISED, HORIZONTAL

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)


def msg(msg):
    popup = tk.Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
    B1.pack()
    popup.mainloop()


def hello(msg):
    messagebox.showwarning("Say Hello", "Hello World")

def deleteBox(titulo, msg):
    result = messagebox.askquestion(titulo, msg, icon='warning')
    if result == 'yes':
        return True
    else:
        return False

def centro(win):
    """
    centers a tkinter ROOT window
    :param win: the root window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


def centro_(win):
    """
    Centraliza todas as sub janelas, exceto a principal
    :param win: the Toplevel window to center
    """
    win.update()
    win.update_idletasks()
    width = win.winfo_reqwidth()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_reqheight()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


class Relat:

    def __init__(self, parent, db):
        self.parent = parent
        self.db = db

        self.parent.title("Relat")
        self.parent.geometry("700x450")
        self.parent.protocol("WM_DELETE_WINDOW", self.fechar_janela)

        main_frame = Frame(self.parent)
        main_frame.pack(fill=BOTH, expand=YES)

        # TOOLBAR
        toolbar = Frame(main_frame)
        toolbar.pack(side=TOP, fill=X)

        self.projeto_img = tk.PhotoImage(file="./imagens/projetos.png")

        projeto_btn = ttk.Button(toolbar, image=self.projeto_img, command=self.lista_projetos)
        projeto_btn.pack(side=LEFT, padx=2, pady=2)

        self.iniciar_img = tk.PhotoImage(file="./imagens/iniciar.png")

        self.iniciar_btn = ttk.Button(toolbar, image=self.iniciar_img, command=self.iniciar)
        self.iniciar_btn.state(['disabled'])  # set the disabled flag, disabling the button
        self.iniciar_btn.pack(side=LEFT, pady=1)

        self.cancelar_img = tk.PhotoImage(file="./imagens/stop.png")

        self.cancelar_btn = ttk.Button(toolbar, image=self.cancelar_img, command=self.cancelar)
        self.cancelar_btn.state(['disabled'])  # set the disabled flag, disabling the button
        # self.cancelar_btn.state(['!disabled'])

        self.cancelar_btn.pack(side=LEFT, pady=1)

        self.sair_img = tk.PhotoImage(file="./imagens/sair.png")

        self.sair_btn = ttk.Button(toolbar, image=self.sair_img, command=self.fechar_janela)
        self.sair_btn.pack(side=LEFT, pady=1)

        status_bar = Frame(main_frame)
        status_bar.pack(side=BOTTOM, fill=X)

        self.text_status_bar = Label(status_bar, text="www.KlinikPython.Wordpress.Com", relief=SUNKEN, bd=1)
        self.text_status_bar.pack(side=LEFT, fill=X, expand=True)

        self.id_status_bar = Label(status_bar, text="")
        self.id_status_bar.pack(side=RIGHT)

        frame_central = ttk.Notebook(main_frame)

        grid_frame = Frame(frame_central, bd=10)
        grid_frame.pack(fill=BOTH, expand=YES, side=LEFT)

        self.dataCols = ('nome', 'ultima_atualizacao')
        self.relatorios_grid = ttk.Treeview(grid_frame, selectmode='browse', columns=self.dataCols)
        self.relatorios_grid.bind("<Double-1>", self.alterar_relatorio_click)
        #self.relatorios_grid.bind("<Button-1>", self.habilita_btn)

        scroll_y = ttk.Scrollbar(grid_frame, orient=VERTICAL, command=self.relatorios_grid.yview)
        scroll_x = ttk.Scrollbar(grid_frame, orient=HORIZONTAL, command=self.relatorios_grid.xview)
        self.relatorios_grid['yscroll'] = scroll_y.set
        self.relatorios_grid['xscroll'] = scroll_x.set

        scroll_y.configure(command=self.relatorios_grid.yview)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.configure(command=self.relatorios_grid.xview)
        scroll_x.pack(side=BOTTOM, fill=X)

        # setup column headings
        self.relatorios_grid['show'] = 'headings'
        self.relatorios_grid.heading('nome', text='Nome', anchor=W)
        self.relatorios_grid.column('nome', stretch=0, width=200)
        self.relatorios_grid.heading('ultima_atualizacao', text='Última Atualização', anchor=W)
        # self.projetos_grid.column('ultima_atualizacao', stretch=0, width=100)

        self.relatorios_grid.pack(fill=BOTH, side=LEFT, expand=True)

        self.relatorios_grid.bind("<Double-1>", self.alterar_relatorio_click)

        frame_central.add(grid_frame, text="Relatórios")

        frame_central.add(Frame(), text="Configurações")

        frame_central.pack(side=LEFT, fill=BOTH, expand=1)

        frame_botoes = Frame(main_frame, width=200, padx=20, pady=30)
        frame_botoes.pack(side=RIGHT, fill=Y)

        self.novo_relatorio_img = tk.PhotoImage(file="./imagens/incluir.png")

        self.novo_relatorio_btn = ttk.Button(frame_botoes, width=20, text="Incluir", image=self.novo_relatorio_img,
                                             compound=LEFT, command=self.novo_relatorio)
        self.novo_relatorio_btn.pack(side=TOP, pady=2)

        self.alterar_relatorio_img = tk.PhotoImage(file="./imagens/alterar.png")

        self.alterar_relatorio_btn = ttk.Button(frame_botoes, width=20, text="Alterar",
                                                image=self.alterar_relatorio_img,
                                                compound=LEFT, command=self.alterar_relatorio)
        self.alterar_relatorio_btn.pack(side=TOP, pady=2)

        self.excluir_relatorio_img = tk.PhotoImage(file="./imagens/excluir.png")

        self.excluir_relatorio_btn = ttk.Button(frame_botoes, width=20, text="Excluir",
                                                image=self.excluir_relatorio_img, compound=LEFT,
                                                command=self.excluir_relatorio)
        self.excluir_relatorio_btn.pack(side=TOP, pady=2)

        self.move_up_img = tk.PhotoImage(file="./imagens/up.png")

        self.move_up_btn = ttk.Button(frame_botoes, width=20, text="Mover para cima", image=self.move_up_img,
                                      compound=LEFT, command=self.move_up)
        self.move_up_btn.pack(side=TOP, pady=2)

        self.move_down_img = tk.PhotoImage(file="./imagens/down.png")

        self.move_down_btn = ttk.Button(frame_botoes, width=20, text="Mover para baixo", image=self.move_down_img,
                                        compound=LEFT, command=self.move_down)
        self.move_down_btn.pack(side=TOP, pady=2)

        menu_bar = tk.Menu(main_frame)

        projeto_menu = tk.Menu(menu_bar, tearoff=0)
        projeto_menu.add_command(label="Projetos", command=self.lista_projetos)

        projeto_menu.add_command(label="Fechar Projeto", command=self.fechar_projeto_janela)
        projeto_menu.add_separator()
        projeto_menu.add_command(label="Sair", command=self.fechar_janela)
        menu_bar.add_cascade(label="Projetos", menu=projeto_menu)

        ajuda_menu = tk.Menu(menu_bar, tearoff=0)
        ajuda_menu.add_command(label="Ajuda", command=self.sobre)

        ajuda_menu.add_command(label="Licença", command=self.sobre)
        ajuda_menu.add_separator()
        ajuda_menu.add_command(label="Sobre", command=self.sobre)
        menu_bar.add_cascade(label="Sobre", menu=ajuda_menu)

        self.parent.config(menu=menu_bar)

    def lista_projetos(self):

        self.projeto_janela = Toplevel(self.parent)

        self.projeto_janela.title("Projetos")
        self.projeto_janela.geometry("400x400")
        self.projeto_janela.protocol("WM_DELETE_WINDOW", self.fechar_projeto_janela)

        self.projeto_janela.withdraw()
        self.projeto_janela.grid()
        self.projeto_janela.transient(self.parent)
        self.projeto_janela.grab_set()

        projeto_frame = Frame(self.projeto_janela)
        projeto_frame.pack(fill=BOTH, expand=True)

        fechar_btn = ttk.Button(self.projeto_janela, text="Fechar", width=10, command=self.fechar_projeto_janela)
        fechar_btn.pack(side=RIGHT, padx=5, pady=5)

        self.excluir_btn = ttk.Button(self.projeto_janela, text="Excluir", width=10, command=self.excluir_projeto)
        self.excluir_btn.pack(side=RIGHT, padx=5, pady=5)
        self.excluir_btn.state(["disabled"])

        self.abrir_btn = ttk.Button(self.projeto_janela, text="Abrir", width=10, command=self.abrir_projeto)
        self.abrir_btn.pack(side=RIGHT)
        self.abrir_btn.state(["disabled"])

        novo_btn = ttk.Button(self.projeto_janela, text="Novo", width=10, command=self.novo_projeto)
        novo_btn.pack(side=RIGHT, padx=5, pady=5)

        grid_frame = Frame(projeto_frame, bd=10)
        grid_frame.pack(fill=BOTH, expand=YES, side=LEFT)

        self.dataCols = ('nome', 'ultima_atualizacao')
        self.projetos_grid = ttk.Treeview(grid_frame, selectmode='browse', columns=self.dataCols)
        self.projetos_grid.bind("<Double-1>", self.abrir_projeto)
        self.projetos_grid.bind("<Button-1>", self.habilita_btn)

        scroll_y = ttk.Scrollbar(grid_frame, orient=VERTICAL, command=self.projetos_grid.yview)
        scroll_x = ttk.Scrollbar(grid_frame, orient=HORIZONTAL, command=self.projetos_grid.xview)
        self.projetos_grid['yscroll'] = scroll_y.set
        self.projetos_grid['xscroll'] = scroll_x.set

        scroll_y.configure(command=self.projetos_grid.yview)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.configure(command=self.projetos_grid.xview)
        scroll_x.pack(side=BOTTOM, fill=X)

        # setup column headings
        self.projetos_grid['show'] = 'headings'
        self.projetos_grid.heading('nome', text='Nome', anchor=W)
        self.projetos_grid.column('nome', stretch=0, width=200)
        self.projetos_grid.heading('ultima_atualizacao', text='Última Atualização', anchor=W)
        # self.projetos_grid.column('ultima_atualizacao', stretch=0, width=100)

        self.projetos_grid.pack(fill=BOTH, side=LEFT, expand=True)

        dados = ProjetosDb(self.db).listar_projetos()
        for row in dados:
            self.projetos_grid.insert('', END, row[0], values=(row[1], row[9]))

        centro_(self.projeto_janela)

        self.projeto_janela.deiconify()
        self.parent.wait_window(self.projeto_janela)

    def novo_projeto(self):

        self.novo_projeto_janela = Toplevel(self.parent)
        self.novo_projeto_janela.resizable(0, 0)

        self.novo_projeto_janela.title("Novo Projeto")
        self.novo_projeto_janela.geometry("700x400")
        self.novo_projeto_janela.protocol("WM_DELETE_WINDOW", self.fechar_novo_projeto)

        self.novo_projeto_janela.withdraw()
        self.novo_projeto_janela.grid()
        self.novo_projeto_janela.transient(self.parent)
        self.novo_projeto_janela.grab_set()

        projeto_frame = Frame(self.novo_projeto_janela)
        projeto_frame.pack(fill=BOTH, expand=True)

        cancelar_btn = ttk.Button(self.novo_projeto_janela, text="Cancelar", width=10, command=self.fechar_novo_projeto)
        cancelar_btn.pack(side=RIGHT, padx=5, pady=5)

        ok_btn = ttk.Button(self.novo_projeto_janela, text="Salvar", width=10, command=self.incluir_projeto)
        ok_btn.pack(side=RIGHT)

        info_frame = Frame(projeto_frame, bd=10)
        info_frame.pack(fill=BOTH, expand=YES, side=RIGHT)

        group_info = ttk.LabelFrame(info_frame, text="Informações", padding=(6, 6, 12, 12))
        group_info.grid(row=0, column=0, sticky='nsew')

        ttk.Label(group_info, text='Nome', width=10).grid(row=0, column=0, sticky=W)
        self.nome = ttk.Entry(group_info, width=25)
        self.nome.grid(row=0, column=1, sticky=W, pady=2)

        ttk.Label(group_info, text='Descrição', width=10).grid(row=1, column=0, sticky=W)
        self.descricao = Text(group_info, height=4, width=19)
        self.descricao.grid(row=1, column=1, sticky=W, pady=2)

        ttk.Label(group_info, text='Autor', width=10).grid(row=2, column=0, sticky=W)
        self.autor = ttk.Entry(group_info, width=25)
        self.autor.grid(row=2, column=1, sticky=W, pady=2)

        group_db = ttk.LabelFrame(info_frame, text="Acesso ao banco", padding=(6, 6, 12, 12))
        group_db.grid(row=1, column=0, sticky=NSEW)

        ttk.Label(group_db, text='Tipo', width=10).grid(row=0, column=0, sticky=W)
        self.box_value = tk.StringVar()
        self.box = ttk.Combobox(group_db, textvariable=self.box_value, width=22)
        self.box['values'] = ('', 'Oracle', 'Mysql', 'PostgreSql')
        self.box.current(0)
        self.box.grid(row=0, column=1, sticky=W, pady=2)

        ttk.Label(group_db, text='Servidor', width=10).grid(row=1, column=0, sticky=W)
        self.servidor = ttk.Entry(group_db, width=25)
        self.servidor.grid(row=1, column=1, sticky=W, pady=2)

        ttk.Label(group_db, text='Porta', width=10).grid(row=2, column=0, sticky=W)
        self.porta = ttk.Entry(group_db, width=15)
        self.porta.grid(row=2, column=1, sticky=W, pady=2)

        ttk.Label(group_db, text='Banco', width=10).grid(row=3, column=0, sticky=W)
        self.senha = ttk.Entry(group_db, width=25)
        self.senha.grid(row=3, column=1, sticky=W, pady=2)

        ttk.Label(group_db, text='Usuário', width=10).grid(row=4, column=0, sticky=W)
        self.usuario = ttk.Entry(group_db, width=25)
        self.usuario.grid(row=4, column=1, sticky=W, pady=2)

        ttk.Label(group_db, text='Senha', width=10).grid(row=5, column=0, sticky=W)
        self.senha = ttk.Entry(group_db, show="*", width=25)
        self.senha.grid(row=5, column=1, sticky=W, pady=2)

        centro_(self.novo_projeto_janela)

        self.novo_projeto_janela.deiconify()
        self.parent.wait_window(self.novo_projeto_janela)

    def alterar_projeto(self):

        self.alterar_projeto_janela = Toplevel(self.parent)
        self.alterar_projeto_janela.resizable(0, 0)

        self.alterar_projeto_janela.title("Novo Projeto")
        self.alterar_projeto_janela.geometry("700x500")
        self.alterar_projeto_janela.protocol("WM_DELETE_WINDOW", self.fechar_alterar_projeto)

        self.alterar_projeto_janela.withdraw()
        self.alterar_projeto_janela.grid()
        self.alterar_projeto_janela.transient(self.parent)
        self.alterar_projeto_janela.grab_set()

        projeto_frame = Frame(self.alterar_projeto_janela, relief=RAISED, borderwidth=1)
        projeto_frame.pack(fill=BOTH, expand=True)

        cancelar_btn = ttk.Button(self.alterar_projeto_janela, text="Cancelar", width=10, command=self.fechar_alterar_projeto)
        cancelar_btn.pack(side=RIGHT, padx=5, pady=5)

        ok_btn = ttk.Button(self.alterar_projeto_janela, text="Abrir", width=10, command=self.salvar_projeto)
        ok_btn.pack(side=RIGHT)

        info_frame = Frame(projeto_frame, bd=10)
        info_frame.pack(fill=BOTH, expand=YES, side=RIGHT)

        group_info = ttk.LabelFrame(info_frame, text="Informações", padding=(6, 6, 12, 12))
        group_info.grid(row=0, column=0, sticky='nsew')

        ttk.Label(group_info, text='Nome', width=10).grid(row=0, column=0, sticky=W)
        self.nome = ttk.Entry(group_info, width=25)
        self.nome.grid(row=0, column=1, sticky=W, pady=2)

        ttk.Label(group_info, text='Descrição', width=10).grid(row=1, column=0, sticky=W)
        self.descricao = Text(group_info, height=4, width=19)
        self.descricao.grid(row=1, column=1, sticky=W, pady=2)

        ttk.Label(group_info, text='Autor', width=10).grid(row=2, column=0, sticky=W)
        self.autor = Text(group_info, height=4, width=19)
        self.autor.grid(row=2, column=1, sticky=W, pady=2)

        group_db = ttk.LabelFrame(info_frame, text="Acesso ao banco", padding=(6, 6, 12, 12))
        group_db.grid(row=1, column=0, sticky='nsew')

        ttk.Label(group_db, text='Tipo', width=10).grid(row=0, column=0, sticky=W)
        self.box_value = tk.StringVar()
        self.box = ttk.Combobox(group_db, textvariable=self.box_value, width=22)
        self.box['values'] = ('', 'Oracle', 'Mysql', 'PostgreSql')
        self.box.current(0)
        self.box.grid(row=0, column=1, sticky=W, pady=2)

        ttk.Label(group_db, text='Servidor', width=10).grid(row=1, column=0, sticky=W)
        self.servidor = ttk.Entry(group_db, width=25)
        self.servidor.grid(row=2, column=0, sticky=W, pady=2)

        ttk.Label(group_db, text='Porta', width=10).grid(row=1, column=0, sticky=W)
        self.porta = ttk.Entry(group_db, width=25)
        self.usuario.grid(row=2, column=1, sticky=W, pady=2)

        ttk.Label(group_db, text='Banco', width=10).grid(row=3, column=0, sticky=W)
        self.senha = ttk.Entry(group_db, width=25)
        self.senha.grid(row=3, column=1, sticky=W, pady=2)

        ttk.Label(group_db, text='Usuário', width=10).grid(row=4, column=0, sticky=W)
        self.usuario = ttk.Entry(group_db, width=25)
        self.usuario.grid(row=4, column=1, sticky=W, pady=2)

        ttk.Label(group_db, text='Senha', width=10).grid(row=5, column=0, sticky=W)
        self.usuario = ttk.Entry(group_db, show="*", width=25)
        self.usuario.grid(row=5, column=1, sticky=W, pady=2)

        centro_(self.alterar_projeto_janela)

        self.alterar_projeto_janela.deiconify()
        self.parent.wait_window(self.projeto_janela)

    def lista_relatorios(self, relatorios):

        self.relatorios = relatorios

        for row in self.relatorios:
            self.relatorios_grid.insert("", END, row[0], values=(row[2], row[8]))

    def excluir_projeto(self):
        if deleteBox("Excluir", "Deseja realmente excluir o projeto selecionado?"):
            item = self.projetos_grid.selection()[0]
            self.projetos_grid.delete(item)

            ProjetosDb(self.db).excluirProjeto(item)

            print("Projeto excluído: ", item)

    def salvar_projeto(self):
        self.projeto_janela.destroy()

    def fechar_janela(self):
        self.parent.destroy()

    def fechar_projeto_janela(self):
        self.projeto_janela.destroy()

    def fechar_novo_projeto(self):
        self.novo_projeto_janela.destroy()

    def fechar_alterar_projeto(self):
        self.alterar_projeto_janela.destroy()

    def iniciar(self):
        pass

    def cancelar(self):
        pass

    def novo_relatorio(self):
        app = Relatorio(self.parent, self.db)
        app.novo_relatorio()

    def alterar_relatorio(self):
        app = Relatorio(self.parent)
        app.alterar_relatorio()

    def alterar_relatorio_click(self, event):
        item = self.relatorios_grid.selection()[0]

        app = Relatorio(self.parent)
        app.alterar_relatorio()

        print("you clicked on", self.relatorios_grid.item(item, "text"))

    def excluir_relatorio(self):
        print("Relatório excluído")

    def move_up(self):
        leaves = self.relatorios_grid.selection()
        print("item: ", leaves)
        for i in leaves:
            self.relatorios_grid.move(i, self.relatorios_grid.parent(i), self.relatorios_grid.index(i) - 1)

    def move_down(self):
        leaves = self.relatorios_grid.selection()
        for i in leaves:
            self.relatorios_grid.move(i, self.relatorios_grid.parent(i), self.relatorios_grid.index(i) + 1)

    def sobre(self):
        app = Sobre(self.parent)

    def abrir_projeto(self, event):

        projeto_id = self.projetos_grid.selection()[0]

        relatorios_lista = RelatoriosDb(self.db).listar_relatorios(projeto_id)
        print(relatorios_lista)

        self.lista_relatorios(relatorios_lista)

        self.fechar_projeto_janela()

    def habilita_btn(self, event):
        self.excluir_btn.state(["!disabled"])
        self.abrir_btn.state(["!disabled"])

    def novo_projeto(self):

        arr = []
        arr.append(self.nome.get())
        arr.append(self.descricao.get())
        arr.append(self.autor.get())
        arr.append(self.bancos.get())
        arr.append(self.nome.get())
        arr.append(self.usuario.get())
        arr.append(self.senha.get())

        retorno = ProjetosDb(self.db).incluir_projeto(arr)
        if retorno.isnumeric:
            self.projetos_grid.insert('', END, arr[0], values=(row[1], row[9]))

        self.fechar_projeto()


class Relatorio:
    def __init__(self, master, db):
        self.master = master
        self.db = db

    def novo_relatorio(self):
        self.relatorio_janela = Toplevel()
        self.relatorio_janela.resizable(0, 0)

        self.relatorio_janela.title("Novo Relatório")
        self.relatorio_janela.geometry("500x300")
        self.relatorio_janela.protocol("WM_DELETE_WINDOW", self.on_close)

        self.relatorio_janela.withdraw()
        self.relatorio_janela.grid()
        self.relatorio_janela.transient(self.master)
        self.relatorio_janela.grab_set()

        relatorio_frame = Frame(self.relatorio_janela, relief=RAISED, borderwidth=1)
        relatorio_frame.pack(fill=BOTH, expand=True)

        self.relatorio_tab = ttk.Notebook(relatorio_frame)
        self.relatorio_tab.pack(fill=BOTH, expand=True)

        cancelar_btn = ttk.Button(self.relatorio_janela, text="Cancelar", width=10, command=self.on_close)
        cancelar_btn.pack(side=RIGHT, padx=5, pady=5)

        ok_btn = ttk.Button(self.relatorio_janela, text="Incluir", width=10, command=self.salvar)
        ok_btn.pack(side=RIGHT)

        frame_informacaoes = ttk.Frame(self.relatorio_tab)
        frame_informacaoes.pack(side=BOTTOM, expand=YES)

        informacoes_bas = ttk.LabelFrame(frame_informacaoes)
        frame_informacaoes.pack(side=BOTTOM, expand=YES)

        # data Nomor
        ttk.Label(frame_informacaoes, text='Nomor Urut').grid(
            row=0, column=0, sticky=W)
        self.entNomor = ttk.Entry(frame_informacaoes)
        self.entNomor.grid(row=0, column=1)

        # data Nama
        ttk.Label(frame_informacaoes, text='Nama Lengkap').grid(
            row=1, column=0, sticky=W)
        self.entNama = ttk.Entry(frame_informacaoes)
        self.entNama.grid(row=1, column=1)

        # data Alamat
        ttk.Label(frame_informacaoes, text='Alamat').grid(
            row=2, column=0, sticky=W)
        self.entAlamat = ttk.Entry(frame_informacaoes)
        self.entAlamat.grid(row=2, column=1)

        # data NoTelp
        ttk.Label(frame_informacaoes, text='No. Telp').grid(
            row=3, column=0, sticky=W)
        self.entTelp = ttk.Entry(frame_informacaoes)
        self.entTelp.grid(row=3, column=1)

        # data Kelas
        ttk.Label(frame_informacaoes, text='Kelas').grid(
            row=4, column=0, sticky=W)
        self.entKelas = ttk.Entry(frame_informacaoes)
        self.entKelas.grid(row=4, column=1)

        f2 = ttk.Frame(self.relatorio_tab)  # second page
        f3 = ttk.Frame(self.relatorio_tab)  # second page

        self.relatorio_tab.add(frame_informacaoes, text='Informações')
        self.relatorio_tab.add(f2, text='Consulta')
        self.relatorio_tab.add(f3, text='Configuração')

        centro_(self.relatorio_janela)

        self.relatorio_janela.deiconify()
        self.master.wait_window(self.relatorio_janela)

    def alterar_relatorio(self):
        self.relatorio_janela = Toplevel()
        self.relatorio_janela.resizable(0, 0)

        self.relatorio_janela.title("Alterar Relatório")
        self.relatorio_janela.geometry("500x300")
        self.relatorio_janela.protocol("WM_DELETE_WINDOW", self.on_close)

        self.relatorio_janela.withdraw()
        self.relatorio_janela.grid()
        self.relatorio_janela.transient(self.master)
        self.relatorio_janela.grab_set()

        relatorio_frame = Frame(self.relatorio_janela, relief=RAISED, borderwidth=1)
        relatorio_frame.pack(fill=BOTH, expand=True)

        self.relatorio_tab = ttk.Notebook(relatorio_frame)
        self.relatorio_tab.pack(fill=BOTH, expand=True)

        cancelar_btn = ttk.Button(self.relatorio_janela, text="Cancelar", width=10, command=self.on_close)
        cancelar_btn.pack(side=RIGHT, padx=5, pady=5)

        ok_btn = ttk.Button(self.relatorio_janela, text="Incluir", width=10, command=self.salvar)
        ok_btn.pack(side=RIGHT)

        f1 = ttk.Frame(self.relatorio_tab)  # first page, which would get widgets gridded into it
        f1.pack(side=BOTTOM, expand=YES)

        f2 = ttk.Frame(self.relatorio_tab)  # second page
        f3 = ttk.Frame(self.relatorio_tab)  # second page
        self.relatorio_tab.add(f1, text='Informações')
        self.relatorio_tab.add(f2, text='Consulta')
        self.relatorio_tab.add(f3, text='Configuração')

        centro_(self.relatorio_janela)

        self.relatorio_janela.deiconify()
        self.master.wait_window(self.relatorio_janela)

    def on_close(self):
        self.relatorio_janela.destroy()

    def salvar(self):
        self.projeto_janela.destroy()


class Sobre:
    def __init__(self, master):
        self.master = master

        self.sobre_janela = Toplevel()
        self.sobre_janela.resizable(0, 0)

        self.sobre_janela.title("Sobre")
        self.sobre_janela.geometry("400x300")
        self.sobre_janela.protocol("WM_DELETE_WINDOW", self.on_close)

        self.sobre_janela.withdraw()
        self.sobre_janela.grid()
        self.sobre_janela.transient(self.master)
        self.sobre_janela.grab_set()

        sobre_frame = Frame(self.sobre_janela, relief=RAISED, borderwidth=1)
        sobre_frame.pack(fill=BOTH, expand=True)

        ok_btn = ttk.Button(self.sobre_janela, text="Ok", width=10, command=self.on_close)
        ok_btn.pack(side=RIGHT)

        # frame_kiri
        grid_frame = Frame(sobre_frame, bd=10)
        grid_frame.pack(fill=BOTH, expand=YES, side=LEFT)

        centro_(self.sobre_janela)

        self.sobre_janela.deiconify()
        self.master.wait_window(self.sobre_janela)

    def on_close(self):
        self.sobre_janela.destroy()


class DbInterno(object):
    ''' A classe DbInterno representa o banco de dados. '''

    def __init__(self, db_name):
        try:
            # conectando...
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
            # imprimindo nome do banco
            print("Banco:", db_name)
            # lendo a versão do SQLite
            self.cursor.execute('SELECT SQLITE_VERSION()')
            self.data = self.cursor.fetchone()
            # imprimindo a versão do SQLite
            print("SQLite version: %s" % self.data)

            fd = open('./data/base.sql', 'r')
            sql_file = fd.read()
            fd.close()

            print("Criando tabelas ...")
            try:
                self.cursor.executescript(sql_file)
            except sqlite3.Error:
                print("Aviso: As tabelas já existem.")
                # return False

            print("Tabelas criadas com sucesso.")

        except sqlite3.Error as er:
            print("Erro ao abrir banco. ", er.message)
        # return False


    def commit_db(self):
        if self.conn:
            self.conn.commit()


    def close_db(self):
        if self.conn:
            self.conn.close()
            print("Conexão fechada.")


class ProjetosDb(object):
    ''' A classe ProjetosDb representa um projeto no banco de dados. '''

    def __init__(self, db):
        self.db = db

    def incluir_projeto(self, dados):
        try:
            self.db.cursor.execute("""
            INSERT INTO projetos (nome, desc, autor, banco, conexao, usuario_db, pass_db, criado_em, alterado_em)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (dados[0], dados[1], dados[2], dados[3], dados[4], dados[5], dados[6], dados[7], dados[8],))
            # gravando no bd
            self.db.commit_db()
            print("Um registro inserido com sucesso.")
        except sqlite3.IntegrityError:
            print("Aviso: O email deve ser único.")
            return False

    def listar_projetos(self):
        sql = 'SELECT * FROM projetos ORDER BY nome'
        r = self.db.cursor.execute(sql)
        return r.fetchall()

    def localizar_projeto(self, id):
        r = self.db.cursor.execute(
            'SELECT * FROM projetos WHERE id = ?', (id,))
        return r.fetchone()

    def atualizarProjeto(self, id):
        try:
            c = self.localizar_projeto(id)
            if c:
                # solicitando os dados ao usuário
                # se for no python2.x digite entre aspas simples
                self.novo_fone = input('Fone: ')
                self.db.cursor.execute("""
                UPDATE projetos
                SET fone = ?
                WHERE id = ?
                """, (self.novo_fone, id,))
                # gravando no bd
                self.db.commit_db()
                print("Dados atualizados com sucesso.")
            else:
                print('Não existe cliente com o id informado.')
        except e:
            raise e

    def excluirProjeto(self, id):
        try:
            projeto = self.localizar_projeto(id)
            # verificando se existe cliente com o ID passado, caso exista
            if projeto:
                self.db.cursor.execute("""
                DELETE FROM projetos WHERE id = ?
                """, (id,))
                # gravando no bd
                self.db.commit_db()
                print("Registro excluído com sucesso.")
            else:
                print('Não existe projeto com o código informado.')
        except e:
            raise e

        '''
        def novoRelatorio(self):

            cursor.execute("""
            INSERT INTO clientes (nome, idade, cpf, email, fone, cidade, uf, criado_em)
            VALUES (?,?,?,?,?,?,?,?)
            """, (p_nome, p_idade, p_cpf, p_email, p_fone, p_cidade, p_uf, p_criado_em))

            conn.commit()
            '''


class RelatoriosDb(object):
    ''' A classe ProjetosDb representa um projeto no banco de dados. '''

    def __init__(self, db):
        self.db = db

    def incluir_relatorio(self, nome):
        try:
            self.db.cursor.execute("""
            INSERT INTO relatorios (
                           id,
                           projeto_id,
                           nome,
                           descricao,
                           sql,
                           ordem,
                           operacao,
                           autor,
                           criado_em,
                           alterado_em
                       )
                       VALUES (
                           'id',
                           'projeto_id',
                           'desc',
                           'sql',
                           'proximo_id',
                           'operacao',
                           'autor',
                           'criado_em',
                           'alterado_em'
                       )""")
            # gravando no bd
            self.db.commit_db()
            print("Um registro inserido com sucesso.")
        except sqlite3.IntegrityError:
            print("Aviso: O email deve ser único.")
            return False

    def listar_relatorios(self, projeto_id):
        sql = 'SELECT * FROM relatorios WHERE projeto_id = ? ORDER BY desc'
        r = self.db.cursor.execute(sql, (projeto_id,))
        return r.fetchall()

    def localizar_projeto(self, id):
        r = self.db.cursor.execute(
            'SELECT * FROM projetos WHERE id = ?', (id,))
        return r.fetchone()

    def atualizarProjeto(self, id):
        try:
            c = self.localizar_projeto(id)
            if c:
                # solicitando os dados ao usuário
                # se for no python2.x digite entre aspas simples
                self.novo_fone = input('Fone: ')
                self.db.cursor.execute("""
                UPDATE projetos
                SET fone = ?
                WHERE id = ?
                """, (self.novo_fone, id,))
                # gravando no bd
                self.db.commit_db()
                print("Dados atualizados com sucesso.")
            else:
                print('Não existe cliente com o id informado.')
        except e:
            raise e

    def excluirProjeto(self, id):
        try:
            c = self.localizar_cliente(id)
            # verificando se existe cliente com o ID passado, caso exista
            if c:
                self.db.cursor.execute("""
                DELETE FROM projetos WHERE id = ?
                """, (id,))
                # gravando no bd
                self.db.commit_db()
                print("Registro %d excluído com sucesso." % id)
            else:
                print('Não existe projeto com o código informado.')
        except e:
            raise e

        '''
        def novoRelatorio(self):

            cursor.execute("""
            INSERT INTO clientes (nome, idade, cpf, email, fone, cidade, uf, criado_em)
            VALUES (?,?,?,?,?,?,?,?)
            """, (p_nome, p_idade, p_cpf, p_email, p_fone, p_cidade, p_uf, p_criado_em))

            conn.commit()
            '''


if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(0, 0)
    root.attributes('-alpha', 0.0)

    db = DbInterno('./data/relat.db')

    app = Relat(root, db)

    centro(root)

    root.attributes('-alpha', 1.0)
    root.mainloop()

    db.close_db()
