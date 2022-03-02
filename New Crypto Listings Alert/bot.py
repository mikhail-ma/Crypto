import requests
from dateutil import parser
import json
import os.path
import time
from datetime import timedelta, datetime, date
from pathlib import Path
import pytz

# from loguru import logger


# request
def make_query(my_query):
    time.sleep(10)
    headers = {"X-API-KEY": "BQYVjT0kytbQ7MVtCISxinG5SbKWfUSd"}
    response = requests.post(
        "https://graphql.bitquery.io/", json={"query": my_query}, headers=headers
    )
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed and return code is " f"{response.status_code}.")


def query_ethereum():
    today = datetime.now(pytz.utc).strftime("%Y-%m-%d")
    query = '''query MyQuery {
      ethereum(network: ethereum) {
        arguments(
          smartContractAddress: {in: ["0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f", "0x1F98431c8aD98523631AE4a59f267346ea31F984"]}
          smartContractEvent: {is: "PairCreated"}
          argument: {not: "pair"}
          date: {is: "'''+today+'''"}
        ) {
          reference {
            address
            smartContract {
              currency {
                symbol
                name
              }
            }
          }
        }
      }
    }'''
    

    return query


def query_bsc():
    today = datetime.now(pytz.utc).strftime("%Y-%m-%d")
    query = '''query MyQuery {
      ethereum(network: bsc) {
        arguments(
          smartContractAddress: {in: ["0xBCfCcbde45cE874adCB698cC183deBcF17952812", "0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73"]}
          smartContractEvent: {is: "PairCreated"}
          argument: {not: "pair"}
          date: {is: "'''+ today+'''"}
          ) {
          reference {
            address
            smartContract {
              currency {
                symbol
                name
              }
          }
        }
      }
    }
    }'''

    return query


def get_tokens(platform):
    if platform == "eth":
        query = make_query(query_ethereum())
    elif platform == "bsc":
        query = make_query(query_bsc())
    else:
        raise ValueError()

    json1 = query["data"]["ethereum"]["arguments"]
    res = list()
    for i in json1:
        r = (
            i["reference"]["smartContract"]["currency"]["name"],
            i["reference"]["address"],
            platform,
        )

        if r[0] not in ("-", "Error in name", "Wrapped BNB", "BUSD Token"):
            res.append(r)

    return set(res)


def telegram_bot_sendtext(bot_message):

    bot_token = "5067292323:AAFWbZCe239IWKr6DE45GPiJPQGDVitmjPk"
    bot_chatID = "@DEXTokenListingAlerts"
    send_text = (
        "https://api.telegram.org/bot"
        + bot_token
        + "/sendMessage?chat_id="
        + bot_chatID
        + "&parse_mode=Markdown&text="
        + bot_message
        + "&disable_web_page_preview=True"
    )

    response = requests.get(send_text)


def main():
    if Path("df_base.json").exists():
        with open("df_base.json", "r") as f:
            file_content = f.read()
            if len(file_content) != 0:
                tokens = json.loads(file_content)
                tokens = [tuple(elem) for elem in tokens]
                tokens = set(tokens)
            else:
                tokens = set()
    else:
        tokens = set()

    while True:
      start = time.time()
      downloaded_tokens = set(get_tokens(platform="eth")).union(
          set(get_tokens(platform="bsc"))
      )
      new_tokens = tokens.difference(downloaded_tokens)
      tokens = downloaded_tokens
      with open("df_base.json", "w") as f:
          json.dump(list(tokens), f, indent=2)

      if len(new_tokens) > 0:
#          logger.info(new_tokens)
          for (token_name, token_address, token_platform) in new_tokens:
              if token_platform == "bsc":
                  bot_message = "🥞 New *PancakeSwap* Token: {} \n [address](https://bscscan.com/address/{}".format(
                      token_name, token_address
                  )
                  telegram_bot_sendtext(bot_message)
              else:
                  bot_message = "🦄 New *UniSwap* Token: {} \n [address](https://bscscan.com/address/{}".format(
                      token_name, token_address
                  )
                  telegram_bot_sendtext(bot_message)

      end = time.time()
      print("elapsed time:", end - start)
      time.sleep(100)


main()
