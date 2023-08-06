import click


@click.command()
@click.option('-n', default=1)
def f(n):
    print('func f of temp_test2 called ' * n)


if __name__ == '__main__':
    f()
