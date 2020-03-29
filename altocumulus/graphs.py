from flask import Blueprint, make_response

graphs = Blueprint('graphs', __name__)

@graphs.route("/simple.png")
def testMatPlot():
    import datetime
    import io
    import random

    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter

    fig = Figure()
    ax = fig.add_subplot(131)
    x = []
    y = []
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=1)
    for i in range(11):
        x.append(now)
        now += delta
        y.append(random.randint(0, 1000))
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas = FigureCanvas(fig)
    png_output = io.BytesIO()
    canvas.print_png(png_output)
    response = make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response