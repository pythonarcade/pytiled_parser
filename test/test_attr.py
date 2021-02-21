import attr


@attr.s(auto_attribs=True, kw_only=True)
class Foo:
    x: int
    y: int

    a: int = 5


@attr.s(auto_attribs=True, kw_only=True)
class Bar(Foo):
    z: int


foo = Foo(x=1, y=2)

bar = Bar(x=1, y=2, z=3)

print(foo)
print(bar)
