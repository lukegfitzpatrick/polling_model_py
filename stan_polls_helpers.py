import numpy as np
import pandas as pd
import pickle
import csv
import matplotlib.pyplot as plt
import datetime
import pystan
import os

def get_median_percentile(fit, name='', niter=0, save=True):
    mu = fit.extract(permuted=True)['mu']
    low = np.nanpercentile(mu, 2.5, axis=0)
    high = np.nanpercentile(mu, 97.5, axis=0)
    mum = np.median(mu, axis=0)
    if save:
        pickle.dump(mum, open('mu_%s_%s.pkl' % (name, niter), 'wb'))
        pickle.dump(low, open('low_%s_%s.pkl' % (name, niter), 'wb'))
        pickle.dump(high, open('high_%s_%s.pkl' % (name, niter), 'wb'))
    return mum, low, high


def get_data(fname="data_polls.csv", numdays=500):
    re =  csv.reader(open(fname))
    Y_clinton, Y_trump, sigma, dates = [], [], [] ,[]
    mdate = {}
    for r in re:
        end_date= r[1]
        if r[2] == "--":
            r[2] = 5
        mdate[end_date] = mdate.get(end_date, []) + [[ float(r[3]), float(r[4]), float(r[2]), r[0], r[1] ] ]

    base = datetime.datetime(2016,12,23)
    date_list = [base - datetime.timedelta(days=x) for x in range(0, 365)]

    for k in date_list[::-1]:
        k = k.strftime("%Y/%m/%d")

        vals = mdate.get(k, [])
        vals = vals + ([[-9]*7 ]*(7-len(vals)))
        Y_clinton.append([v[0] for v in vals])
        Y_trump.append([v[1] for v in vals])
        sigma.append([v[2] for v in vals])
        dates.append(k)

    return [np.array(x) for x in [Y_clinton, Y_trump, sigma, dates]]

def fit_stan(stan_dat, n_chains, n_iter, fit=None, verbose=False):
    fit = pystan.stan(
            fit = fit,
            file='state_space_polls.stan',
            data=stan_dat,
            chains=n_chains,
            iter=n_iter,
            verbose= verbose,
        )

    return fit

def read_n_plot(path, niter, title, Y_clinton, Y_trump, dates):
    os.chdir(path)
    chi = []
    with (open('high_Clinton_'+str(niter)+'.pkl', "rb")) as openfile:
        while True:
            try:
                chi.append(pickle.load(openfile))
            except EOFError:
                break

    clo = []
    with (open('low_Clinton_'+str(niter)+'.pkl', "rb")) as openfile:
        while True:
            try:
                clo.append(pickle.load(openfile))
            except EOFError:
                break

    cmu = []
    with (open('mu_Clinton_'+str(niter)+'.pkl', "rb")) as openfile:
        while True:
            try:
                cmu.append(pickle.load(openfile))
            except EOFError:
                break

    thi = []
    with (open('high_Trump_'+str(niter)+'.pkl', "rb")) as openfile:
        while True:
            try:
                thi.append(pickle.load(openfile))
            except EOFError:
                break

    tlo = []
    with (open('low_Trump_'+str(niter)+'.pkl', "rb")) as openfile:
        while True:
            try:
                tlo.append(pickle.load(openfile))
            except EOFError:
                break

    tmu = []
    with (open('mu_Trump_'+str(niter)+'.pkl', "rb")) as openfile:
        while True:
            try:
                tmu.append(pickle.load(openfile))
            except EOFError:
                break

    df_clinton = pd.DataFrame(Y_clinton, index=pd.DatetimeIndex(dates))
    df_clinton['mu'] = cmu[0]
    df_clinton['hi'] = chi[0]
    df_clinton['lo'] = clo[0]

    df_trump = pd.DataFrame(Y_trump, index = pd.DatetimeIndex(dates))
    df_trump['mu'] = tmu[0]
    df_trump['hi'] = thi[0]
    df_trump['lo'] = tlo[0]

    fig, ax = plt.subplots(figsize=(25, 10))
    for col in range(7):
        plt.scatter(df_clinton.loc[df_clinton[col]!=-9].index, df_clinton[col].loc[df_clinton[col]!=-9], color='blue', s=3)
        plt.scatter(df_trump.loc[df_trump[col]!=-9].index, df_trump[col].loc[df_trump[col]!=-9], color='red', s= 3)

        plt.plot(df_trump.index, df_trump.mu, color='red')
        plt.fill_between(df_trump.index, df_trump['lo'], df_trump['hi'], alpha=0.1, color='gray')

        plt.plot(df_clinton.index, df_clinton.mu, color='blue')
        plt.fill_between(df_clinton.index, df_clinton['lo'], df_clinton['hi'], alpha=0.1, color='gray')
        plt.title(title, fontsize=20)

    return fig
