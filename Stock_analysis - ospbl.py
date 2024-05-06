import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
import pandas_ta as ta
import matplotlib.dates as mdates
from datetime import datetime, timedelta



def plotGraph(df, title='Stock Prices'):
    ax = df.plot(title=title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.show()

def fetchData(stock):
    data = yf.download(stock, start=start_date, end=end_date)
    data.to_csv(stock + '.csv')

def normalizedData(df):
    return df / df.iloc[0, :]

def createDataFrame(stockList, start_date, end_date):
    dates = pd.date_range(start_date, end_date)
    df = pd.DataFrame(index=dates)
    for stock in stockList:
        data = pd.read_csv(stock + '.csv', index_col="Date", parse_dates=True, usecols=['Date', 'Close'],
                        na_values=['nan'])
        data = data.rename(columns={'Close': stock})
        df = df.join(data)
        df = df.dropna()
    return df

def plotRollingMean(mergedData, stock):
    ax = mergedData[stock].plot(title=stock + " Rolling Mean", label=stock)
    rollingMean = getRollingMean(mergedData[stock], window=20)
    rollingMean.plot(label="Rolling Mean", ax=ax)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend(loc="upper right")
    plt.show()

def getRollingMean(values, window):
    return values.rolling(window).mean()

def getRollingStd(values, window):
    return values.rolling(window).std()

def getBollingerBands(rollMean, rollStd):
    upperBand = rollMean + rollStd * 2
    lowerBand = rollMean - rollStd * 2
    return upperBand, lowerBand

def plotBollingerBand(data, rollMean, upper_Band, lower_Band, stock):
    ax = data.plot(title="Bollinger Bands", label=stock)
    rollMean.plot(label="Rolling Mean", ax=ax)
    upper_Band.plot(label="Upper Band", ax=ax)
    lower_Band.plot(label="Lower Band", ax=ax)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend(loc="upper right")
    plt.show()

def computeDailyReturns(df):
    return (df / df.shift(1)) - 1

def plotDailyReturns(dailyReturns, title, xlabel, label):
    ax = dailyReturns.plot(title=title, label=label)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Daily Returns")
    ax.legend(loc="upper right")
    plt.show()



def plotGraph(df, title='Stock Prices'):
    ax = df.plot(title=title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.show()



def plotGraph(df, title='Stock Prices'):
    ax = df.plot(title=title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.show()



def plotGraph(df, title='Stock Prices'):
    ax = df.plot(title=title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.show()
    
def get_date(date_entry):
    return date_entry.get_date()


class StockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Analysis App")

        self.symbol_label = ttk.Label(root, text="Enter Stock Symbol:")
        self.symbol_label.grid(row=0, column=0, padx=5, pady=5)
        self.symbol_entry = ttk.Entry(root)
        self.symbol_entry.grid(row=0, column=1, padx=5, pady=5)

        self.start_label = ttk.Label(root, text="Select Start Date:")
        self.start_label.grid(row=1, column=0, padx=5, pady=5)
        self.start_entry = DateEntry(root, date_pattern='yyyy-mm-dd')
        self.start_entry.grid(row=1, column=1, padx=5, pady=5)

        self.end_label = ttk.Label(root, text="Select End Date:")
        self.end_label.grid(row=2, column=0, padx=5, pady=5)
        self.end_entry = DateEntry(root, date_pattern='yyyy-mm-dd')
        self.end_entry.grid(row=2, column=1, padx=5, pady=5)

        self.submit_button1 = ttk.Button(root, text="Above 3 Months Analysis", command=self.plot_stock_existing)
        self.submit_button1.grid(row=3, column=0, padx=5, pady=5)

        self.submit_button2 = ttk.Button(root, text="Below 3 Months Analysis", command=self.plot_stock_new)
        self.submit_button2.grid(row=3, column=1, padx=5, pady=5)



    def plot_stock_existing(self):
        symbol = self.symbol_entry.get()
        start_date = self.start_entry.get()
        end_date = self.end_entry.get()

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
            return

        stock_data = yf.download(symbol, start=start_date, end=end_date)
        stock_data = yf.download(symbol, start=start_date, end=end_date)
        stock_data.ta.macd(append=True)
        stock_data.ta.rsi(append=True)
        stock_data.ta.bbands(append=True)
        stock_data.ta.obv(append=True)
        stock_data.ta.sma(length=20, append=True)
        stock_data.ta.ema(length=50, append=True)
        stock_data.ta.stoch(append=True)
        stock_data.ta.adx(append=True)
        stock_data.ta.willr(append=True)
        stock_data.ta.cmf(append=True)
        stock_data.ta.psar(append=True)
        stock_data['OBV_in_million'] = stock_data['OBV'] / 1e7
        stock_data['MACD_histogram_12_26_9'] = stock_data['MACDh_12_26_9']

        last_day_summary = stock_data.iloc[-1][['Adj Close',
                                                'MACD_12_26_9', 'MACD_histogram_12_26_9', 'RSI_14', 'BBL_5_2.0',
                                                'BBM_5_2.0', 'BBU_5_2.0', 'SMA_20', 'EMA_50', 'OBV_in_million',
                                                'STOCHk_14_3_3', 'STOCHd_14_3_3', 'ADX_14', 'WILLR_14', 'CMF_20',
                                                'PSARl_0.02_0.2', 'PSARs_0.02_0.2']]

        summary_message = "Summary of Technical Indicators for the Last Day:\n\n" + last_day_summary.to_string()
        messagebox.showinfo("Last Day Summary", summary_message)

        plt.figure(figsize=(14, 8))
        plt.subplot(4, 2, 1)
        plt.plot(stock_data.index, stock_data['Adj Close'], label='Adj Close', color='blue')
        plt.plot(stock_data.index, stock_data['EMA_50'], label='EMA 50', color='green')
        plt.plot(stock_data.index, stock_data['SMA_20'], label='SMA_20', color='orange')
        plt.title("Price Trend")
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b%d'))
        plt.xticks(rotation=45, fontsize=8)
        plt.legend()

        plt.subplot(4, 2, 2)
        plt.plot(stock_data['OBV'], label='On-Balance Volume')
        plt.title('On-Balance Volume (OBV) Indicator')
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b%d'))
        plt.xticks(rotation=45, fontsize=8)
        plt.legend()

        plt.subplot(4, 2, 3)
        plt.plot(stock_data['MACD_12_26_9'], label='MACD')
        plt.plot(stock_data['MACDh_12_26_9'], label='MACD Histogram')
        plt.title('MACD Indicator')
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b%d'))
        plt.xticks(rotation=45, fontsize=8)
        plt.title("MACD")
        plt.legend()

        plt.subplot(4, 2, 4)
        plt.plot(stock_data['RSI_14'], label='RSI')
        plt.axhline(y=70, color='r', linestyle='--', label='Overbought (70)')
        plt.axhline(y=30, color='g', linestyle='--', label='Oversold (30)')
        plt.legend()
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b%d'))
        plt.xticks(rotation=45, fontsize=8)
        plt.title('RSI Indicator')

        plt.subplot(4, 2, 5)
        plt.plot(stock_data.index, stock_data['BBU_5_2.0'], label='Upper BB')
        plt.plot(stock_data.index, stock_data['BBM_5_2.0'], label='Middle BB')
        plt.plot(stock_data.index, stock_data['BBL_5_2.0'], label='Lower BB')
        plt.plot(stock_data.index, stock_data['Adj Close'], label='Adj Close', color='brown')
        plt.title("Bollinger Bands")
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b%d'))
        plt.xticks(rotation=45, fontsize=8)
        plt.legend()

        plt.subplot(4, 2, 6)
        plt.plot(stock_data.index, stock_data['STOCHk_14_3_3'], label='Stoch %K')
        plt.plot(stock_data.index, stock_data['STOCHd_14_3_3'], label='Stoch %D')
        plt.title("Stochastic Oscillator")
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b%d'))
        plt.xticks(rotation=45, fontsize=8)
        plt.legend()

        plt.subplot(4, 2, 7)
        plt.plot(stock_data.index, stock_data['WILLR_14'])
        plt.title("Williams %R")
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b%d'))
        plt.xticks(rotation=45, fontsize=8)

        plt.subplot(4, 2, 8)
        plt.plot(stock_data.index, stock_data['ADX_14'])
        plt.title("Average Directional Index (ADX)")
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b%d'))
        plt.xticks(rotation=45, fontsize=8)

        plt.tight_layout()
        plt.show()


        # Your existing code for plotting using the fetched data goes here...


    def plot_stock_new(self):
        symbol = self.symbol_entry.get()
        start_date = self.start_entry.get()
        end_date = self.end_entry.get()

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
            return

        stock_data = yf.download(symbol, start=start_date, end=end_date)
        # Your new code for plotting using the fetched data goes here...



        # Define the stock symbol and timeframe
        symbol = symbol
        end_date = datetime.today()
        start_date = end_date - timedelta(days=90)  # 3 months before today

        # Fetch stock data using yfinance
        stock_data = yf.download(symbol, start=start_date, end=end_date)

        # Calculate technical indicators using pandas-ta
        stock_data.ta.macd(append=True)
        stock_data.ta.rsi(append=True)
        stock_data.ta.bbands(append=True)
        stock_data.ta.obv(append=True)

        # Calculate additional technical indicators
        stock_data.ta.sma(length=20, append=True)
        stock_data.ta.ema(length=50, append=True)
        stock_data.ta.stoch(append=True)
        stock_data.ta.adx(append=True)

        # Calculate other indicators
        stock_data.ta.willr(append=True)
        stock_data.ta.cmf(append=True)
        stock_data.ta.psar(append=True)

        #convert OBV to million
        stock_data['OBV_in_million'] =  stock_data['OBV']/1e7
        stock_data['MACD_histogram_12_26_9'] =  stock_data['MACDh_12_26_9'] # not to confuse chatGTP

        # Summarize technical indicators for the last day
        last_day_summary = stock_data.iloc[-1][['Adj Close',
        'MACD_12_26_9','MACD_histogram_12_26_9', 'RSI_14', 'BBL_5_2.0', 'BBM_5_2.0', 'BBU_5_2.0','SMA_20', 'EMA_50','OBV_in_million', 'STOCHk_14_3_3', 
        'STOCHd_14_3_3', 'ADX_14',  'WILLR_14', 'CMF_20', 
        'PSARl_0.02_0.2', 'PSARs_0.02_0.2'
        ]]

        print("Summary of Technical Indicators for the Last Day:")
        print(last_day_summary)

        ## Work on the prompt
        sys_prompt = """
        Assume the role as a leading Technical Analysis (TA) expert in the stock market, \
        a modern counterpart to Charles Dow, John Bollinger, and Alan Andrews. \
        Your mastery encompasses both stock fundamentals and intricate technical indicators. \
        You possess the ability to decode complex market dynamics, \
        providing clear insights and recommendations backed by a thorough understanding of interrelated factors. \
        Your expertise extends to practical tools like the pandas_ta module, \
        allowing you to navigate data intricacies with ease. \
        As a TA authority, your role is to decipher market trends, make informed predictions, and offer valuable perspectives.

        given {} TA data as below on the last trading day, what will be the next few days possible stock price movement? 

        Summary of Technical Indicators for the Last Day:
        {}""".format(symbol,last_day_summary)

        print(sys_prompt)

        # Plot the technical indicators
        plt.figure(figsize=(14, 8))

        # Price Trend Chart
        plt.subplot(3, 3, 1)
        plt.plot(stock_data.index, stock_data['Adj Close'], label='Adj Close', color='blue')
        plt.plot(stock_data.index, stock_data['EMA_50'], label='EMA 50', color='green')
        plt.plot(stock_data.index, stock_data['SMA_20'], label='SMA_20', color='orange')
        plt.title("Price Trend")
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b%d'))  # Format date as "Jun14"
        plt.xticks(rotation=45, fontsize=8)  # Adjust font size
        plt.legend()

        # On-Balance Volume Chart
        plt.subplot(3, 3, 2)
        plt.plot(stock_data['OBV'], label='On-Balance Volume')
        plt.title('On-Balance Volume (OBV) Indicator')
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b%d'))  # Format date as "Jun14"
        plt.xticks(rotation=45, fontsize=8)  # Adjust font size
        plt.legend()

        # MACD Plot
        plt.subplot(3, 3, 3)
        plt.plot(stock_data['MACD_12_26_9'], label='MACD')
        plt.plot(stock_data['MACDh_12_26_9'], label='MACD Histogram')
        plt.title('MACD Indicator')
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b%d'))  # Format date as "Jun14"
        plt.xticks(rotation=45, fontsize=8)  # Adjust font size
        plt.title("MACD")
        plt.legend()

        # RSI Plot
        plt.subplot(3, 3, 4)
        plt.plot(stock_data['RSI_14'], label='RSI')
        plt.axhline(y=70, color='r', linestyle='--', label='Overbought (70)')
        plt.axhline(y=30, color='g', linestyle='--', label='Oversold (30)')
        plt.legend()
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b%d'))  # Format date as "Jun14"
        plt.xticks(rotation=45, fontsize=8)  # Adjust font size
        plt.title('RSI Indicator')

        # Bollinger Bands Plot
        plt.subplot(3, 3, 5)
        plt.plot(stock_data.index, stock_data['BBU_5_2.0'], label='Upper BB')
        plt.plot(stock_data.index, stock_data['BBM_5_2.0'], label='Middle BB')
        plt.plot(stock_data.index, stock_data['BBL_5_2.0'], label='Lower BB')
        plt.plot(stock_data.index, stock_data['Adj Close'], label='Adj Close', color='brown')
        plt.title("Bollinger Bands")
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b%d'))  # Format date as "Jun14"
        plt.xticks(rotation=45, fontsize=8)  # Adjust font size
        plt.legend()

        # Stochastic Oscillator Plot
        plt.subplot(3, 3, 6)
        plt.plot(stock_data.index, stock_data['STOCHk_14_3_3'], label='Stoch %K')
        plt.plot(stock_data.index, stock_data['STOCHd_14_3_3'], label='Stoch %D')
        plt.title("Stochastic Oscillator")
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b%d'))  # Format date as "Jun14"
        plt.xticks(rotation=45, fontsize=8)  # Adjust font size
        plt.legend()

        # Williams %R Plot
        plt.subplot(3, 3, 7)
        plt.plot(stock_data.index, stock_data['WILLR_14'])
        plt.title("Williams %R")
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b%d'))  # Format date as "Jun14"
        plt.xticks(rotation=45, fontsize=8)  # Adjust font size

        # ADX Plot
        plt.subplot(3, 3, 8)
        plt.plot(stock_data.index, stock_data['ADX_14'])
        plt.title("Average Directional Index (ADX)")
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b%d'))  # Format date as "Jun14"
        plt.xticks(rotation=45, fontsize=8)  # Adjust font size

        # CMF Plot
        plt.subplot(3, 3, 9)
        plt.plot(stock_data.index, stock_data['CMF_20'])
        plt.title("Chaikin Money Flow (CMF)")
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b%d'))  # Format date as "Jun14"
        plt.xticks(rotation=45, fontsize=8)  # Adjust font size

        # Show the plots
        plt.tight_layout()
        plt.show()

root = tk.Tk()
app = StockApp(root)
root.mainloop()
