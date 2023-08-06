
## FX Rates from openexchangerates.org

import logging
logger = logging.getLogger(__name__)

import pandas as pd
import json
import os
import argparse
import ast
from datetime import datetime

######## openexchangerates app_id
app_id = os.environ.get("OPENEXCHANGERATES_APP_ID") #get from environment variable if set
#else get from the config.json file
if not app_id:
    from pkg_resources import Requirement, resource_filename
    myconfig = resource_filename(Requirement.parse("portia_fxrates"),"config.json")
    try:
        with open(myconfig, 'r') as f:
            fxconf = json.load(f)
            app_id = fxconf['OPENEXCHANGERATES_APP_ID'] 
    except FileNotFoundError as e:
        print ("Please enter your Openexchangerates.org App ID:")
        app_id = input()
        config = {'OPENEXCHANGERATES_APP_ID': app_id}
        with open(myconfig, 'w') as f:
            json.dump(config, f)
        #logger.error("Please rename config.json.example to config.json and add your openexhangerates app_id")
    except Exception as e:
        logger.error("Error: {}\nPlease either\n* add openexchangerates app_id to {} or\n* Set 'OPENEXCHANGERATES_APP_ID'  environment variable.".format(e, myconfig))

#settings for pandas display
#pd.set_option('display.max_rows', 500)

#open FX Rates
baseurl = "http://openexchangerates.org/api"


def getFX(currlist=None, cobdate = None):
    """
    Returns pandas dataframe with FX rates against USD.
    If cobdate is passed historical rates are returned, otherwise the current rates.
    
    param: currlist: list of ISO currencies
    type: currlist: list
    
    param: cobdate: date for which historical dates are requested in the format YYYYMMDD
    type: cobdate: int or string
    
    returns: pandas.DataFrame: with exchange rates
    """
    if cobdate is None:
        endpoint = "/latest.json?app_id=" + app_id
        cobdate = datetime.strftime(datetime.today(), '%Y%m%d')
    else:
        mycobdate = str(cobdate)
        mycobdate = "-".join([mycobdate[:4], mycobdate[4:6], mycobdate[6:8]])
        endpoint = "/historical/" + mycobdate + ".json?app_id=" + app_id
    url = baseurl + endpoint   
    logger.info("Getting FX rates from: {}".format(url))
    df = pd.read_json(url)
    df = df[["base", "rates", "timestamp"]]
    if currlist is not None:
        df = df.loc[currlist]
    df = df.reset_index()
    df = df.rename(columns={'index': 'CURR'})
    df = df.set_index('CURR')
    df['cobdate'] = cobdate
    logger.info("FX Rates: ".format(df.to_string(index=False)))
    return df



if __name__ == '__main__':  
    
    parser = argparse.ArgumentParser(description="FX Rates from OpenExchangerates.org")
    parser.add_argument("-curr", "--currlist", help="Currencylist in list format ['EUR', 'CHF'] ", type=ast.literal_eval)
    args = parser.parse_args()
    fx = getFX(args.currlist)
    fx.to_clipboard(index=False)
    print(fx.to_string(index=False))