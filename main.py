import sqlite3
import matplotlib.pyplot as plt
import csv

# Professional Context Manager
def run_inventory_system():
    try:
        with sqlite3.connect('tech_inventory.db') as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Create Table
            cursor.execute('''CREATE TABLE IF NOT EXISTS assets 
                            (id INTEGER PRIMARY KEY, item TEXT, category TEXT, price REAL)''')

            # Clean and Insert Data (Mock Data)
            assets_to_add = [
                ('samsung book e30', 'Laptop', 2500.00),
                ('hy320 projector', 'Peripherals', 800.00),
                ('chromecast', 'Peripherals', 250.00),
                ('ventisol cooler', 'Office', 350.00)
            ]
            
            # Using placeholders for security (SC-900 best practice)
            for item, cat, price in assets_to_add:
                cursor.execute("INSERT INTO assets (item, category, price) VALUES (?, ?, ?)", 
                               (item.title(), cat, price))
            
            # SQL Analysis: Summing prices AS 'total_value'
            cursor.execute("SELECT category, SUM(price) AS total_value FROM assets GROUP BY category")
            report_data = cursor.fetchall()

            # Visualization with Matplotlib
            categories = [row['category'] for row in report_data]
            values = [row['total_value'] for row in report_data]

            plt.bar(categories, values, color='teal')
            plt.title('Inventory Value by Category')
            plt.ylabel('Total Value (R$)')
            plt.savefig('inventory_report.png')
            
            print("✅ Database ready and report generated as 'inventory_report.png'!")

    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")

if __name__ == "__main__":
    run_inventory_system()