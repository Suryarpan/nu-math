from math import comb
from typing import Optional


class UpperConstraint[T: (int, float)]:
    p: Optional[T] = None
    q: Optional[T] = None

    @classmethod
    def ups_factory(cls, p: T, q: T):
        cls.p = p
        cls.q = q
        return cls

    def __init__(self, n) -> None:
        if self.p >= n or n >= self.q:
            raise ValueError(f"{n=} needs to be in the range ({self.p}, {self.q})")
        self.n = n

    def __add__(self, other):
        if not isinstance(other, UpperConstraint):
            raise TypeError(f"unsupported type {type(other)}")
        if other.p != self.p or other.q != self.q:
            raise TypeError(f"{other=} belongs to different set")
        s_n = self.n - self.p
        o_n = other.n - self.p
        q_p = self.q - self.p
        ups = self.ups_factory(self.p, self.q)
        return ups(self.p + ((s_n + o_n) / (1 + s_n * o_n / (q_p * q_p))))

    def __mul__(self, other):
        if not isinstance(other, int):
            raise TypeError(f"unsupported type {type(other)}")
        nume_limit = (other - 1) // 2
        deno_limit = other // 2
        s_n = self.n - self.p
        q_p = self.q - self.p
        nume = sum(
            s_n ** (2 * j + 1) * comb(other, 2 * j + 1) / q_p ** (2 * j)
            for j in range(nume_limit + 1)
        )
        deno = sum(
            s_n ** (2 * j) * comb(other, 2 * j) / q_p ** (2 * j)
            for j in range(deno_limit + 1)
        )
        ups = self.ups_factory(self.p, self.q)
        return ups((nume / deno) + self.p)

    def __str__(self) -> str:
        return f"{self.n}:({self.p},{self.q})"


def main():
    ups = UpperConstraint.ups_factory(3, 20)
    a = ups(10)
    b = ups(15)
    c = a + b + b + a + a + b + a + b + b + a
    d = a * 5 + b * 5
    print(c)
    print(d)


if __name__ == "__main__":
    main()
