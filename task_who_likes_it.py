def likes(names):
    d = {
        0: "no one likes this",
        1: "{0} likes this",
        2: "{0} and {1} like this",
        3: "{0}, {1} and {2} like this"
    }
    n = len(names)
    template = d.get(n, "{}, {} and {} others like this")
    args = names if n in d else (names[0], names[1], n - 2)
    return template.format(*args)

print(likes(["x", "y", "x", "i", "z"]))
print(likes([]))



def likes(names):
    d = {
        0: "no one likes this",
        1: "{0} likes this",
        2: "{0} and {1} like this",
        3: "{0}, {1} and {2} like this"
    }
    n = len(names)
    return d[n].format(*names) if n in d else (
        "{0}, {1} and {2} others like this".format(names[0], names[1], n - 2))

print(likes(["x", "y", "x"]))


def likes(names):

    d = {0: lambda: f"no one likes this",
         1: lambda: f"{names[0]} likes this",
         2: lambda: f"{names[0]} and {names[1]} like this",
         3: lambda: f"{names[0]}, {names[1]} and {names[2]} like this",
         }

    return d.get(len(names), lambda: f"{names[0]}, {names[1]} and {len(names) - 2} others like this")()

print(likes(["x", "y"]))

def likes(names):

    d = {0: lambda: f"no one likes this",
         1: lambda: f"{names[0]} likes this",
         2: lambda: f"{names[0]} and {names[1]} like this",
         3: lambda: f"{names[0]}, {names[1]} and {names[2]} like this",
         }

    return d.get(len(names), lambda: f"{names[0]}, {names[1]} and {len(names) - 2} others like this")()

print(likes(["x"]))


def likes(names):

    d = {0: lambda: f"no one likes this",
         1: lambda: f"{names[0]} likes this",
         2: lambda: f"{names[0]} and {names[1]} like this",
         3: lambda: f"{names[0]}, {names[1]} and {names[2]} like this",
         }

    return d.get(len(names), lambda: f"{names[0]}, {names[1]} and {len(names) - 2} others like this")()

print(likes([]))

