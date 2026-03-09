
import flet as ft
import requests

def main(page: ft.Page):
    page.title = "MarketVision AI"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 450
    page.window_height = 800
    page.padding = 25

    # Элементы интерфейса
    articul_input = ft.TextField(label="Артикул WB", border_color="purple", value="211232454")
    result_card = ft.Column(visible=False)
    name_text = ft.Text(size=18, weight=ft.FontWeight.BOLD)
    price_text = ft.Text(size=16, color=ft.Colors.GREEN_400)
    brand_text = ft.Text(size=14, italic=True, color=ft.Colors.GREY_400)
    ai_advice = ft.Text("Лама анализирует...", color=ft.Colors.BLUE_200)
    loading = ft.ProgressBar(visible=False, color="purple")

    def get_wb_data(e):
        art = articul_input.value
        if not art or not art.isdigit():
            articul_input.error_text = "Введите цифры!"
            page.update()
            return
        
        loading.visible = True
        result_card.visible = False
        page.update()

        headers = {"User-Agent": "Mozilla/5.0"}
        url = f"https://wb.ru{art}"
        
        try:
            r = requests.get(url, headers=headers, timeout=10)
            data = r.json().get('data', {}).get('products', [])
            
            if not data:
                articul_input.error_text = "Товар не найден"
            else:
                item = data[0]
                name_text.value = item.get('name', 'Без имени')
                brand_text.value = f"Бренд: {item.get('brand', 'N/A')}"
                price = item.get('salePriceU', 0) // 100
                price_text.value = f"Цена: {price} ₽"
                
                result_card.visible = True
                
                # Запрос к Ламе
                prompt = f"Товар: {name_text.value}. Цена: {price}р. Дай краткий совет селлеру."
                try:
                    res = requests.post("http://localhost:11434/api/generate", 
                                        json={"model": "tinyllama", "prompt": prompt, "stream": False}, timeout=15)
                    ai_advice.value = res.json().get('response', '...')
                except:
                    ai_advice.value = "🤖 Лама спит (запусти Ollama)"
        except:
            articul_input.error_text = "Ошибка связи"
        
        loading.visible = False
        page.update()

    page.add(
        ft.Text("📦 OpenClaw Sentinel", size=24, weight=ft.FontWeight.BOLD, color="purple200"),
        articul_input,
        ft.FilledButton("Анализировать", on_click=get_wb_data, style=ft.ButtonStyle(bgcolor="purple")),
        loading,
        ft.Divider(height=20),
        result_card := ft.Column([
            name_text, brand_text, price_text,
            ft.Container(content=ai_advice, bgcolor=ft.Colors.WHITE10, padding=15, border_radius=10)
        ], visible=False)
    )

if __name__ == "__main__":
    ft.run(main)


           
