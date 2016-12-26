import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import ttk, font,  messagebox, Frame, Label, Text, Listbox, TOP, LEFT, BOTH, X, Y, W, EW, NSEW, RIGHT, END, \
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

    #Guarda o ID do projeto aberto
    projeto_aberto = 0

    #Janela prncipal
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db

        self.parent.title("Relat")
        self.parent.geometry("700x450")
        self.parent.protocol("WM_DELETE_WINDOW", self.fechar_janela_ctrl)

        main_frame = Frame(self.parent)
        main_frame.pack(fill=BOTH, expand=YES)

        # TOOLBAR
        toolbar = Frame(main_frame)
        toolbar.pack(side=TOP, fill=X)

        self.projeto_img = tk.PhotoImage(file="./imagens/projetos.png")

        self.lista_projetos_btn = ttk.Button(toolbar, image=self.projeto_img, command=self.lista_projetos)
        self.lista_projetos_btn.pack(side=LEFT, padx=2, pady=2)

        self.iniciar_img = tk.PhotoImage(file="./imagens/iniciar.png")

        self.iniciar_btn = ttk.Button(toolbar, image=self.iniciar_img, command=self.iniciar_ctrl)
        self.iniciar_btn.state(['disabled'])  # set the disabled flag, disabling the button
        self.iniciar_btn.pack(side=LEFT, pady=1)

        self.cancelar_img = tk.PhotoImage(file="./imagens/stop.png")

        self.cancelar_btn = ttk.Button(toolbar, image=self.cancelar_img, command=self.cancelar_ctrl)
        self.cancelar_btn.state(['disabled'])  # set the disabled flag, disabling the button
        # self.cancelar_btn.state(['!disabled'])

        self.cancelar_btn.pack(side=LEFT, pady=1)

        self.sair_img = tk.PhotoImage(file="./imagens/sair.png")

        self.sair_btn = ttk.Button(toolbar, image=self.sair_img, command=self.fechar_janela_ctrl)
        self.sair_btn.pack(side=LEFT, pady=1)

        status_bar = Frame(main_frame)
        status_bar.pack(side=BOTTOM, fill=X)

        self.text_status_bar = Label(status_bar, text="www.KlinikPython.Wordpress.Com", relief=SUNKEN, bd=1)
        self.text_status_bar.pack(side=LEFT, fill=X, expand=True)

        frame_central = ttk.Notebook(main_frame)

        grid_frame = Frame(frame_central, bd=10)
        grid_frame.pack(fill=BOTH, expand=YES, side=LEFT)

        self.dataCols = ('nome', 'ultima_atualizacao')
        self.relatorios_grid = ttk.Treeview(grid_frame, selectmode='browse', columns=self.dataCols)
        self.relatorios_grid.bind("<Double-1>", self.alterar_relatorio_click)
        self.relatorios_grid.bind("<Button-1>", self.habilita_btn_relat)

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
        self.novo_relatorio_btn.state(['disabled'])
        self.novo_relatorio_btn.pack(side=TOP, pady=2)

        self.alterar_relatorio_img = tk.PhotoImage(file="./imagens/alterar.png")

        self.alterar_relatorio_btn = ttk.Button(frame_botoes, width=20, text="Alterar",
                                                image=self.alterar_relatorio_img,
                                                compound=LEFT, command=self.alterar_relatorio)
        self.alterar_relatorio_btn.state(['disabled'])
        self.alterar_relatorio_btn.pack(side=TOP, pady=2)

        self.excluir_relatorio_img = tk.PhotoImage(file="./imagens/excluir.png")

        self.excluir_relatorio_btn = ttk.Button(frame_botoes, width=20, text="Excluir",
                                                image=self.excluir_relatorio_img, compound=LEFT,
                                                command=self.excluir_relatorio_ctrl)
        self.excluir_relatorio_btn.state(['disabled'])
        self.excluir_relatorio_btn.pack(side=TOP, pady=2)

        self.move_up_img = tk.PhotoImage(file="./imagens/up.png")

        self.move_up_btn = ttk.Button(frame_botoes, width=20, text="Mover para cima", image=self.move_up_img,
                                      compound=LEFT, command=self.move_up_ctrl)
        self.move_up_btn.state(['disabled'])
        self.move_up_btn.pack(side=TOP, pady=2)

        self.move_down_img = tk.PhotoImage(file="./imagens/down.png")

        self.move_down_btn = ttk.Button(frame_botoes, width=20, text="Mover para baixo", image=self.move_down_img,
                                        compound=LEFT, command=self.move_down_ctrl)
        self.move_down_btn.state(['disabled'])
        self.move_down_btn.pack(side=TOP, pady=2)

        menu_bar = tk.Menu(main_frame)

        projeto_menu = tk.Menu(menu_bar, tearoff=0)
        projeto_menu.add_command(label="Projetos", command=self.lista_projetos)

        projeto_menu.add_command(label="Fechar Projeto", command=self.fechar_projeto_ctrl)
        projeto_menu.add_separator()
        projeto_menu.add_command(label="Sair", command=self.fechar_janela_ctrl)
        menu_bar.add_cascade(label="Projetos", menu=projeto_menu)

        ajuda_menu = tk.Menu(menu_bar, tearoff=0)
        ajuda_menu.add_command(label="Ajuda", command=self.sobre_ctrl)

        ajuda_menu.add_command(label="Licença", command=self.sobre_ctrl)
        ajuda_menu.add_separator()
        ajuda_menu.add_command(label="Sobre", command=self.sobre_ctrl)
        menu_bar.add_cascade(label="Sobre", menu=ajuda_menu)

        self.parent.config(menu=menu_bar)

    def lista_projetos(self):

        self.projeto_janela = Toplevel(self.parent)

        self.projeto_janela.title("Projetos")
        self.projeto_janela.geometry("400x400")
        self.projeto_janela.protocol("WM_DELETE_WINDOW", self.fechar_projeto_janela_ctrl)

        self.projeto_janela.withdraw()
        self.projeto_janela.grid()
        self.projeto_janela.transient(self.parent)
        self.projeto_janela.grab_set()

        projeto_frame = Frame(self.projeto_janela)
        projeto_frame.pack(fill=BOTH, expand=True)

        fechar_proj_btn = ttk.Button(self.projeto_janela, text="Fechar", width=10, command=self.fechar_projeto_janela_ctrl)
        fechar_proj_btn.pack(side=RIGHT, padx=5, pady=5)

        self.excluir_proj_btn = ttk.Button(self.projeto_janela, text="Excluir", width=10, command=self.excluir_projeto_ctrl)
        self.excluir_proj_btn.pack(side=RIGHT, padx=5, pady=5)
        self.excluir_proj_btn.state(["disabled"])

        self.abrir_proj_btn = ttk.Button(self.projeto_janela, text="Abrir", width=10, command=self.abrir_projeto_ctrl)
        self.abrir_proj_btn.pack(side=RIGHT)
        self.abrir_proj_btn.state(["disabled"])

        self.alterar_proj_btn = ttk.Button(self.projeto_janela, text="Alterar", width=10, command=lambda: self.form_projeto('alterar'))
        self.alterar_proj_btn.pack(side=RIGHT)
        self.alterar_proj_btn.state(["disabled"])

        novo_proj_btn = ttk.Button(self.projeto_janela, text="Novo", width=10, command=lambda: self.form_projeto('novo'))
        novo_proj_btn.pack(side=RIGHT, padx=5, pady=5)

        grid_frame = Frame(projeto_frame, bd=10)
        grid_frame.pack(fill=BOTH, expand=YES, side=LEFT)

        self.dataCols = ('nome', 'ultima_atualizacao')
        self.projetos_grid = ttk.Treeview(grid_frame, selectmode='browse', columns=self.dataCols)
        self.projetos_grid.bind("<Double-1>", self.abrir_projeto_click)
        self.projetos_grid.bind("<Button-1>", self.habilita_btn_proj)

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

        centro_(self.projeto_janela)

        self.lista_projetos_ctrl()

        self.projeto_janela.deiconify()
        self.parent.wait_window(self.projeto_janela)

    def lista_projetos_ctrl(self):

        self.projetos_grid.delete(*self.projetos_grid.get_children())

        dados = ProjetosDb(self.db).listar_projetos()
        for row in dados:
            formato = '{%d/%m/%Y %H:%M:%S}'

            #datetime.strptime("21/11/06 16:30", "%d/%m/%y %H:%M")
            self.projetos_grid.insert('', END, row[0], values=(row[1], row[12]))

    def form_projeto(self, acao):

        self.form_projeto_janela = Toplevel(self.parent)
        self.form_projeto_janela.resizable(0, 0)

        if acao == 'novo':
            self.form_projeto_janela.title("Novo Projeto")
        else:
            self.form_projeto_janela.title("Alterar Projeto")

        self.form_projeto_janela.geometry("700x400")
        self.form_projeto_janela.protocol("WM_DELETE_WINDOW", self.fechar_form_projeto_ctrl)

        self.form_projeto_janela.withdraw()
        self.form_projeto_janela.grid()
        self.form_projeto_janela.transient(self.parent)
        self.form_projeto_janela.grab_set()

        projeto_frame = Frame(self.form_projeto_janela)
        projeto_frame.pack(fill=BOTH, expand=True)

        cancelar_btn = ttk.Button(self.form_projeto_janela, text="Cancelar", width=10, command=self.fechar_form_projeto_ctrl)
        cancelar_btn.pack(side=RIGHT, padx=5, pady=5)

        ok_btn = ttk.Button(self.form_projeto_janela, text="Salvar", width=10, command=lambda: self.form_projeto_ctrl(acao))
        ok_btn.pack(side=RIGHT)

        info_frame = Frame(projeto_frame, bd=10)
        info_frame.pack(fill=BOTH, expand=YES, side=RIGHT)

        group_info = ttk.LabelFrame(info_frame, text="Informações", padding=(6, 6, 12, 12))
        group_info.grid(row=0, column=0, sticky='nsew')

        ttk.Label(group_info, text='Nome', width=10).grid(row=0, column=0, sticky=W)
        self.nome = ttk.Entry(group_info, width=25)
        self.nome.grid(row=0, column=1, sticky=W, pady=2)

        ttk.Label(group_info, text='Descrição', width=10).grid(row=1, column=0, sticky=W)
        self.descricao = Text(group_info, height=4, width=25)
        self.descricao.configure(font=font.Font(font=self.nome['font']))
        self.descricao.grid(row=1, column=1, sticky=W, pady=2)

        ttk.Label(group_info, text='Autor', width=10).grid(row=2, column=0, sticky=W)
        self.autor = ttk.Entry(group_info, width=25)
        self.autor.grid(row=2, column=1, sticky=W, pady=2)

        group_db = ttk.LabelFrame(info_frame, text="Acesso ao banco", padding=(6, 6, 12, 12))
        group_db.grid(row=1, column=0, sticky=NSEW)

        ttk.Label(group_db, text='Tipo', width=10).grid(row=0, column=0, sticky=W)
        self.bd_tipo_value = tk.StringVar()
        self.bd_tipo = ttk.Combobox(group_db, textvariable=self.bd_tipo_value, state="readonly", width=22)
        self.bd_tipo['values'] = ('', 'Oracle', 'Mysql', 'PostgreSql')
        self.bd_tipo.current(0)
        self.bd_tipo.grid(row=0, column=1, sticky=W, pady=2)

        ttk.Label(group_db, text='Servidor', width=10).grid(row=1, column=0, sticky=W)
        self.bd_servidor = ttk.Entry(group_db, width=25)
        self.bd_servidor.grid(row=1, column=1, sticky=W, pady=2)

        ttk.Label(group_db, text='Porta', width=10).grid(row=2, column=0, sticky=W)
        self.bd_porta = ttk.Entry(group_db, width=15)
        self.bd_porta.grid(row=2, column=1, sticky=W, pady=2)

        ttk.Label(group_db, text='Banco', width=10).grid(row=3, column=0, sticky=W)
        self.bd_banco = ttk.Entry(group_db, width=25)
        self.bd_banco.grid(row=3, column=1, sticky=W, pady=2)

        ttk.Label(group_db, text='Usuário', width=10).grid(row=4, column=0, sticky=W)
        self.bd_usuario = ttk.Entry(group_db, width=25)
        self.bd_usuario.grid(row=4, column=1, sticky=W, pady=2)

        ttk.Label(group_db, text='Senha', width=10).grid(row=5, column=0, sticky=W)
        self.bd_senha = ttk.Entry(group_db, show="*", width=25)
        self.bd_senha.grid(row=5, column=1, sticky=W, pady=2)

        centro_(self.form_projeto_janela)

        if acao == 'alterar':
            self.alterar_projeto_ctrl()

        self.form_projeto_janela.deiconify()
        self.parent.wait_window(self.form_projeto_janela)

    def alterar_projeto_ctrl(self):

        projeto_id = self.projetos_grid.selection()[0]

        projeto = ProjetosDb(self.db).localizar_projeto(projeto_id)

        self.nome.insert(0, projeto[1])
        self.descricao.insert(END, projeto[2])
        self.autor.insert(0, projeto[3])
        self.bd_tipo.current(projeto[4])
        self.bd_servidor.insert(0, projeto[5])
        self.bd_porta.insert(0, projeto[6])
        self.bd_banco.insert(0, projeto[7])
        self.bd_usuario.insert(0, projeto[9])
        self.bd_senha.insert(0, projeto[10])

    def form_projeto_ctrl(self, acao):

        arr = []
        arr.append(self.nome.get())
        arr.append(self.descricao.get("1.0", END))
        arr.append(self.autor.get())
        bd_tipo = self.bd_tipo.current()
        arr.append(bd_tipo)
        arr.append(self.bd_servidor.get())
        arr.append(self.bd_porta.get())
        arr.append(self.bd_banco.get())
        # if (bd_tipo == 1)
        #    conexao = oracle+cx_oracle://user:pass@host:port/dbname
        arr.append(self.bd_usuario.get())
        arr.append(self.bd_senha.get())
        arr.append("conexao")

        #Novo Projeto
        if acao == 'novo':

            #data de criação
            arr.append(datetime.now().isoformat(" "))

            retorno = ProjetosDb(self.db).novo_projeto(arr)
            # if retorno.isnumeric:
            #    self.projetos_grid.insert('', END, arr[0], values=(row[1], row[9]))

            self.fechar_form_projeto_ctrl()
            self.fechar_projeto_janela_ctrl()

            self.habilita_btn_abrir_proj()

        #Alterar projeto
        else:
            projeto_id = self.projetos_grid.selection()[0]

            # id do projeto
            arr.append(projeto_id)

            retorno = ProjetosDb(self.db).alterar_projeto(arr)
            # if retorno.isnumeric:
            #    self.projetos_grid.insert('', END, arr[0], values=(row[1], row[9]))

            self.lista_projetos_ctrl()

            self.fechar_form_projeto_ctrl()

    def excluir_projeto_ctrl(self):
        if deleteBox("Excluir", "Deseja realmente excluir o projeto selecionado?"):
            item = self.projetos_grid.selection()[0]
            self.projetos_grid.delete(item)

            ProjetosDb(self.db).excluirProjeto(item)

            print("Projeto excluído: ", item)

    def indica_porta_bd(self, event):
        current = self.db_tipo.current()
        if current != -1:
            if current == 'Oracle':
                self.porta

    def fechar_janela_ctrl(self):
        self.parent.destroy()

    def fechar_projeto_ctrl(self):

        for child in self.relatorios_grid.get_children():
            print(self.relatorios_grid.item(child)["values"])

        #self.projetos_grid.delete(item)

        self.iniciar_btn.state(["disabled"])
        self.cancelar_btn.state(["disabled"])
        self.novo_relatorio_btn.state(["disabled"])
        self.alterar_relatorio_btn.state(["disabled"])
        self.excluir_relatorio_btn.state(["disabled"])
        self.move_up_btn.state(["disabled"])
        self.move_down_btn.state(["disabled"])

        #Limpar a lista de relatórios
        self.relatorios_grid.delete(*self.relatorios_grid.get_children())

    def fechar_projeto_janela_ctrl(self):
        self.projeto_janela.destroy()

    def fechar_form_projeto_ctrl(self):
        self.form_projeto_janela.destroy()

    def abrir_projeto_ctrl(self):

        projeto_id = self.projetos_grid.selection()[0]

        self.projeto_aberto = projeto_id

        relatorios_lista = RelatoriosDb(self.db).listar_relatorios(projeto_id)
        #print(relatorios_lista)

        self.lista_relatorios_ctrl(relatorios_lista)

        self.fechar_projeto_janela_ctrl()

        self.habilita_btn_abrir_proj()

    def abrir_projeto_click(self, event):

        projeto_id = self.projetos_grid.selection()[0]

        relatorios_lista = RelatoriosDb(self.db).listar_relatorios(projeto_id)
        #print(relatorios_lista)

        self.lista_relatorios_ctrl(relatorios_lista)

        self.fechar_projeto_janela_ctrl()

        self.habilita_btn_abrir_proj()

    def habilita_btn_proj(self, event):
        self.alterar_proj_btn.state(["!disabled"])
        self.abrir_proj_btn.state(["!disabled"])
        self.excluir_proj_btn.state(["!disabled"])

    def habilita_btn_abrir_proj(self):
        self.novo_relatorio_btn.state(["!disabled"])
        self.iniciar_btn.state(["!disabled"])

    def iniciar_ctrl(self):

        self.lista_projetos_btn.state(["disabled"])
        self.sair_btn.state(["disabled"])

        self.novo_relatorio_btn.state(["disabled"])
        self.alterar_relatorio_btn.state(["disabled"])
        self.excluir_relatorio_btn.state(["disabled"])
        self.move_up_btn.state(["disabled"])
        self.move_down_btn.state(["disabled"])

        self.iniciar_btn.state(["disabled"])
        self.cancelar_btn.state(["!disabled"])

    def cancelar_ctrl(self):

        self.lista_projetos_btn.state(["!disabled"])
        self.sair_btn.state(["!disabled"])

        self.novo_relatorio_btn.state(["!disabled"])

        self.iniciar_btn.state(["!disabled"])
        self.cancelar_btn.state(["disabled"])

    def novo_relatorio(self):

        print('Projeto aberto:', self.projeto_aberto)

        self.novo_relatorio_janela = Toplevel()
        self.novo_relatorio_janela.resizable(0, 0)

        self.novo_relatorio_janela.title("Novo Relatório")
        self.novo_relatorio_janela.geometry("500x300")
        self.novo_relatorio_janela.protocol("WM_DELETE_WINDOW", self.fechar_novo_relatorio_ctrl)

        self.novo_relatorio_janela.withdraw()
        self.novo_relatorio_janela.grid()
        self.novo_relatorio_janela.transient(self.parent)
        self.novo_relatorio_janela.grab_set()

        relatorio_frame = Frame(self.novo_relatorio_janela, relief=RAISED, borderwidth=1)
        relatorio_frame.pack(fill=BOTH, expand=True)

        relatorio_tab = ttk.Notebook(relatorio_frame)
        relatorio_tab.pack(fill=BOTH, expand=True)

        cancelar_btn = ttk.Button(self.novo_relatorio_janela, text="Cancelar", width=10, command=self.fechar_novo_relatorio_ctrl)
        cancelar_btn.pack(side=RIGHT, padx=5, pady=5)

        ok_btn = ttk.Button(self.novo_relatorio_janela, text="Incluir", width=10, command=self.salvar_relat_ctrl)
        ok_btn.pack(side=RIGHT)

        info_frame = Frame(relatorio_tab, bd=10)
        info_frame.pack(fill=BOTH, expand=YES, side=RIGHT)

        group_info = ttk.LabelFrame(info_frame, text="Informações", padding=(6, 6, 12, 12))
        group_info.grid(row=0, column=0, sticky='nsew')

        ttk.Label(group_info, text='Nome', width=10).grid(row=0, column=0, sticky=W)
        self.nome_relatorio = ttk.Entry(group_info, width=25)
        self.nome_relatorio.grid(row=0, column=1, sticky=W, pady=2)

        ttk.Label(group_info, text='Descrição', width=10).grid(row=1, column=0, sticky=W)
        self.descricao_relatorio = Text(group_info, height=4, width=25)
        self.descricao_relatorio.configure(font=font.Font(font=self.nome_relatorio['font']))
        self.descricao_relatorio.grid(row=1, column=1, sticky=W, pady=2)

        ttk.Label(group_info, text='Autor', width=10).grid(row=2, column=0, sticky=W)
        self.autor_relatorio = ttk.Entry(group_info, width=25)
        self.autor_relatorio.grid(row=2, column=1, sticky=W, pady=2)

        consulta_frame = ttk.Frame(relatorio_tab)

        sql_frame = ttk.LabelFrame(consulta_frame, text="Sql", padding=(6, 6, 12, 12))
        sql_frame.grid(row=0, column=0, sticky=NSEW)

        self.query = Text(sql_frame, height=4, width=25)
        self.query.configure(font=font.Font(font=self.nome_relatorio['font']))
        self.query.grid(row=0, column=0, sticky=W, pady=2)

        colunas_frame = ttk.LabelFrame(consulta_frame, text="Colunas", padding=(6, 6, 12, 12))
        colunas_frame.grid(row=0, column=0, sticky=NSEW)

        self.dataCols = ('nome', 'complemento')
        self.colunas_grid = ttk.Treeview(colunas_frame, selectmode='browse', columns=self.dataCols)
        self.colunas_grid.bind("<Double-1>", self.abrir_projeto_click)
        self.colunas_grid.bind("<Button-1>", self.habilita_btn_proj)

        scroll_y = ttk.Scrollbar(colunas_frame, orient=VERTICAL, command=self.colunas_grid.yview)
        scroll_x = ttk.Scrollbar(colunas_frame, orient=HORIZONTAL, command=self.colunas_grid.xview)
        self.colunas_grid['yscroll'] = scroll_y.set
        self.colunas_grid['xscroll'] = scroll_x.set

        scroll_y.configure(command=self.colunas_grid.yview)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.configure(command=self.colunas_grid.xview)
        scroll_x.pack(side=BOTTOM, fill=X)

        # setup column headings
        self.colunas_grid['show'] = 'headings'
        self.colunas_grid.heading('nome', text='Nome', anchor=W)
        self.colunas_grid.column('nome', stretch=0, width=200)
        self.colunas_grid.heading('complemento', text='Última Atualização', anchor=W)

        self.colunas_grid.pack(fill=BOTH, side=LEFT, expand=True)

        frame_botoes = Frame(relatorio_tab, width=200, padx=20, pady=30)
        frame_botoes.pack(side=RIGHT, fill=Y)

        self.novo_relatorio_img = tk.PhotoImage(file="./imagens/incluir.png")

        self.novo_relatorio_btn = ttk.Button(frame_botoes, width=20, text="Incluir", image=self.novo_relatorio_img,
                                             compound=LEFT, command=self.form_relatorio)
        self.novo_relatorio_btn.state(['disabled'])
        self.novo_relatorio_btn.pack(side=TOP, pady=2)

        self.alterar_relatorio_img = tk.PhotoImage(file="./imagens/alterar.png")

        self.alterar_relatorio_btn = ttk.Button(frame_botoes, width=20, text="Alterar",
                                                image=self.alterar_relatorio_img,
                                                compound=LEFT, command=self.alterar_relatorio)
        self.alterar_relatorio_btn.state(['disabled'])
        self.alterar_relatorio_btn.pack(side=TOP, pady=2)

        f3 = ttk.Frame(relatorio_tab)  # second page

        relatorio_tab.add(info_frame, text='Informações')
        relatorio_tab.add(consulta_frame, text='Consulta')
        relatorio_tab.add(f3, text='Configuração')

        centro_(self.novo_relatorio_janela)

        self.novo_relatorio_janela.deiconify()
        self.parent.wait_window(self.novo_relatorio_janela)

    def alterar_relatorio(self):

        self.alterar_relatorio_janela = Toplevel()
        self.alterar_relatorio_janela.resizable(0, 0)

        self.alterar_relatorio_janela.title("Alterar Relatório")
        self.alterar_relatorio_janela.geometry("500x300")
        self.alterar_relatorio_janela.protocol("WM_DELETE_WINDOW", self.fechar_alterar_relatorio_ctrl)

        self.alterar_relatorio_janela.withdraw()
        self.alterar_relatorio_janela.grid()
        self.alterar_relatorio_janela.transient(self.parent)
        self.alterar_relatorio_janela.grab_set()

        relatorio_frame = Frame(self.alterar_relatorio_janela, relief=RAISED, borderwidth=1)
        relatorio_frame.pack(fill=BOTH, expand=True)

        self.relatorio_tab = ttk.Notebook(relatorio_frame)
        self.relatorio_tab.pack(fill=BOTH, expand=True)

        cancelar_btn = ttk.Button(self.alterar_relatorio_janela, text="Cancelar", width=10, command=self.fechar_alterar_relatorio_ctrl)
        cancelar_btn.pack(side=RIGHT, padx=5, pady=5)

        ok_btn = ttk.Button(self.alterar_relatorio_janela, text="Incluir", width=10, command=self.salvar_relat_ctrl)
        ok_btn.pack(side=RIGHT)

        f1 = ttk.Frame(self.relatorio_tab)  # first page, which would get widgets gridded into it
        f1.pack(side=BOTTOM, expand=YES)

        f2 = ttk.Frame(self.relatorio_tab)  # second page
        f3 = ttk.Frame(self.relatorio_tab)  # second page
        self.relatorio_tab.add(f1, text='Informações')
        self.relatorio_tab.add(f2, text='Consulta')
        self.relatorio_tab.add(f3, text='Configuração')

        centro_(self.alterar_relatorio_janela)

        self.alterar_relatorio_janela.deiconify()
        self.parent.wait_window(self.alterar_relatorio_janela)

    def lista_relatorios_ctrl(self, relatorios):

        self.relatorios = relatorios

        for row in self.relatorios:
            self.relatorios_grid.insert("", END, row[0], values=(row[2], row[8]))

    def fechar_novo_relatorio_ctrl(self):
        self.novo_relatorio_janela.destroy()

    def fechar_alterar_relatorio_ctrl(self):
        self.alterar_relatorio_janela.destroy()

    def salvar_relat_ctrl(self):
        self.projeto_janela.destroy()

    def habilita_btn_relat(self, event):
        self.alterar_relatorio_btn.state(["!disabled"])
        self.excluir_relatorio_btn.state(["!disabled"])
        self.move_up_btn.state(["!disabled"])
        self.move_down_btn.state(["!disabled"])

    def novo_relatorio_ctrl(self):
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

        self.fechar_novo_relatorio_ctrl()

    def alterar_relatorio_ctrl(self):
        item = self.relatorios_grid.selection()[0]

        print("you clicked on", self.relatorios_grid.item(item, "text"))

    def alterar_relatorio_click(self):
        item = self.relatorios_grid.selection()[0]

        print("you clicked on", self.relatorios_grid.item(item, "text"))

    def excluir_relatorio_ctrl(self, db):

        if deleteBox("Excluir", "Deseja realmente excluir o relatório selecionado?"):
            relatorio_id = self.relatorios_grid.selection()
            self.relatorios_grid.delete(relatorio_id)

            RelatoriosDb(self.db).excluirRelatorio(relatorio_id)

            print("Projeto excluído: ", relatorio_id)

    def move_up_ctrl(self):
        leaves = self.relatorios_grid.selection()
        print("item: ", leaves)
        for i in leaves:
            self.relatorios_grid.move(i, self.relatorios_grid.parent(i), self.relatorios_grid.index(i) - 1)

    def move_down_ctrl(self):
        leaves = self.relatorios_grid.selection()
        for i in leaves:
            self.relatorios_grid.move(i, self.relatorios_grid.parent(i), self.relatorios_grid.index(i) + 1)

    def sobre_ctrl(self):
        app = Sobre(self.parent)


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
            self.conn = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES)
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

    def rollback_db(self):
        if self.conn:
            self.conn.rollback()

    def close_db(self):
        if self.conn:
            self.conn.close()
            print("Conexão fechada.")


