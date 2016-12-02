import tkinter as tk
from tkinter import ttk, messagebox, Frame, Label, Listbox, TOP, LEFT, BOTH, X, Y, W, RIGHT, \
    YES, SUNKEN, BOTTOM, VERTICAL, Toplevel, RAISED, HORIZONTAL
import sqlite3

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


def hello():
    messagebox.showinfo("Say Hello", "Hello World")


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

    def __init__(self, parent):
        self.parent = parent
 
        self.parent.title("Relat")
        self.parent.geometry("700x450")
        self.parent.protocol("WM_DELETE_WINDOW", self.on_close)

        #CONEXÃO COM BANCO DE DADOS
        self.db = DbInterno('./data/relat.db')

        main_frame = Frame(self.parent)
        main_frame.pack(fill=BOTH, expand=YES)

        #TOOLBAR
        toolbar = Frame(main_frame)
        toolbar.pack(side=TOP, fill=X)

        self.novo_projeto_img = tk.PhotoImage(file="./imagens/btn.png")

        novo_projeto_btn = ttk.Button(toolbar, image=self.novo_projeto_img, command=self.novo_projeto)
        novo_projeto_btn.pack(side=LEFT, padx=1, pady=1)

        self.abrir_projeto_img = tk.PhotoImage(file="./imagens/btn.png")

        abrir_projeto_btn = ttk.Button(toolbar, image=self.abrir_projeto_img, command=self.abrir_projeto)
        abrir_projeto_btn.pack(side=LEFT, padx=2, pady=2)

        ttk.Separator(toolbar).pack(side=LEFT, padx=1, pady=1)

        self.sobre_img = tk.PhotoImage(file="./imagens/btn.png")

        sobre_btn = ttk.Button(toolbar, image=self.sobre_img, command=self.sobre)
        sobre_btn.pack(side=LEFT, padx=2, pady=2)

        ttk.Separator(toolbar).pack(side=LEFT, padx=1, pady=1)

        self.encerrar_img = tk.PhotoImage(file="./imagens/btn.png")

        encerrar_btn = ttk.Button(toolbar, image=self.encerrar_img, command=self.on_close)
        encerrar_btn.pack(side=LEFT, padx=2, pady=2)

        status_bar = Label(main_frame, text="www.KlinikPython.Wordpress.Com",
                           relief=SUNKEN, bd=1)
        status_bar.pack(side=BOTTOM, fill=X)

        frame_central = ttk.Notebook(main_frame)

        grid_frame = Frame(frame_central)

        scroll = ttk.Scrollbar(grid_frame, orient=VERTICAL)
        self.relatorios_grid = ttk.Treeview(grid_frame, yscrollcommand=scroll.set)

        self.relatorios_grid.pack(side=LEFT, fill=BOTH, expand=True)
        scroll.configure(command=self.relatorios_grid.yview)
        scroll.pack(side=RIGHT, fill=Y)

        self.relatorios_grid["columns"] = ("desc", "ult_execucao")
        self.relatorios_grid.column("desc", width=150)
        self.relatorios_grid.column("ult_execucao", width=80)
        self.relatorios_grid.heading("desc", text="Descrição")
        self.relatorios_grid.heading("ult_execucao", text="Última Execução")

        for i in range(10):
            self.relatorios_grid.insert("", "end", text="Item %s" % i)

        self.relatorios_grid.bind("<Double-1>", self.alterar_relatorio_click)

        frame_central.add(grid_frame, text="Relatórios")

        frame_central.add(Frame(), text="Configurações")

        frame_central.pack(side=LEFT, fill=BOTH, expand=1)

        frame_botoes = Frame(main_frame, width=200, padx=20, pady=30)
        frame_botoes.pack(side=RIGHT, fill=Y)

        self.iniciar_img = tk.PhotoImage(file="./imagens/btn.png")

        self.iniciar_btn = ttk.Button(frame_botoes, text="Iniciar", width=20, image=self.iniciar_img, compound=LEFT,
                                      command=self.iniciar)
        # self.iniciar_btn.state(['disabled'])  # set the disabled flag, disabling the button
        # self.iniciar_btn.state(['!disabled'])
        self.iniciar_btn.pack(side=TOP, pady=2)

        self.cancelar_img = tk.PhotoImage(file="./imagens/btn.png")

        self.cancelar_btn = ttk.Button(frame_botoes, text="Cancelar", width=20, image=self.cancelar_img, compound=LEFT,
                                       command=self.cancelar)
        self.cancelar_btn.pack(side=TOP, pady=2)

        ttk.Separator(frame_botoes).pack(side=TOP, padx=10, pady=1)

        self.novo_relatorio_img = tk.PhotoImage(file="./imagens/btn.png")

        self.novo_relatorio_btn = ttk.Button(frame_botoes, width=20, text="Incluir", image=self.cancelar_img,
                                             compound=LEFT, command=self.novo_relatorio)
        self.novo_relatorio_btn.pack(side=TOP, pady=2)

        self.alterar_relatorio_img = tk.PhotoImage(file="./imagens/btn.png")

        self.alterar_relatorio_btn = ttk.Button(frame_botoes, width=20, text="Alterar", image=self.alterar_relatorio_img,
                                              compound=LEFT, command=self.alterar_relatorio)
        self.alterar_relatorio_btn.pack(side=TOP, pady=2)

        self.excluir_relatorio_img = tk.PhotoImage(file="./imagens/btn.png")

        self.excluir_relatorio_btn = ttk.Button(frame_botoes, width=20, text="Excluir",
                                                image=self.excluir_relatorio_img, compound=LEFT,
                                                command=self.excluir_relatorio)
        self.excluir_relatorio_btn.pack(side=TOP, pady=2)

        ttk.Separator(frame_botoes).pack(side=TOP, padx=10, pady=1)

        self.move_up_img = tk.PhotoImage(file="./imagens/btn.png")

        self.move_up_btn = ttk.Button(frame_botoes, width=20, text="Mover para cima", image=self.move_up_img,
                                      compound=LEFT, command=self.move_up)
        self.move_up_btn.pack(side=TOP, pady=2)

        self.move_down_img = tk.PhotoImage(file="./imagens/btn.png")

        self.move_down_btn = ttk.Button(frame_botoes, width=20, text="Mover para baixo", image=self.move_down_img,
                                        compound=LEFT, command=self.move_down)
        self.move_down_btn.pack(side=TOP, pady=2)

    def on_close(self, event=None):
        self.parent.destroy()

    def move_up(self):
        leaves = self.relatorios_grid.selection()
        print("item: ", leaves)
        for i in leaves:
            self.relatorios_grid.move(i, self.relatorios_grid.parent(i), self.relatorios_grid.index(i) - 1)

    def move_down(self):
        leaves = self.relatorios_grid.selection()
        for i in leaves:
            self.relatorios_grid.move(i, self.relatorios_grid.parent(i), self.relatorios_grid.index(i) + 1)

    def novo_projeto(self):
        app = Projeto(self.parent)
        app.novo_projeto()

    def abrir_projeto(self):
        app = Projeto(self.parent)
        app.abrir_projeto()

    def iniciar(self):
        pass

    def cancelar(self):
        pass

    def novo_relatorio(self):
        app = Relatorio(self.parent)
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
        app = Projeto(self.parent)
        app.excluir_relatorio()

    def sobre(self):
        app = Sobre(self.parent)


