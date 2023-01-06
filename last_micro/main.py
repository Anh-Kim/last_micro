from flask import Flask
from pytrends.request import TrendReq
import matplotlib.pyplot as plt
import io
import base64
import time

app = Flask(__name__)

@app.route('/', methods=["GET"])
def trend():
    # Build the payload for the request
    kw_list = ["Crêpe", "Gauffre"]
    timeframe = "2022-10-01 2023-01-01"
    pytrend = TrendReq(retries=5)
    pytrend.build_payload(kw_list, cat=0, timeframe=timeframe, geo='', gprop='')

    # Get the interest over time data
    df = pytrend.interest_over_time()
    time.sleep(5)

    if all(df.isPartial == False):
        del df['isPartial']

    # Generate a plot of the interest over time data
    fig, ax = plt.subplots(figsize=(8, 6))
    df.iloc[:,0].plot.line(ax=ax)
    df.iloc[:,1].plot.line(ax=ax)
    plt.xlabel('Date')
    plt.legend(loc='lower left')

    # Convert the plot to a base64-encoded image
    img = io.BytesIO()
    fig.savefig(img, format='jpeg', bbox_inches='tight', dpi=20)
    img.seek(0)
    plot_data = base64.b64encode(img.getvalue()).decode()

    # Return the plot in the response
    return '<img src="data:image/png;base64,{}">'.format(plot_data)


if __name__ == "__main__":
    app.run()
