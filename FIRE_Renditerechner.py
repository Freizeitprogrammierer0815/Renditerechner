import matplotlib.pyplot as plt
import numpy as np
import panel as pn

# Initialize Panel extension
pn.extension()

# Default values
Start_cap = 80000
payout_year = 30
rendite = 0.088
monthly = 2000
payoutrate = 0.03
inflat = 0.0191

# Widgets
Interest_on_invest_widget = pn.widgets.FloatSlider(name='Interest on Investment', start=0.01, end=0.2, step=0.002, value=rendite, format='0.00%')
Start_capital_widget = pn.widgets.FloatSlider(name='Start Capital', start=0, end=200000, step=1000, value=Start_cap)
Monthly_invest_widget = pn.widgets.FloatSlider(name='Monthly Investment', start=50, end=3000, step=50, value=monthly)
payoutrate_widget = pn.widgets.FloatSlider(name='Payout Rate', start=0.01, end=0.1, step=0.001, value=payoutrate, format='0.0%')
years_til_payout_widget = pn.widgets.FloatSlider(name='Years till Payout', start=1, end=60, step=1, value=payout_year)
inflation_widget = pn.widgets.FloatSlider(name='Inflation', start=0.00, end=0.1, step=0.0001, value=inflat, format='0.00%')

# Function for calculation and plotting
def f(Interest_on_invest, Start_capital, Monthly_invest, years_til_payout, inflation, payoutrate):
    fig, ax = plt.subplots(figsize=(6, 4))
    k = Start_capital
    A_0 = Monthly_invest * 12
    kk = []
    ii = []

    # Investment period
    for i in range(int(years_til_payout)):
        k = (k * (1 + Interest_on_invest - inflation) + A_0)
        kk.append(k)
        ii.append(i)

    # Payout period
    payout_start = k
    for i in range(int(years_til_payout), int(years_til_payout + 30)):  # Example: 30 years of payout
        k = (k - payout_start * payoutrate) * (1 + Interest_on_invest - inflation)
        kk.append(k)
        ii.append(i)

    ax.plot(ii, kk, label="Total Capital")
    ax.set_ylim(-10000, max(kk) + 20000)
    ax.set_xlabel("Years")
    ax.set_ylabel("Capital (€)")
    ax.grid()
    ax.legend()
    plt.close(fig)  # Close the figure to avoid duplicate rendering
    return fig

# Pane to dynamically update the plot
def update_plot():
    fig = f(
        Interest_on_invest_widget.value,
        Start_capital_widget.value,
        Monthly_invest_widget.value,
        years_til_payout_widget.value,
        inflation_widget.value,
        payoutrate_widget.value,
    )
    return fig

plot_pane = pn.pane.Matplotlib(update_plot(), sizing_mode="stretch_width")

# Callback to refresh the plot whenever a widget value changes
def refresh_plot(event=None):
    plot_pane.object = update_plot()

# Link widget value changes to the refresh function
for widget in [
    Interest_on_invest_widget,
    Start_capital_widget,
    Monthly_invest_widget,
    years_til_payout_widget,
    inflation_widget,
    payoutrate_widget,
]:
    widget.param.watch(refresh_plot, "value")

# Layout
dashboard = pn.Column(
    pn.pane.Markdown("# Renten Rechner Dashboard"),
    Interest_on_invest_widget,
    Start_capital_widget,
    Monthly_invest_widget,
    years_til_payout_widget,
    inflation_widget,
    payoutrate_widget,
    plot_pane,
)

# Serve the dashboard
dashboard.servable()
pn.serve(dashboard)