class Projeto:
    
    def __init__(self, master):

        self.master = master

    def novo_projeto(self):

        self.projeto_janela = Toplevel()

        self.projeto_janela.title("Novo Projeto")
        self.projeto_janela.geometry("700x300")
        self.projeto_janela.protocol("WM_DELETE_WINDOW", self.on_close)

        self.projeto_janela.withdraw()
        self.projeto_janela.grid()
        self.projeto_janela.transient(self.master)
        self.projeto_janela.grab_set()

        projeto_frame = Frame(self.projeto_janela, relief=RAISED, borderwidth=1)
        projeto_frame.pack(fill=BOTH, expand=True)

        cancelar_btn = ttk.Button(self.projeto_janela, text="Fechar", width=10, command=self.on_close)
        cancelar_btn.pack(side=RIGHT, padx=5, pady=5)

        ok_btn = ttk.Button(self.projeto_janela, text="Incluir", width=10, command=self.salvar)
        ok_btn.pack(side=RIGHT)

        # frame_kiri
        grid_frame = Frame(projeto_frame, bd=10)
        grid_frame.pack(fill=BOTH, expand=YES, side=LEFT)

        scroll = ttk.Scrollbar(grid_frame, orient=VERTICAL)

        self.projetos_grid = ttk.Treeview(grid_frame, yscrollcommand=scroll.set)

        self.projetos_grid.pack(fill=Y, side=LEFT)

        scroll.configure(command=self.projetos_grid.yview)
        scroll.pack(side=LEFT, fill=Y)

        self.projetos_grid["columns"] = ("description", "last_update")
        self.projetos_grid.column("description", width=100)
        self.projetos_grid.column("last_update", width=100)
        self.projetos_grid.heading("description", text="Descrição")
        self.projetos_grid.heading("last_update", text="Última Atualização")

        self.projetos_grid.insert("", 0, text="Line 1", values=("1A","1b"))
        self.projetos_grid.insert("", 1, text="Line 2", values=("2A", "2b"))
        self.projetos_grid.insert("", 2, text="Line 3", values=("3A", "3b"))

        id2 = self.projetos_grid.insert("", 3, "dir2", text="Dir 2")
        self.projetos_grid.insert(id2, "end", "dir 2", text="sub dir 2", values=("2A","2B"))

        ##alternatively:
        self.projetos_grid.insert("", 4, "dir3", text="Dir 3")
        self.projetos_grid.insert("dir3", 4, text=" sub dir 3",values=("3A"," 3B"))

        # frame_kanan
        fr_kanan = Frame(grid_frame, bd=10)
        fr_kanan.pack(fill=BOTH, expand=YES, side=RIGHT)

        # fr_kanan_atas
        fr_katas = Frame(fr_kanan)
        fr_katas.pack(side=TOP, expand=YES)

        # data Nomor
        ttk.Label(fr_katas, text='Nomor Urut').grid(
            row=0, column=0, sticky=W)
        self.entNomor = ttk.Entry(fr_katas)
        self.entNomor.grid(row=0, column=1)

        # data Nama
        ttk.Label(fr_katas, text='Nama Lengkap').grid(
            row=1, column=0, sticky=W)
        self.entNama = ttk.Entry(fr_katas)
        self.entNama.grid(row=1, column=1)

        # data Alamat
        ttk.Label(fr_katas, text='Alamat').grid(
            row=2, column=0, sticky=W)
        self.entAlamat = ttk.Entry(fr_katas)
        self.entAlamat.grid(row=2, column=1)

        # data NoTelp
        ttk.Label(fr_katas, text='No. Telp').grid(
            row=3, column=0, sticky=W)
        self.entTelp = ttk.Entry(fr_katas)
        self.entTelp.grid(row=3, column=1)

        # data Kelas
        ttk.Label(fr_katas, text='Kelas').grid(
            row=4, column=0, sticky=W)
        self.entKelas = ttk.Entry(fr_katas)
        self.entKelas.grid(row=4, column=1)

        # fr_kanan_bawah
        fr_kawah = Frame(fr_kanan)
        fr_kawah.pack(side=BOTTOM, expand=YES)

        centro_(self.projeto_janela)

        self.projeto_janela.deiconify()
        self.master.wait_window(self.projeto_janela)

    def abrir_projeto(self):

        self.projeto_janela = Toplevel()

        self.projeto_janela.title("Abrir Projeto")
        self.projeto_janela.geometry("400x300")
        self.projeto_janela.protocol("WM_DELETE_WINDOW", self.on_close)

        self.projeto_janela.withdraw()
        self.projeto_janela.grid()
        self.projeto_janela.transient(self.master)
        self.projeto_janela.grab_set()

        projeto_frame = Frame(self.projeto_janela, relief=RAISED, borderwidth=1)
        projeto_frame.pack(fill=BOTH, expand=True)

        cancelar_btn = ttk.Button(self.projeto_janela, text="Cancelar", width=10, command=self.on_close)
        cancelar_btn.pack(side=RIGHT, padx=5, pady=5)

        ok_btn = ttk.Button(self.projeto_janela, text="Abrir", width=10, command=self.salvar)
        ok_btn.pack(side=RIGHT)

        # frame_kiri
        grid_frame = Frame(projeto_frame, bd=10)
        grid_frame.pack(fill=BOTH, expand=YES, side=LEFT)

        scroll = ttk.Scrollbar(grid_frame, orient=VERTICAL)

        self.projetos_grid = ttk.Treeview(grid_frame, yscrollcommand=scroll.set)

        self.projetos_grid.pack(fill=Y, side=LEFT)

        scroll.configure(command=self.projetos_grid.yview)
        scroll.pack(side=LEFT, fill=Y)

        self.projetos_grid["columns"] = ("description", "last_update")
        self.projetos_grid.column("description", width=100)
        self.projetos_grid.column("last_update", width=100)
        self.projetos_grid.heading("description", text="Descrição")
        self.projetos_grid.heading("last_update", text="Última Atualização")

        self.projetos_grid.insert("", 0, text="Line 1", values=("1A","1b"))
        self.projetos_grid.insert("", 1, text="Line 2", values=("2A", "2b"))
        self.projetos_grid.insert("", 2, text="Line 3", values=("3A", "3b"))

        id2 = self.projetos_grid.insert("", 3, "dir2", text="Dir 2")
        self.projetos_grid.insert(id2, "end", "dir 2", text="sub dir 2", values=("2A","2B"))

        ##alternatively:
        self.projetos_grid.insert("", 4, "dir3", text="Dir 3")
        self.projetos_grid.insert("dir3", 4, text=" sub dir 3",values=("3A"," 3B"))

        centro_(self.projeto_janela)

        self.projeto_janela.deiconify()
        self.master.wait_window(self.projeto_janela)

    def on_close(self):
        self.projeto_janela.destroy()

    def salvar(self):
        self.projeto_janela.destroy()

