# encoding: utf-8

from __future__ import print_function
from functools import wraps

import numpy as np
import pandas as pd

import matplotlib.cm as cm
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import matplotlib.gridspec as gridspec
import seaborn as sns

from . import performance as pfm


DECIMAL_TO_BPS = 10000


# -----------------------------------------------------------------------------------
# plotting settings


def customize(func):
    """
    Decorator to set plotting context and axes style during function call.
    """
    @wraps(func)
    def call_w_context(*args, **kwargs):
        set_context = kwargs.pop('set_context', True)
        if set_context:
            with plotting_context(), axes_style():
                sns.despine(left=True)
                return func(*args, **kwargs)
        else:
            return func(*args, **kwargs)
    return call_w_context


def plotting_context(context='notebook', font_scale=1.5, rc=None):
    """
    Create signaldigger default plotting style context.

    Under the hood, calls and returns seaborn.plotting_context() with
    some custom settings. Usually you would use in a with-context.

    Parameters
    ----------
    context : str, optional
        Name of seaborn context.
    font_scale : float, optional
        Scale font by signal font_scale.
    rc : dict, optional
        Config flags.
        By default, {'lines.linewidth': 1.5}
        is being used and will be added to any
        rc passed in, unless explicitly overriden.

    Returns
    -------
    seaborn plotting context

    Example
    -------
    with signaldigger.plotting.plotting_context(font_scale=2):
        signaldigger.create_full_report(..., set_context=False)

    See also
    --------
    For more information, see seaborn.plotting_context().
    """
    if rc is None:
        rc = {}

    rc_default = {'lines.linewidth': 1.5}

    # Add defaults if they do not exist
    for name, val in rc_default.items():
        rc.setdefault(name, val)

    return sns.plotting_context(context=context, font_scale=font_scale, rc=rc)


def axes_style(style='darkgrid', rc=None):
    """Create signaldigger default axes style context.

    Under the hood, calls and returns seaborn.axes_style() with
    some custom settings. Usually you would use in a with-context.

    Parameters
    ----------
    style : str, optional
        Name of seaborn style.
    rc : dict, optional
        Config flags.

    Returns
    -------
    seaborn plotting context

    Example
    -------
    with signaldigger.plotting.axes_style(style='whitegrid'):
        signaldigger.create_full_report(..., set_context=False)

    See also
    --------
    For more information, see seaborn.plotting_context().

    """
    if rc is None:
        rc = {}

    rc_default = {}

    # Add defaults if they do not exist
    for name, val in rc_default.items():
        rc.setdefault(name, val)

    return sns.axes_style(style=style, rc=rc)


class GridFigure(object):
    def __init__(self, rows, cols, height_ratio=1.0):
        self.rows = rows
        self.cols = cols
        self.fig = plt.figure(figsize=(14, rows * 7 * height_ratio))
        self.gs = gridspec.GridSpec(rows, cols, wspace=0.1, hspace=0.5)
        self.curr_row = 0
        self.curr_col = 0
    
    def next_row(self):
        if self.curr_col != 0:
            self.curr_row += 1
            self.curr_col = 0
        subplt = plt.subplot(self.gs[self.curr_row, :])
        self.curr_row += 1
        return subplt
    
    def next_cell(self):
        if self.curr_col >= self.cols:
            self.curr_row += 1
            self.curr_col = 0
        subplt = plt.subplot(self.gs[self.curr_row, self.curr_col])
        self.curr_col += 1
        return subplt


# -----------------------------------------------------------------------------------
# Functions to Plot Tables


def plot_table(table, name=None, fmt=None):
    """
    Pretty print a pandas DataFrame.

    Uses HTML output if running inside Jupyter Notebook, otherwise
    formatted text output.

    Parameters
    ----------
    table : pd.Series or pd.DataFrame
        Table to pretty-print.
    name : str, optional
        Table name to display in upper left corner.
    fmt : str, optional
        Formatter to use for displaying table elements.
        E.g. '{0:.2f}%' for displaying 100 as '100.00%'.
        Restores original setting after displaying.
    """
    if isinstance(table, pd.Series):
        table = pd.DataFrame(table)
    
    if isinstance(table, pd.DataFrame):
        table.columns.name = name
    
    prev_option = pd.get_option('display.float_format')
    if fmt is not None:
        pd.set_option('display.float_format', lambda x: fmt.format(x))
    
    print(table)
    
    if fmt is not None:
        pd.set_option('display.float_format', prev_option)


def plot_information_table(ic_summary_table):
    print("Information Analysis")
    plot_table(ic_summary_table.apply(lambda x: x.round(3)).T)


def plot_quantile_statistics_table(tb):
    print("\n\nValue of signals of Different Quantiles Statistics")
    plot_table(tb)


