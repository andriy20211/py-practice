import os
from fpdf import FPDF
from models.product import Product


def generate_products_report(filename: str, products: list[Product]) -> str:
    pdf = FPDF()
    pdf.add_page()

    # Заголовок
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Men's Clothing Store - Inventory Report", ln=True, align="C")
    pdf.ln(10)

    # Таблиця / Список товарів
    pdf.set_font("Arial", "B", 12)
    pdf.cell(40, 10, "Product ID", border=1)
    pdf.cell(100, 10, "Product Name", border=1)
    pdf.cell(40, 10, "Price ($)", border=1, ln=True)

    pdf.set_font("Arial", "", 12)
    for prod in products:
        # Оскільки стандартний шрифт Arial не підтримує кирилицю,
        # очищаємо або конвертуємо назву в латиницю (ascii трансліт), якщо необхідно.
        prod_name = prod.name.encode('ascii', 'ignore').decode('ascii') or f"Product #{prod.id}"

        pdf.cell(40, 10, str(prod.id), border=1)
        pdf.cell(100, 10, prod_name, border=1)
        pdf.cell(40, 10, f"{prod.price:.2f}", border=1, ln=True)

    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    filepath = f"./{upload_dir}/{filename}"
    pdf.output(filepath)

    return filepath