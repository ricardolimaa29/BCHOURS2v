import flet as ft
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from msal import ConfidentialClientApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import csv
import os


# Lista de e-mails correspondentes à equipe
emails_equipe = {
    "Felipe Augusto Ribeiro dos Santos": "felipe.augusto@friboi.com.br",
    "Decio João Greco": "decio.greco@friboi.com.br",
    "Antônio Marcos Faustino": "antonio.faustino@friboi.com.br",
}

# Lista para armazenar os registros do relatório
registros = []


def main(page: ft.Page):
    page.title = "Cálculo de Horas Trabalhadas e Relatório"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window.maximized = True

    equipe_TI = list(emails_equipe.keys())

    nomes_equipe = ft.Dropdown(
        value="Felipe Augusto Ribeiro dos Santos",
        options=[ft.dropdown.Option(nome) for nome in equipe_TI],
        focused_border_color=ft.colors.GREEN,
        width=400
        
    )
    data_hoje = datetime.now().strftime('%d/%m/%Y')
    entrada = ft.TextField(label="Hora de Entrada (HH:MM)", width=400,
                           focused_border_color=ft.colors.GREEN
                           )
    resultado_7h20 = ft.Text(value="Saída estimada (7h20min): --:--", size=16, weight="bold")
    resultado_extra = ft.Text(value="Saída máxima (+2h extras): --:--", size=16, weight="bold")
    aviso = ft.Text(value="", size=14, weight="bold", color="red")

    # Função para calcular os horários e salvar no relatório
    def calcular_horarios(e):
        global nome
        try:
            # Lê e converte o horário de entrada
            nome = nomes_equipe.value
            hora_entrada = datetime.strptime(entrada.value, "%H:%M")
            saida_7h20 = hora_entrada + timedelta(hours=8, minutes=20)
            saida_extra = saida_7h20 + timedelta(hours=2)

            # Adicionar ao relatório
            registros.append({
                "Nome": nome,
                "Entrada": entrada.value,
                "Saída Estimada (7h20)": saida_7h20.strftime('%H:%M'),
                "Saída Máxima (+2h)": saida_extra.strftime('%H:%M'),
                "Data": data_hoje
            })

            # Atualiza os resultados
            resultado_7h20.value = f"Saída estimada (7h20min): {saida_7h20.strftime('%H:%M')}"
            resultado_extra.value = f"Saída máxima (+2h extras): {saida_extra.strftime('%H:%M')}"
            aviso.value = ""

            page.update()

        except ValueError:
            aviso.value = "Erro: Insira a hora de entrada no formato HH:MM."
            page.update()

    # Função para gerar o relatório
    def gerar_relatorio(e):
        # Nome do arquivo CSV        'Entrada'
        nome_arquivo = "relatorio_horas_trabalhadas.csv"

        # Criação do arquivo CSV
        with open(nome_arquivo, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Nome", "Entrada", "Saída Estimada (7h20)", "Saída Máxima (+2h)", "Data"])
            writer.writeheader()
            writer.writerows(registros)

        aviso.value = f"Relatório '{nome_arquivo}' gerado com sucesso!"
        
        page.update()

    # Função para enviar o relatório por e-mail
    def enviar_email(e):
        try:
            # Configuração do OAuth2
            client_id = "SEU_CLIENT_ID"
            client_secret = "SEU_CLIENT_SECRET"
            tenant_id = "SEU_TENANT_ID"
            scope = ["https://outlook.office365.com/.default"]

            app = ConfidentialClientApplication(client_id, authority=f"https://login.microsoftonline.com/{tenant_id}", client_credential=client_secret)
            token = app.acquire_token_for_client(scopes=scope)

            if "access_token" not in token:
                raise Exception("Falha ao obter o token de acesso.")

            access_token = token["access_token"]
            smtp_server = "smtp.office365.com"
            smtp_port = 587

            remetente = "gestaodehorasti@outlook.com"  # Substitua pelo seu e-mail

            for nome, email in emails_equipe.items():
                if email:
                    # Criar mensagem de e-mail
                    msg = MIMEMultipart()
                    msg['From'] = remetente
                    msg['To'] = email
                    msg['Subject'] = "Relatório de Horas Trabalhadas"

                    # Corpo do e-mail
                    corpo = f"Olá {nome},\n\nSegue o relatório atualizado de horas trabalhadas.\n\nAtenciosamente,\nEquipe de Gestão de Horas"
                    msg.attach(MIMEText(corpo, 'plain'))

                    # Anexo do relatório
                    nome_arquivo = "relatorio_horas_trabalhadas.csv"
                    with open(nome_arquivo, "rb") as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f"attachment; filename={nome_arquivo}",
                        )
                        msg.attach(part)

                    # Enviar o e-mail usando OAuth2
                    with smtplib.SMTP(smtp_server, smtp_port) as server:
                        server.starttls()
                        auth_string = f"user={remetente}\1auth=Bearer {access_token}\1\1"
                        server.docmd("AUTH", "XOAUTH2 " + auth_string.encode("utf-8").strip().decode())
                        server.send_message(msg)

            aviso.value = "E-mails enviados com sucesso!"
            page.update()

        except Exception as ex:
            aviso.value = f"Erro ao enviar e-mails: {str(ex)}"
            page.update()
    # Botões adicionais
    gerar_relatorio_btn = ft.ElevatedButton(text="Gerar Relatório", on_click=gerar_relatorio,width=200,color="White",bgcolor='Blue')
    calcular_btn = ft.ElevatedButton(text="Calcular", on_click=calcular_horarios,width=200,color="White",bgcolor='Green')
    enviar_email_btn = ft.ElevatedButton(text="Enviar Relatório por E-mail", on_click=enviar_email)

    page.add(
        ft.Container(
            content=ft.Column(
                [
                    nomes_equipe,
                    entrada,
                    calcular_btn,
                    gerar_relatorio_btn,
                    resultado_7h20,
                    resultado_extra,
                    aviso,
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                
                
            ),
            alignment=ft.alignment.center,
            border=ft.border.all(2, "#002B6B")
            
        )
    )
    


# Executa o app
ft.app(target=main)