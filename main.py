"""
Joseph Dowdy
MIS 315, Summer 1st Session 2022 - Section 1
6/28/22
Homework Assignment #5, Crypto rate conversion w/ an API
I, Joseph Dowdy, can attest that this script is my work and my work alone, enjoy! :-)

I have a lot of template 'rows'(lists) set up to make writing to the csv file much easier. Overall my process is to make
the request to the api while only requesting the live data for the 4 crypto coins. Their respective values are stored
into a list. The user is then prompted with a GUI. Any blank entry boxes are treated as 0.0. When clicked, the
conversion button takes the entered values and attempts to cast them as floats, if unsuccessful an error message
appears. If successful the script continues to do calculations and writes the desired output to a csv file title
'crypto_conversions.csv'. This script only supports writing one set of conversions at a time, meaning if a user enters
values and converts and then writes more values and converts, only the later values will be reflected in the csv
file. Entry boxes are cleared after successful conversions as well as a message box appears telling the user that the
conversion was successful.

Note - I wrote this code on MacOS which is a little wonky when configuring button background colors. I found a method
to change them (highlightbackground) but I am unsure if this will properly display my chosen color on PC. I apologize
in advance for the trouble.
"""

# -------------------------------------------------- Imports ---------------------------------------------------------#
import requests
import json
import tkinter
import csv
import tkinter.messagebox

# -------------------------------------------------- Variables -------------------------------------------------------#
SYMBOLS = "BTC,ETH,XRP,BNB"
SYMBOLS_COLUMN = ["BTC", "ETH", "BNB", "XRP"]
HASH_ROW = ["--", "--", "--","--", "--"]
sum_entered = 0

MY_KEY = "9dea11b46f55bb9473f6ebd06874807e"
URL = f"http://api.coinlayer.com/api/live?access_key={MY_KEY}&symbols={SYMBOLS}"
HEADER = ["Currency", "Price", "Quantity", "Cost(USD)", "Exchange Rate USD:COIN"]

overall_bg_color = "bisque"
convert_btn_color = "green1"
exit_btn_color = "#FF8C00"

exchange_rates = []
entries = []
usd_costs = []


# -------------------------------------------------- Functions -------------------------------------------------------#


def calculate_exchange():
    """This function is called when the conversion button is clicked. When called it collects the entry box data and
    attempts to store the values as floats (null are treated as 0.0). Afterwords appropriate functions and calculations
    are called to finalize the process and write to a csv file."""

    global entries
    global exchange_rates
    global sum_entered
    global usd_costs

    # resetting global variables in case user does multiple conversions in a session.
    sum_entered = 0
    exchange_rates = []
    entries = [btc_entry.get(), eth_entry.get(), bnb_entry.get(), xrp_entry.get()]

    # checking if any boxes were left unpopulated, if so they are assigned to 0.0
    for i in range(0, len(entries)):
        if entries[i] == "":
            entries[i] = 0.0

    try:
        # trying to convert entered values into floats.
        for i in range(0, len(entries)):
            entries[i] = float(entries[i])

            # successful entries are added to running sum
            sum_entered += entries[i] * crypto_rates[i]
            # math completed to calculate exchanged coins from USD
            exchange_rates.append(1 / crypto_rates[i])
            usd_costs.append((entries[i] * crypto_rates[i]))

        # rounding sum_entered to two decimals for professionalism
        sum_entered = round(sum_entered, 2)

        # Calling two other functions to complete writing to the csv and clearing the entry boxes
        write_to_file()
        reset_entries()

    except:
        # This sends error message to user to check for value types
        tkinter.messagebox.showerror("Error", "Sorry, the report could not be written. "
                                              "Check to ensure you are entering positive numbers and not "
                                              "strings/negative values")


def write_to_file():
    """This function, when called, opens and writes to crypto_conversion.csv the appropriate requested format"""

    # opening crypto_conversion.csv in write mode and storing it as file
    with open("crypto_conversion.csv", "w") as file:
        # creating the csv writer
        writer = csv.writer(file, lineterminator="\n")

        # writing the header onto the csv file
        writer.writerow(HEADER)

        # looping through to write appropriate rows with live data
        for i in range(0, len(entries)):
            row = [SYMBOLS_COLUMN[i], crypto_rates[i], entries[i], usd_costs[i], exchange_rates[i]]
            writer.writerow(row)

        # This is to write the default hash row and bottom total row
        writer.writerow(HASH_ROW)
        total_row = ["Total", "--", "--", sum_entered, "--"]
        writer.writerow(total_row)

    # Message box showing success
    tkinter.messagebox.showinfo("Complete", "The conversions were stored in crypto_conversion.csv")


def reset_entries():
    """This function, when called, resets all the entry boxes to null"""
    btc_entry.delete(0, "end")
    eth_entry.delete(0, "end")
    bnb_entry.delete(0, "end")
    xrp_entry.delete(0, "end")


def close_application():
    """This function, when called, terminates the GUI"""
    print("Application successfully closed.")
    root.destroy()


# ------------------------------------------- Main Logic & GUI Setup -------------------------------------------------#

# response to get requested URL with key and other requests (only specific coins)
response = requests.get(URL)

# if response is successful, the main logic and GUI commences
if response:

    # loading response into json
    data = json.loads(response.text)
    # gathering needed live rates for conversion from json file
    crypto_rates = [data["rates"]["BTC"], data["rates"]["ETH"], data["rates"]["BNB"], data["rates"]["XRP"]]

    root = tkinter.Tk()
    root.title("Exchange Rate Calculator")
    root.configure(bg=overall_bg_color)

    # btc label setup
    btc_label = tkinter.Label(root, text="BTC:")
    btc_label.configure(bg=overall_bg_color)
    btc_label.grid(column=0, row=0)

    # btc entry box setup
    btc_entry = tkinter.Entry(root, width=10)
    btc_entry.grid(column=1, row=0)

    # eth label setup
    eth_label = tkinter.Label(root, text="ETH:")
    eth_label.configure(bg=overall_bg_color)
    eth_label.grid(column=2, row=0)

    # etc entry box setup
    eth_entry = tkinter.Entry(root, width=10)
    eth_entry.grid(column=3, row=0)

    # conversion button setup, created on MacOS so PC viewers may see this GUI differently
    convert_button = tkinter.Button(root, text="Convert Currency", command=calculate_exchange)
    convert_button.configure(highlightbackground=convert_btn_color, width=15)
    convert_button.grid(column=4, row=0, padx=5, pady=7.5)

    # bnb label setup
    bnb_label = tkinter.Label(root, text="BNB:")
    bnb_label.configure(bg=overall_bg_color)
    bnb_label.grid(column=0, row=1)

    # bnb entry box setup
    bnb_entry = tkinter.Entry(root, width=10)
    bnb_entry.grid(column=1, row=1)

    # xrp label setup
    xrp_label = tkinter.Label(root, text="XRP:")
    xrp_label.configure(bg=overall_bg_color)
    xrp_label.grid(column=2, row=1)

    # xrp entry box setup
    xrp_entry = tkinter.Entry(root, width=10)
    xrp_entry.grid(column=3, row=1)

    # exit/quit button set up. Once again, create on MacOS so this may be visibly different to PC users.
    exit_button = tkinter.Button(root, text="Close Converter", command=close_application)
    exit_button.configure(highlightbackground=exit_btn_color, width=15)
    exit_button.grid(column=4, row=1, padx=5, pady=7.5)

    root.mainloop()

# If response not found, this is printed and application is over
else:
    print("There was an unexpected issue, please check URL and key!")
