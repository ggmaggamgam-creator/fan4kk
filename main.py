import ast
import operator

import flet as ft


_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def calculate(expression: str):
    tree = ast.parse(expression, mode="eval")

    def evaluate(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
            left = evaluate(node.left)
            right = evaluate(node.right)
            return _OPERATORS[type(node.op)](left, right)

        if isinstance(node, ast.UnaryOp) and type(node.op) in _OPERATORS:
            return _OPERATORS[type(node.op)](evaluate(node.operand))

        raise ValueError("Недопустимое выражение")

    return evaluate(tree.body)


def main(page: ft.Page):
    page.title = "Крутой калькулятор"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 320
    page.window_height = 450
    page.window_resizable = False
    page.theme_mode = ft.ThemeMode.DARK

    result_var = ft.TextField(
        value="0",
        text_align=ft.TextAlign.RIGHT,
        text_size=28,
        read_only=True,
        border_radius=10,
        bgcolor=ft.colors.GREY_900,
    )

    def on_button_click(e):
        char = e.control.text
        current_text = result_var.value or "0"

        if char == "C":
            result_var.value = "0"
        elif char == "=":
            try:
                result = calculate(current_text)
                if isinstance(result, float):
                    if not result.is_integer():
                        result = round(result, 10)
                    else:
                        result = int(result)
                result_var.value = str(result)
            except (SyntaxError, ValueError, TypeError, ZeroDivisionError, OverflowError):
                result_var.value = "Ошибка"
        elif current_text == "Ошибка" or current_text == "0":
            result_var.value = char
        else:
            result_var.value = current_text + char

        page.update()

    buttons = [
        "C", "(", ")", "/",
        "7", "8", "9", "*",
        "4", "5", "6", "-",
        "1", "2", "3", "+",
        "0", ".", "=",
    ]

    grid = ft.GridView(
        expand=True,
        runs_count=4,
        max_extent=70,
        child_aspect_ratio=1.0,
        spacing=5,
        run_spacing=5,
    )

    for text in buttons:
        grid.controls.append(
            ft.ElevatedButton(
                text=text,
                on_click=on_button_click,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=8),
                ),
            )
        )

    page.add(
        ft.Container(content=result_var, padding=10, width=300),
        ft.Container(content=grid, padding=10, width=300, height=320),
    )


ft.app(target=main)
