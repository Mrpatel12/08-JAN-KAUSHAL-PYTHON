import qrcode

data = "https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox"

qr = qrcode.make(data)
qr.save("qrcode.png")
