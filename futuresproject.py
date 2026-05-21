import yfinance as yf
from colorama import Style, Fore

# loon hulga for funktsiooni jaoks
futures = {
    "GC=F": "Gold",
    "ES=F": "S&P 500",
    "CL=F": "Crude Oil",
    "NQ=F": "Nasdaq 100",
}

# loon funktsiooni mis laeb andmeid alla iga mainitud futuuri kohta, kuld, snp jne
def fetch_futures(daycount):
    results = {}
    for ticker, name in futures.items():
        try:
            data = yf.download(ticker, period=f"{daycount}d", progress=False)
        except Exception as e:
            print(f"No data for {name} ({ticker}): {e}")
            continue
        data.columns = data.columns.droplevel("Ticker")
        results[name] = data
    return results

# loon funktsiooni selle jaoks, et analuusida kui palju on antud futuur kysitud paevaarvust liikus
print(f"{Fore.YELLOW}===FUTURES PRICES===\n {Style.BRIGHT}{Fore.CYAN}LONGER TERM MOVEMENT{Style.RESET_ALL}")
def longmovement(daycount, data_by_name):
    for name, data in data_by_name.items():
        today = float(data["Close"].iloc[-1])
        beginning = float(data["Close"].iloc[0])
        change = (today - beginning) / beginning * 100
        if change > 0:
            b = f"{Fore.GREEN}▲{Style.RESET_ALL}"
        elif change < 0:
            b = f"{Fore.RED}▼{Style.RESET_ALL}"
        else:
            b = ""
        print(f"\n{name} price has moved from {beginning:.2f} ({daycount} days' ago close) to {today:.2f} (currently) {b}({change:.3f}%)")
        if abs(change) > 2:
            print(f"Alert: {name} has moved more than 2%!")
print(f"{Fore.YELLOW}====================={Style.RESET_ALL}")

# loon funktsiooni, mis naitab, millises piirkonnas on hind eelmise toopaeva jooksul turul liikunud
def sessionvolatility(daycount, data_by_name):
    print(f"{Style.BRIGHT}{Fore.CYAN}===INTRADAY VOLATILITY==={Style.RESET_ALL}")
    for name, data in data_by_name.items():
        if len(data) < 2:
            print(f"{name}: not enough data")
            continue
        high = float(data["High"].iloc[-1])
        low = float(data["Low"].iloc[-1])
        yesterdayclose = float(data["Close"].iloc[-2])
        truerange = max(
            high - low,
            abs(high - yesterdayclose),
            abs(low - yesterdayclose),
        )
        volatility = (truerange / yesterdayclose) * 100
        print(f"{name} intraday volatility: {volatility:.2f}%")
    print(f"{Fore.YELLOW}====================={Style.RESET_ALL}")

# loon pidevalt küsiva tsükli
while True:
    try:
        daycount = int(round(float(input(
            f"{Fore.CYAN}Enter the number of days to check for price action (e.g., 1/5/10)> {Style.RESET_ALL}"
        ))))
        if daycount < 1:
            print(f"{Fore.RED}Please enter a number of at least 1.{Style.RESET_ALL}")
            continue
        break
    except ValueError:
        print(f"{Fore.RED}Invalid input. Please enter a number.{Style.RESET_ALL}")
data_by_name = fetch_futures(daycount)
