import pandas

data = {
      'id':[1,2,3,4,5],
      'Name':['kaushal','raj','sachin','virat','rohit'],
      'Age':[25,35,29,51,38]
}

dt = pandas.DataFrame(data)
print(dt)