# -----------------------------------------------------------------------------------
# Functions to Plot Returns


'''


def plot_quantile_returns_bar(mean_ret_by_q,
                              # ylim_percentiles=None,
                              ax=None):
    """
    Plots mean period wise returns for signal quantiles.

    Parameters
    ----------
    mean_ret_by_q : pd.DataFrame
        DataFrame with quantile, (group) and mean period wise return values.
    ax : matplotlib.Axes, optional
        Axes upon which to plot.

    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
        
    """
    mean_ret_by_q = mean_ret_by_q.copy().loc[:, ['mean']]
    
    ymin = None
    ymax = None
    
    if ax is None:
        f, ax = plt.subplots(1, 1, figsize=(18, 6))
    
    mean_ret_by_q.multiply(DECIMAL_TO_BPS) \
        .plot(kind='bar',
              title="Mean Return (on symbol, time) By signal Quantile", ax=ax)
    ax.set(xlabel='Quantile', ylabel='Mean Return (bps)',
           ylim=(ymin, ymax))
    
    return ax


'''


def plot_quantile_returns_ts(mean_ret_by_q, ax=None):
    """
    Plots mean period wise returns for signal quantiles.

    Parameters
    ----------
    mean_ret_by_q : pd.DataFrame
        DataFrame with quantile, (group) and mean period wise return values.
    ax : matplotlib.Axes, optional
        Axes upon which to plot.

    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
        
    """
    if ax is None:
        f, ax = plt.subplots(1, 1, figsize=(18, 6))
    
    ret_wide = pd.concat({k: v['mean'] for k, v in mean_ret_by_q.items()}, axis=1)
    ret_wide.index = pd.to_datetime(ret_wide.index, format="%Y%m%d")
    # ret_wide = ret_wide.rolling(window=22).mean()
    
    ret_wide.plot(lw=1.2, ax=ax, cmap=cm.get_cmap('RdBu'))
    ax.legend(loc='upper left')
    ymin, ymax = ret_wide.min().min(), ret_wide.max().max()
    ax.set(ylabel='Return',
           title="Daily Quantile Return (equal weight within quantile)",
           xlabel='Date',
           # yscale='symlog',
           # yticks=np.linspace(ymin, ymax, 5),
           ylim=(ymin, ymax))
    
    ax.yaxis.set_major_formatter(ScalarFormatter())
    ax.axhline(1.0, linestyle='-', color='black', lw=1)
    
    return ax


def plot_mean_quantile_returns_spread_time_series(mean_returns_spread, period,
                                                  std_err=None,
                                                  bandwidth=1,
                                                  ax=None):
    """
    Plots mean period wise returns for signal quantiles.

    Parameters
    ----------
    mean_returns_spread : pd.Series
        Series with difference between quantile mean returns by period.
    std_err : pd.Series
        Series with standard error of difference between quantile
        mean returns each period.
    bandwidth : float
        Width of displayed error bands in standard deviations.
    ax : matplotlib.Axes, optional
        Axes upon which to plot.

    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
    """
    
    if False:  # isinstance(mean_returns_spread, pd.DataFrame):
        if ax is None:
            ax = [None for a in mean_returns_spread.columns]
        
        ymin, ymax = (None, None)
        for (i, a), (name, fr_column) in zip(enumerate(ax),
                                             mean_returns_spread.items()):
            stdn = None if std_err is None else std_err[name]
            stdn = mean_returns_spread.loc
            a = plot_mean_quantile_returns_spread_time_series(fr_column,
                                                              std_err=stdn,
                                                              ax=a)
            ax[i] = a
            curr_ymin, curr_ymax = a.get_ylim()
            ymin = curr_ymin if ymin is None else min(ymin, curr_ymin)
            ymax = curr_ymax if ymax is None else max(ymax, curr_ymax)
        
        for a in ax:
            a.set_ylim([ymin, ymax])
        
        return ax
    
    periods = period
    title = ('Top Minus Bottom Quantile Return'
             .format(periods if periods is not None else ""))
    
    if ax is None:
        f, ax = plt.subplots(figsize=(18, 6))
    
    mean_returns_spread.index = pd.to_datetime(mean_returns_spread.index, format="%Y%m%d")
    mean_returns_spread_bps = mean_returns_spread['mean_diff'] * DECIMAL_TO_BPS

    std_err_bps = mean_returns_spread['std'] * DECIMAL_TO_BPS
    upper = mean_returns_spread_bps.values + (std_err_bps * bandwidth)
    lower = mean_returns_spread_bps.values - (std_err_bps * bandwidth)
    
    mean_returns_spread_bps.plot(alpha=0.4, ax=ax, lw=0.7, color='navy')
    mean_returns_spread_bps.rolling(22).mean().plot(color='green',
                                                    alpha=0.7,
                                                    ax=ax)
    # ax.fill_between(mean_returns_spread.index, lower, upper,
    #                 alpha=0.3, color='indianred')
    ax.axhline(0.0, linestyle='-', color='black', lw=1, alpha=0.8)

    ax.legend(['mean returns spread', '1 month moving avg'], loc='upper right')
    ylim = np.nanpercentile(abs(mean_returns_spread_bps.values), 95)
    ax.set(ylabel='Difference In Quantile Mean Return (bps)',
           xlabel='',
           title=title,
           ylim=(-ylim, ylim))
    
    return ax


