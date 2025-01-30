import flet as ft
import datetime 




def main(pagina: ft.Page):
    pagina.fonts = {
        "Poppins": "fonts/Poppins-Bold.ttf",
        "Poppins2": "fonts/Poppins-Light.ttf",
        "Poppins3": "fonts/Poppins-Regular.ttf",
    }
    pagina.window.maximized = True
    pagina.title = 'BCHOURS'
    pagina.theme = ft.Theme(color_scheme_seed=ft.colors.GREEN)
    titulo = ft.Text('Sistema de Ponto-Friboi 📋',
                     font_family='Poppins',size=33)
    
    nome = ft.TextField(label='Insira o Nome',width=450,
                        text_style= ft.TextStyle(font_family='Poppins3',size=20))
    
    botao_gerar = ft.ElevatedButton(text='Gerar',color='white',
                                    style= ft.ButtonStyle(
                                        text_style= ft.TextStyle(font_family='Poppins2',size=20)))
    

    body = ft.Container(
            content=ft.Column(
                [
                    nome,
                    botao_gerar
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

    pagina.add(
        ft.Column(
            [
                navBar,  # Título no topo
                ft.Container(height=200),  # Espaço vazio para empurrar o body
                body,  # Body centralizado na área desejada
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    
ft.app(target=main)
