# tutti-crawler

## fork
This fork includes aws lambda functions and api definitions which can be used with a telegram bot. Because it is so far only intended to be for a small audience efficientcy will only be implemented later on

### api
`curl -o tutti.json -H "X-Tutti-Hash: "a275c2cc-8f54-4444-87a1-8b743dc868d4"" https://api.tutti.ch/v10/list.json?limit=30&o=1&region=4&sp=1&with_all_regions=true`

## Setup
1. `lambda_function.py` is a aws lambda function for it to work a Telegram bot is required and messages need to be forwarded to this function by aws API Gateway. For the setup you can consult `https://dev.to/nqcm/-building-a-telegram-bot-with-aws-api-gateway-and-aws-lambda-27fg` a Telegram webhook should be placed to point to your aws gateway. The Telegramm bot key must be submitted to the function by a enviromental variable named `TELEGRAM_TOKEN`
2. Creatte a dynamodb table named "Tutti" and add a first item to the table by running `dynamodb_setup.py`
3. create a Cloudwatch event to call the function e.g. every 15 minutes. Setting Webhooks

So now we have a secure URL which is connected to our code living in a cloud function. Cool! We can go ahead and tell Telegram to send any future messages received by our bot to this address.

Setting a webhook is as simple as typing the following in your browser and hitting enter. (Make sure to substitute the place holder text)

"https://api.telegram.org/bot<your-bot-token>/setWebHook?url=<your-API-invoke-URL>"

You will get a confirmation message from Telegram and from now on any messages sent to your bot will be pushed to this URL.
Adding code to Lambda function

Go ahead and try sending a message from your own Telegram account to the bot.