from numpy import *

#根-poly->系数-ploy1d->多项式
#系数(多项式)-roots->根

#TODO 已知多项式的系数，构造多项式
b = poly1d([1, 1]) #<class 'numpy.lib.polynomial.poly1d'>
#一个多项式的系数是1 1
print("b =\n", b)
#一个多项式y = x + 1

#TODO 已知多项式的根，构造多项式
root = [1, -1] # list
#一个多项式的根为1，-1
# a = poly1d(poly(root))
#poly()函数可以将根转换为多项式的系数
a = poly(root) # numpy.ndarray  根 变 系数
a = poly1d(a)  #系数 变 多项式
print("\na =\n", a)
#该多项式为a = [1. 0. -1.],即y = x^2 - 1

#TODO 求多项式的根
print("\nthe roots of poly :\n", roots(poly(root))) #系数变根
print(roots(a)) #多项式变根
print(a.r)

#TODO 求解多项式的系数
print("\nthe coefficients of poly:\n", a.c)

print("\neuqal?:\n", array_equal(set(root), set(roots(a))))
#判断两个根是否相等，转为set集合后，不用考虑根的先后顺序

#TODO 求解多项式某点的值
print("\nx=5, y=?:\n", a(5))
#求解函数在点x = 5的值

print("\na+b=? \n", polyadd(a, b))

