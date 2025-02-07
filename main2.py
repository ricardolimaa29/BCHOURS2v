import flet as ft
import datetime 
import json
import os
import time
from winotify import Notification,audio

almoço = 1
CONFIG_FILE = "config.json"
LOG_FILE = "log.json"


def carregar_configuracoes():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"nome": "", "expediente": "", "cargo": ""}


def carregar_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    return []

def salvar_logs(logs):
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)

config = carregar_configuracoes()
logs = carregar_logs()


config = carregar_configuracoes()

def main(pagina: ft.Page):
    pagina.fonts = {
        "Poppins": "fonts/Poppins-Bold.ttf",
        "Poppins2": "fonts/Poppins-Light.ttf",
        "Poppins3": "fonts/Poppins-Regular.ttf",
    }
    pagina.window.maximized = True
    pagina.title = 'Supervisor de Ponto'
    pagina.theme = ft.Theme(color_scheme_seed=ft.colors.RED)

    tabela = ft.DataTable(columns=[
        ft.DataColumn(ft.Text("Data")),
        ft.DataColumn(ft.Text("Nome")),
        ft.DataColumn(ft.Text("Cargo")),
        ft.DataColumn(ft.Text("Entrada")),
        ft.DataColumn(ft.Text("Expediente")),
        ft.DataColumn(ft.Text("Almoço")),
        ft.DataColumn(ft.Text("Saída")),
    ])

    config = carregar_configuracoes()

    def abrir_configuracoes(e):
        nome.value = str(config.get("nome", ""))
        expediente_hr.value = config.get("expediente", "")
        cargo.value = config.get("cargo","")
        pagina.overlay.append(configuracoes_modal) == configuracoes_modal
        configuracoes_modal.open = True
        pagina.update()

    def fechar_modal(e):
        configuracoes_modal.open = False
        pagina.update()

    def calcular(e):
        try:
           
            config = carregar_configuracoes()

           
            entrada_valor = entrada_hr.value.strip() if entrada_hr.value.strip() else config.get("entrada", "")
            expediente_valor = expediente_hr.value.strip() if expediente_hr.value.strip() else config.get("expediente", "")
            nome_valor = nome.value.strip() if nome.value.strip() else config.get("nome", "")
            cargo_valor = cargo.value.strip() if cargo.value.strip() else config.get("cargo", "")

          
            if not entrada_valor or not expediente_valor:
                print("Erro: Preencha todos os campos ou salve as configurações antes de calcular!")
                return

            
            ent = datetime.datetime.strptime(entrada_valor, "%H:%M")

           
            exp_parts = expediente_valor.split(":")
            if len(exp_parts) != 2 or not exp_parts[0].isdigit() or not exp_parts[1].isdigit():
                print("Erro: Formato de expediente inválido! Use H:M")
                return

            exp = datetime.timedelta(hours=int(exp_parts[0]), minutes=int(exp_parts[1]))

            
            saida = ent + exp + datetime.timedelta(hours=1) 
            saida_formatada = saida.strftime("%H:%M")

            
            data_atual = datetime.datetime.now().strftime("%d/%m/%Y")

            novo_registro = {
                "data": data_atual,
                "nome": nome_valor,
                "cargo": cargo_valor,
                "entrada": entrada_valor,
                "expediente": expediente_valor,
                "almoço": "1h",
                "saida": saida_formatada
            }

            logs.append(novo_registro)
            salvar_logs(logs)

            tabela.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(novo_registro["data"])),  
                ft.DataCell(ft.Text(novo_registro["nome"])),
                ft.DataCell(ft.Text(novo_registro["cargo"])),
                ft.DataCell(ft.Text(novo_registro["entrada"])),
                ft.DataCell(ft.Text(novo_registro["expediente"])),
                ft.DataCell(ft.Text(novo_registro["almoço"])),
                ft.DataCell(ft.Text(novo_registro["saida"])),
            ]))

            pagina.update()

        except ValueError as ve:
            print(f"Erro de valor: {ve}")
        except Exception as ex:
            print(f"Erro inesperado: {ex}")


    def salvar_configuracoes(config):
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)


    btn_config = ft.ElevatedButton(" ", on_click=abrir_configuracoes, icon=ft.icons.SETTINGS,width=55)

    titulo = ft.Text('Supervisor de Ponto-Friboi 📋',
                        font_family='Poppins',size=33)
    
    nome = ft.TextField(label='Insira o Nome',width=450,
                        text_style= ft.TextStyle(font_family='Poppins3',size=20))
    entrada_hr = ft.TextField(label="Horario de entrada:", hint_text="H:M",
                        text_style=ft.TextStyle(font_family='Poppins3',size=20),width=450)
    expediente_hr = ft.TextField(label="Seu Expediente é:", hint_text="H:M",
                                        text_style=ft.TextStyle(font_family='Poppins3',size=20),width=450)
    cargo = ft.TextField(label="Cargo:", hint_text="Analista Jr,Analista Pleno..,",
                                        text_style=ft.TextStyle(font_family='Poppins3',size=20),width=450)

    botao_gerar = ft.ElevatedButton(text='Salvar',
                                    on_click=calcular,
                                    style= ft.ButtonStyle(
                                        text_style= ft.TextStyle(font_family='Poppins2',size=20)))

    status_text = ft.Text(value="", size=16, color="Green", visible=False)

    body = ft.Container(
            content=ft.Column(
                [
                    entrada_hr,
                    botao_gerar,
                    status_text,
                    tabela
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
        )   




    navBar = ft.Container(
            content=ft.Column(
                [
                    titulo
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                
                
            ),
            alignment=ft.alignment.center,
            
        )
    def atualizar_configuracoes(e):
        config["nome"] = (nome.value)
        config["expediente"] = expediente_hr.value
        config["cargo"] = cargo.value
        salvar_configuracoes(config)
        status_text.value = "Configurações salvas com sucesso!"
        status_text.color = "green"
        status_text.visible = True
        configuracoes_modal.open = False
        pagina.update()
        time.sleep(3)
        status_text.visible = False
        pagina.update()

    configuracoes_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("⚙ CONFIGURAÇÕES ⚙",text_align='center'),
            content=ft.Column(
                [nome, expediente_hr,cargo],
                tight=True,
                width=400,
                height=300
            ),
            actions=[
                ft.TextButton("Salvar",icon='SAVE', on_click=atualizar_configuracoes,icon_color=ft.colors.GREEN),
                ft.TextButton("Fechar",icon='CLOSE', on_click=fechar_modal,icon_color=ft.colors.RED),
            ],
        )

    pagina.add(
        btn_config,
        ft.Column(
            [
                navBar,  
                ft.Container(height=300),  
                body, 
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    
ft.app(target=main)
