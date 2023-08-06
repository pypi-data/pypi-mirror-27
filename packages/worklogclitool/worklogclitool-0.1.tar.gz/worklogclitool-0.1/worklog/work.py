import click
import datetime


def temp_log(time):
    try:
        with open('./templog.log', "w") as f:
            f.write(time)
        f.close()
    except:
        print('file error')


def read_temp_log():
    try:
        timelog = ''
        with open('./templog.log', "r") as f:
            if f is not '':
                timelog = f.readline().splitlines()
        f.close()
        return timelog
    except:
        print('file error')


def work_log(time, date):
    try:
        with open('./worklog.log', "a+") as f:
            f.write(date)
            f.write(time+'\n')
        f.close()
    except:
        print('file error')


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('Version 1.0')
    ctx.exit()

# TODO check current date so you cant log old times
def start_timer(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    temp_log(start_time)
    click.echo('Timer starting: '+datetime.datetime.now().strftime('%T'))
    ctx.exit()


def stop_timer(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    try:
        start_time = read_temp_log()
        stop_time = datetime.datetime.now()
        start_time_format = datetime.datetime.strptime(start_time[0], '%Y-%m-%d %H:%M:%S.%f')
        time_diff = stop_time - start_time_format
        temp_log('')
        date = datetime.datetime.now().strftime('%d-%m-%Y - ')
        work_log(str(time_diff)[:-7], date)
        click.echo('Timer stoped')
        click.echo('Time loged:')
        click.echo(str(time_diff)[:-7])
    except:
        print('Timer is not started')
    ctx.exit()


def add_time(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    user_input = click.prompt('Input format: D-M-Y--H:M:S')
    date = user_input[:10] + ' - '
    time = user_input[12:]
    work_log(time, date)
    click.echo('Time logged: %s%s' % (date, time))
    ctx.exit()


def show_timer(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    try:
        start_time = read_temp_log()
        stop_time = datetime.datetime.now()
        start_time_format = datetime.datetime.strptime(start_time[0], '%Y-%m-%d %H:%M:%S.%f')
        time_diff = stop_time - start_time_format
        click.echo('Current worktime:')
        click.echo(time_diff)
    except:
        print('Timer is not started')
    ctx.exit()


@click.command()
@click.option('--version', '-v', multiple=True, is_flag=True,
              callback=print_version,
              expose_value=False, is_eager=True,
              help='Show the version')
@click.option('--start', '-sta', multiple=True, is_flag=True,
              callback=start_timer,
              expose_value=False, is_eager=True,
              help='Start the timer')
@click.option('--stop', '-sto', multiple=True, is_flag=True,
              callback=stop_timer,
              expose_value=False, is_eager=True,
              help='Stop timer')
@click.option('--add', '-a', multiple=True, is_flag=True,
              callback=add_time, #prompt='Day-month-year - hours:minutes:seconds',
              expose_value=False, is_eager=True,
              help='Add time to a specific day \n "D-M-Y--H:M:S"')
@click.option('--show', '-sh', multiple=True, is_flag=True,
              callback=show_timer,
              expose_value=False, is_eager=True,
              help='Show how much you have worked for now')
def work():
    click.echo('Work is a cli tool to log your work. Try work --help to get started.')