def plot_cumulative_return(ret, ax=None, title=None):
    """
    Plots the cumulative returns of the returns series passed in.

    Parameters
    ----------
    ret : pd.Series
        Period wise returns of dollar neutral portfolio weighted by signal
        value.
    ax : matplotlib.Axes, optional
        Axes upon which to plot.

    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
    """
    if ax is None:
        f, ax = plt.subplots(1, 1, figsize=(18, 6))
    
    ret = ret.copy()
    
    cum = ret  # pfm.daily_ret_to_cum(ret)
    cum.index = pd.to_datetime(cum.index, format="%Y%m%d")
    
    cum.plot(ax=ax, lw=3, color='indianred', alpha=1.0)
    ax.axhline(0.0, linestyle='-', color='black', lw=1)
    
    metrics = pfm.calc_performance_metrics(cum, cum_return=True, compound=False)
    ax.text(.85, .30,
            "Ann.Ret. = {:.1f}%\nAnn.Vol. = {:.1f}%\nSharpe = {:.2f}".format(metrics['ann_ret']*100,
                                                                           metrics['ann_vol']*100,
                                                                           metrics['sharpe']),
            fontsize=12,
            bbox={'facecolor': 'white', 'alpha': 1, 'pad': 5},
            transform=ax.transAxes,
            verticalalignment='top')
    if title is None:
        title = "Cumulative Return"
    ax.set(ylabel='Cumulative Return',
           title=title,
           xlabel='Date')
    
    return ax


def plot_cumulative_returns_by_quantile(quantile_ret, ax=None):
    """
    Plots the cumulative returns of various signal quantiles.

    Parameters
    ----------
    quantile_ret : int: pd.DataFrame
        Cumulative returns by signal quantile.
    ax : matplotlib.Axes, optional
        Axes upon which to plot.

    Returns
    -------
    ax : matplotlib.Axes
    """
    
    if ax is None:
        f, ax = plt.subplots(1, 1, figsize=(18, 6))
    
    cum_ret = quantile_ret
    cum_ret.index = pd.to_datetime(cum_ret.index, format="%Y%m%d")
    
    cum_ret.plot(lw=2, ax=ax, cmap=cm.get_cmap('RdBu'))
    ax.axhline(0.0, linestyle='-', color='black', lw=1)
    
    ax.legend(loc='upper left')
    ymin, ymax = cum_ret.min().min(), cum_ret.max().max()
    ax.set(ylabel='Cumulative Returns',
           title='Cumulative Return of Each Quantile (equal weight within quantile)',
           xlabel='Date',
           # yscale='symlog',
           # yticks=np.linspace(ymin, ymax, 5),
           ylim=(ymin, ymax))
    
    sharpes = ["sharpe_{:d} = {:.2f}".format(col, pfm.calc_performance_metrics(ser, cum_return=True,
                                                                               compound=False)['sharpe'])
               for col, ser in cum_ret.items()]
    ax.text(.02, .30,
            '\n'.join(sharpes),
            fontsize=12,
            bbox={'facecolor': 'white', 'alpha': 1, 'pad': 5},
            transform=ax.transAxes,
            verticalalignment='top')

    ax.yaxis.set_major_formatter(ScalarFormatter())
    
    return ax


# -----------------------------------------------------------------------------------
# Functions to Plot IC


