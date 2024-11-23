from shiny import App, reactive, render, ui
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm, ttest_ind

# Z-test function
def calculate_ztest(control, test):
    """
    Perform a Z-test for two samples.
    Returns the effect size, Z-statistic, and p-value.
    """
    mean_control = np.mean(control)
    mean_test = np.mean(test)

    var_mean_control = np.var(control, ddof=1) / len(control)
    var_mean_test = np.var(test, ddof=1) / len(test)

    difference_mean = mean_test - mean_control
    difference_mean_var = var_mean_control + var_mean_test

    zstat = difference_mean / np.sqrt(difference_mean_var)
    pvalue = norm.sf(np.abs(zstat)) * 2  # two-sided
    effect = difference_mean

    return effect, zstat, pvalue

def compute_ecdf(data):
    sorted_data = np.sort(data)
    y = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
    return sorted_data, y

# Define the UI
app_ui = ui.page_fluid(
    ui.h1("Welch test with unequal variances VS asymptotic Z test with equal variances"),
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_slider("num_sim", "Number of Simulations:", min=100, max=20000, value=1000, step=100),
            ui.input_numeric("variance_mult", "Variance Multiplier:", value=1.0, min=0.1, max=10, step=0.1),
            ui.input_numeric("lift", "Lift, % for AB test", value=0.1, min=0, max=1, step=0.1),
            ui.input_action_button("run_sim", "Run Simulation", class_="btn-primary"),
        ),
        # Output section for the results
        ui.output_plot("main", width=800, height=800),
    )
)

def server(input, output, session):

    @reactive.calc()
    def run_simulation():
        nsim = input.num_sim()
        variance_multiplier = input.variance_mult()
        lift = input.lift()
        base_var = 1

        pv = []

        for i in range(nsim):
            cnt = norm.rvs(loc=1, scale=base_var, size=10000)
            trt = norm.rvs(loc=1 * (1 + lift), scale=base_var * variance_multiplier, size=10000)

            zt_result = calculate_ztest(cnt, trt)
            ttest_result = ttest_ind(cnt, trt, equal_var=False)

            pv.append([variance_multiplier, zt_result[2], ttest_result.pvalue])

        # Store results in the reactive values
        df = pd.DataFrame(pv, columns=["var_mult", "pvalue_zt", "pvalue_tt"])

        return df

    @render.plot
    @reactive.event(input.run_sim, ignore_none=True)
    def main():

        df = run_simulation()
        # Create a figure and axis object
        fig, ax = plt.subplots(figsize=(8, 8))

        # Compute ECDF
        xt, yt = compute_ecdf(df["pvalue_tt"])
        xz, yz = compute_ecdf(df["pvalue_zt"])
        
        # Plot ECDF
        ax.step(xt, yt, where="post", color="blue", label='TTest')
        ax.step(xz, yz, where="post", color="red", label='ZTest', alpha=0.6)
        ax.set_title(f'Var in B is {input.variance_mult()} times higher than in A', fontsize=10)
        ax.grid(True)

        ax.legend()
        return fig

# Run the app
app = App(app_ui, server)