class ProjetosDb(object):
    ''' A classe ProjetosDb representa um projeto no banco de dados. '''

    def __init__(self, db):
        self.db = db

    def novo_projeto(self, dados):
        try:
            self.db.cursor.execute("""
            INSERT INTO projetos (nome, descricao, autor, bd_tipo, bd_servidor, bd_porta, bd, bd_usuario,
            bd_senha, bd_str_conexao, criado_em)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (dados[0], dados[1], dados[2], dados[3], dados[4], dados[5], dados[6], dados[7], dados[8],
                  dados[9], dados[10],))
            # gravando no bd
            self.db.commit_db()
            print("Um registro inserido com sucesso.")
        # Catch the exception
        except Exception as e:
            print(e)
            # Roll back any change if something goes wrong
            self.db.rollback_db()
            return False

    def listar_projetos(self):
        sql = 'SELECT * FROM projetos ORDER BY nome'
        r = self.db.cursor.execute(sql)
        return r.fetchall()

    def localizar_projeto(self, id):
        r = self.db.cursor.execute(
            'SELECT * FROM projetos WHERE id = ?', (id,))
        return r.fetchone()

    def alterar_projeto(self, dados):
        try:
            self.db.cursor.execute("""
            UPDATE projetos
               SET nome = ?,
                   descricao = ?,
                   autor = ?,
                   bd_tipo = ?,
                   bd = ?,
                   bd_servidor = ?,
                   bd_porta = ?,
                   bd_usuario = ?,
                   bd_senha = ?,
                   bd_str_conexao = ?
                WHERE id = ?
            """, (dados[0], dados[1], dados[2], dados[3], dados[4], dados[5], dados[6], dados[7], dados[8],
                  dados[9], dados[10],))
            # gravando no bd
            self.db.commit_db()
            print("Dados atualizados com sucesso.")
        except Exception as e:
            print(e)
            self.db.rollback_db()
            #raise e

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
        sql = 'SELECT * FROM relatorios WHERE projeto_id = ? ORDER BY descricao'
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