def plot_ic_ts(ic, period, ax=None):
    """
    Plots Spearman Rank Information Coefficient and IC moving
    average for a given signal.

    Parameters
    ----------
    ic : pd.DataFrame
        DataFrame indexed by date, with IC for each forward return.
    ax : matplotlib.Axes, optional
        Axes upon which to plot.

    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
    """
    ic = ic.copy()
    if isinstance(ic, pd.DataFrame):
        ic = ic.iloc[:, 0]
    mean, std = ic.mean(), ic.std()

    if ax is None:
        num_plots = 1
        f, ax = plt.subplots(num_plots, 1, figsize=(18, num_plots * 7))
        ax = np.asarray([ax]).flatten()

    ic.plot(ax=ax, lw=0.6, color='navy', label='daily IC', alpha=0.8)
    ic.rolling(22).mean().plot(ax=ax, color='royalblue', lw=2, alpha=0.6, label='1 month MA')
    ax.axhline(0.0, linestyle='-', color='black', linewidth=1, alpha=0.8)

    ax.text(.05, .95,
            "Mean {:.3f} \n Std. {:.3f}".format(mean, std),
            fontsize=16,
            bbox={'facecolor': 'white', 'alpha': 1, 'pad': 5},
            transform=ax.transAxes,
            verticalalignment='top',
            )
    
    ymin, ymax = (None, None)
    curr_ymin, curr_ymax = ax.get_ylim()
    ymin = curr_ymin if ymin is None else min(ymin, curr_ymin)
    ymax = curr_ymax if ymax is None else max(ymax, curr_ymax)

    ax.legend(loc='upper right')
    ax.set(ylabel='IC', xlabel="", ylim=[ymin, ymax],
           title="Daily IC and Moving Average".format(period))
    
    return ax


def plot_ic_hist(ic, period, ax=None):
    """
    Plots Spearman Rank Information Coefficient histogram for a given signal.

    Parameters
    ----------
    ic : pd.DataFrame
        DataFrame indexed by date, with IC for each forward return.
    ax : matplotlib.Axes, optional
        Axes upon which to plot.

    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
    """

    ic = ic.copy()
    if isinstance(ic, pd.DataFrame):
        ic = ic.iloc[:, 0]
    mean, std = ic.mean(), ic.std()
    
    if ax is None:
        v_spaces = 1
        f, ax = plt.subplots(v_spaces, 3, figsize=(18, v_spaces * 6))
        ax = ax.flatten()

    sns.distplot(ic.replace(np.nan, 0.), ax=ax,
                 hist_kws={'color': 'royalblue'},
                 kde_kws={'color': 'navy', 'alpha': 0.5},
                 # hist_kws={'weights':},
                 )
    ax.axvline(mean, color='indianred', linestyle='dashed', linewidth=1.0, label='Mean')
    ax.text(.05, .95,
            "Mean {:.3f} \n Std. {:.3f}".format(mean, std),
            fontsize=16,
            bbox={'facecolor': 'white', 'alpha': 1, 'pad': 5},
            transform=ax.transAxes,
            verticalalignment='top')
    
    ax.set(title="Distribution of Daily IC",
           xlabel='IC',
           xlim=[-1, 1])
    ax.legend(loc='upper right')

    return ax


def plot_monthly_ic_heatmap(mean_monthly_ic, period, ax=None):
    """
    Plots a heatmap of the information coefficient or returns by month.

    Parameters
    ----------
    mean_monthly_ic : pd.DataFrame
        The mean monthly IC for N periods forward.

    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
    """
    
    mean_monthly_ic = mean_monthly_ic.copy()
    
    num_plots = 1.0
    
    v_spaces = ((num_plots - 1) // 3) + 1
    
    if ax is None:
        f, ax = plt.subplots(v_spaces, 3, figsize=(18, v_spaces * 6))
        ax = ax.flatten()
    
    new_index_year = []
    new_index_month = []
    for date in mean_monthly_ic.index:
        new_index_year.append(date.year)
        new_index_month.append(date.month)
    
    mean_monthly_ic.index = pd.MultiIndex.from_arrays(
            [new_index_year, new_index_month],
            names=["year", "month"])
    
    sns.heatmap(
            mean_monthly_ic.unstack(),
            annot=True,
            alpha=1.0,
            center=0.0,
            annot_kws={"size": 7},
            linewidths=0.01,
            linecolor='white',
            cmap=cm.get_cmap('RdBu'),
            cbar=False,
            ax=ax)
    ax.set(ylabel='', xlabel='')
    
    ax.set_title("IC Monthly Mean".format(period))
    
    return ax


# -----------------------------------------------------------------------------------
# Functions to Plot Others
def plot_event_bar(mean_ret, ax):
    ax.bar(mean_ret.index, mean_ret.values * DECIMAL_TO_BPS, width=8.0)
    
    ax.set(xlabel='Period Length', ylabel='bps')
    ax.legend(list(map(lambda x: str(x), mean_ret.index.values)))
    return ax


def plot_event_dist(df_events, axs):
    i = 0
    for period, ser in df_events.items():
        ax = axs[i]
        sns.distplot(ser, ax=ax)
        ax.set(xlabel='Return', ylabel='',
               title="Distribution of return after {:d} trade dats".format(period))
        # self.show_fig(fig, 'event_return_{:d}days.png'.format(my_period))
        i += 1
    
    # print(mean)