class Relatorio:
    def __init__(self, master):
        self.master = master

    def novo_relatorio(self):
        self.relatorio_janela = Toplevel()

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

            # all SQL commands (split on ';')
            sqlCommands = sql_file.split(';')

            print("Criando tabelas ...")

            # Execute every command from the input file
            for command in sqlCommands:
                # This will skip and report errors
                # For example, if the tables do not yet exist, this will skip over
                # the DROP TABLE commands
                try:
                    self.cursor.executescript(command)
                except sqlite3.Error:
                    print("Aviso: As tabelas já existem.")
                    #return False

            print("Tabelas criadas com sucesso.")

        except sqlite3.Error as er:
            print("Erro ao abrir banco. ", er.message)
            #return False

    def commit_db(self):
        if self.conn:
            self.conn.commit()

    def close_db(self):
        if self.conn:
            self.conn.close()
            print("Conexão fechada.")


class ProjetosDb(object):
    ''' A classe RelatDb representa um cliente no banco de dados. '''

    def __init__(self):
        #print("Criando tabela 'Projetos'")

        try:
            self.db.cursor.execute("""

            );
        """)
        except sqlite3.Error:
            print("Aviso: A tabela 'Projetos' já existe.")
            return False

        print("Tabela 'Projetos' criada com sucesso.")

        print("Criando tabela 'Relatorios'.")

        try:
            self.db.cursor.execute("""

        """)
        except sqlite3.Error:
            print("Aviso: A tabela 'Relatorios' já existe.")
            return False

        print("Tabela 'Relatorios' criada com sucesso.")


    def novoProjeto(self):

        try:
            self.db.cursor.execute("""
            INSERT INTO clientes (nome, idade, cpf, email, fone, cidade, uf, criado_em)
            VALUES ('Regis da Silva', 35, '12345678901', 'regis@email.com', '(11) 9876-5342',
            'São Paulo', 'SP', '2014-07-30 11:23:00.199000')
            """)
            # gravando no bd
            self.db.commit_db()
            print("Um registro inserido com sucesso.")
        except sqlite3.IntegrityError:
            print("Aviso: O email deve ser único.")
            return False

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
    root.attributes('-alpha', 0.0)

    db = DbInterno('./data/relat.db')

    app = Relat(root)
    
    centro(root)
    
    root.attributes('-alpha', 1.0)
    root.mainloop()

    db.fechar_conexao()

