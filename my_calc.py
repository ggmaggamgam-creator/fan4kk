import flet as ft

def main(page: ft.Page):
    page.title = "Простой калькулятор"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 350
    page.window_height = 500

    result = ft.Text(value="0", size=40, weight=ft.FontWeight.BOLD)
    current_value = ""

    def button_clicked(e):
        nonlocal current_value
        value = e.control.text

        if value == "C":
            current_value = ""
            result.value = "0"
        elif value == "=":
            try:
                result.value = str(eval(current_value))
            except Exception:
                result.value = "Ошибка"
            current_value = ""
        else:
            if current_value == "0":
                current_value = value
            else:
                current_value += value
            result.value = current_value
        
        page.update()

    buttons = [
        ["7", "8", "9", "/"],
        ["4", "5", "6", "*"],
        ["1", "2", "3", "-"],
        ["C", "0", "=", "+"]
    ]

    grid = ft.Column(
        [
            ft.Row([result], alignment=ft.MainAxisAlignment.END),
            *[
                ft.Row(
                    [
                        ft.ElevatedButton(text=btn, on_click=button_clicked, width=70, height=70)
                        for btn in row
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
                for row in buttons
            ]
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    page.add(grid)

# Правильный запуск для современных версий Flet:
ft.app(target=main)