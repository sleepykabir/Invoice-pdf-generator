from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from datetime import date
from num2words import num2words
import os

buyers = {
    "X": {
        "name": "PLQ SHIPPING.",
        "address": [
            "NARAYANGANJ",
            "BANGLADESH"
        ]
    },
    "Y": {
        "name": "ABC SHIPPING LTD.",
        "address": [
            "PORT AREA",
            "CHATTOGRAM"
        ]
    },
    "Z": {
        "name": "XYZ MARINE SERVICES",
        "address": [
            "NARAYANGANJ",
            "BANGLADESH"
        ]
    }
}


# USER INPUT
buyer_key = input("Select buyer (X / Y / Z): ").upper()
pos_dtc = input("Enter POS/DTC No (example: 06/26): ").strip()
liters = float(input("Enter diesel quantity (liters): "))
rate = float(input("Enter rate per liter (BDT): "))

# VALIDATION
if buyer_key not in buyers:
    raise ValueError("Invalid buyer selection. Choose X, Y, or Z.")

# CREATE SAVE FOLDER
os.makedirs("invoices", exist_ok=True)

# CREATE PDF FILE
file_name = f"invoices/POS-DTC_{pos_dtc.replace('/', '-')}_{date.today()}.pdf"
c = canvas.Canvas(file_name, pagesize=A4)


# ================================

buyer = buyers[buyer_key]
total = liters * rate
amount_words = num2words(int(total), lang='en').upper()


width, height = A4
y = height - 2 * cm

# ===== COMPANY HEADER (FIXED) =====
c.setFont("Helvetica-Bold", 18)
c.drawCentredString(width / 2, y, "XYZ OIL SUPPLIERS")

c.setFont("Helvetica", 10)
y -= 0.6 * cm
c.drawCentredString(
    width / 2, y,
    "AB Street, CHATTOGRAM, BANGLADESH."
)
y -= 0.5 * cm
c.drawCentredString(
    width / 2, y,
    "H/P: +88 01******, TEL.: +88 01******, E-mail: salmankabir0068@gmail.com"
)

y -= 0.7 * cm
c.line(2 * cm, y, width - 2 * cm, y)
# POS/DTC Number
c.setFont("Helvetica", 10)
c.drawString(2 * cm, y - 0.8 * cm, f"POS/DTC :- {pos_dtc}")


# ===== INVOICE TITLE =====
y -= 1 * cm
c.setFont("Helvetica-Bold", 14)
c.drawCentredString(width / 2, y, "INVOICE")

# Date
c.setFont("Helvetica", 10)
c.drawRightString(width - 2 * cm, y - 1 * cm,
                  f"Date : {date.today().strftime('%d/%m/%Y')}")

# ===== TO SECTION =====
y -= 2 * cm
c.setFont("Helvetica-Bold", 10)
c.drawString(2 * cm, y, "TO,")

y -= 0.5 * cm
c.setFont("Helvetica-Bold", 10)
c.drawString(2 * cm, y, buyer["name"])

c.setFont("Helvetica", 10)
for line in buyer["address"]:
    y -= 0.45 * cm
    c.drawString(2 * cm, y, line)

# ===== SUBJECT =====
y -= 0.6 * cm
c.setFont("Helvetica-Bold", 10)
c.drawString(
    2 * cm, y,
    f'SUB :- MV. "SHIP - 01" SUPPLY OF HSD/DIESEL – {int(liters)} LTRS AT CTG. O/A-B.'
)

# ===== BODY =====
y -= 1.2 * cm
text = c.beginText(2 * cm, y)
text.setFont("Helvetica", 10)

text.textLine("DEAR SIR,")
text.textLine("")
text.textLine(
    f"FORWARDED OUR BILL AGAINST SUPPLY OF {int(liters)} "
    f"({num2words(int(liters)).upper()}) LTRS HSD/DIESEL "
    f"DATED – {date.today().strftime('%d/%m/%Y')}."
)
text.textLine("")
text.textLine(f"WT :- HIGH SPEED DIESEL (HSD) = {int(liters)} LTRS")
text.textLine(f"RATE : @ H.S.D/DIESEL = BDT. {rate:.2f} PER LTR.")
text.textLine("")
text.textLine(f"( {int(liters)} x {rate:.2f} ) BDT. = {total:,.2f}")
text.textLine("")
text.textLine(f"TK.= ( {amount_words} ) ONLY.")
text.textLine("")
text.textLine("THANKING YOU,")
text.textLine("")
text.textLine("YOURS FAITHFULLY,")
text.textLine("FOR, XYZ OIL SUPPLIERS")
text.textLine("")
text.textLine("( MD. Salman KABIR )")
text.textLine("")
text.textLine("OUR BANK DETAILS :-")
text.textLine("ABC ENTERPRISE")
text.textLine("AC/NO.-0*****1, BANK ASIA LTD.")
text.textLine("SK. MUJIB ROAD, BRANCH, CHATTOGRAM.")

c.drawText(text)
c.save()

print("Invoice PDF generated successfully!")

