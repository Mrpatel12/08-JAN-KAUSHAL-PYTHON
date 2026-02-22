import qrcode

upi_id = "kaushal10804@oksbi"
Bank_name = "Bank of Baroda"
name = "Kapupara Dayaben Laxmanbhai"
amount = ""
currency = "INR"

upi_link = f"upi://pay?pa={upi_id}&pn={name}&am={amount}&currency={currency}"
qr = qrcode.make(upi_link)
qr.save("bank_qr.png")

print("Your qrcode is generated")

