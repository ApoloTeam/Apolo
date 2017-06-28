class D():
    def foo(self):
        print("class D")

class B(D):
    pass

class C(D):
    def foo(self):
        print("class C")

class A(B, C):
    pass

f = A()
f.foo()