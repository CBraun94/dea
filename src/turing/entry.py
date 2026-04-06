from turing.web import app


def main():
    import sys

    if len(sys.argv) == 1:
        app.run()


if __name__ == '__main__':
    main()
