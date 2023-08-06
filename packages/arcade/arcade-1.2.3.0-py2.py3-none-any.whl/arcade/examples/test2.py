def draw(draw_func):
    def f():
        print("A")
        draw_func()
        print("B")
    return f

@draw
def draw_func():
    print("Ok")

def main():
    draw_func()

main()

