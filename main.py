import time
import requests
import json
import csv
from discord_webhook import DiscordWebhook, DiscordEmbed
import threading
import argparse

colour_for_embed = 0x02ffec


def get_whale_data(row, event_type, offset_time):
    # Create a session for making HTTP requests
    s = requests.session()

    # Calculate the timestamp for the specified time offset
    final = int(time.time()) - offset_time

    # Construct the API URL with parameters
    url = f"https://api.opensea.io/api/v1/events?account_address={row['Addy']}&event_type={event_type}&only_opensea=false&offset=0&limit=15&occurred_after={final}"

    # Set the OpenSea API key in the headers
    headers = {"X-API-KEY": ""}

    # Make the GET request
    response = s.request("GET", url, headers=headers)

    # Parse the JSON response
    y = json.loads(response.text)

    # Return the asset events data
    return y['asset_events']


def create_embed(data, seller, link_seller, action_type):
    images, links, prices, names = [], [], [], []

    # Extract relevant information from the data
    for item in data:
        image = item['asset']['image_url']
        link = item['asset']['permalink']
        price = item['starting_price'] if action_type == 'listing' else item['total_price']
        name = item['asset']['name']
        actual_price = int(price) / 1000000000000000000
        actual_price2 = "ETH " + str(actual_price)

        images.append(image)
        links.append(link)
        prices.append(actual_price2)
        names.append(name)

    embeds = []

    # Create Discord embeds for each item
    for i in range(len(names)):
        embed = DiscordEmbed(title=f'{names[i]}', description='', url=links[i], color=colour_for_embed)
        embed.add_embed_field(name='User', value=f"[{seller}]({link_seller})", inline=False)
        embed.add_embed_field(name='Price', value=f"```css\n{prices[i]}```", inline=True)
        embed.add_embed_field(name='Action', value=f"```css\n{action_type.capitalize()}```", inline=True)
        embed.set_thumbnail(url=images[i])
        embed.set_footer(text="Whales Monitor")
        embeds.append(embed)

    return embeds


def whales_monitor(Threadname, Number, event_type, offset_time):
    while True:
        try:
            with open('settings.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)

                # Skip rows based on the thread number
                for _ in range(Number):
                    next(reader)
                row = next(reader)

                webhook = DiscordWebhook(url=row['Webhook'])

                whale_data = get_whale_data(row, event_type, offset_time)
                seller = whale_data[0]['seller']['user']['username']
                link_seller = "https://opensea.io/" + seller
                print(link_seller)

                embeds = create_embed(whale_data, seller, link_seller, event_type)

                # Send Discord webhooks for each embed
                for embed in embeds:
                    webhook.add_embed(embed)
                    response = webhook.execute()
                    response.connection.close()

                # Sleep based on the event type
                time.sleep(310 if event_type == 'created' else 312)
        except Exception as e:
            print(f"Exception found '{e}' - Nothing found! - {Threadname}")

            # Sleep on exception based on the event type
            time.sleep(310 if event_type == 'created' else 312)


def main():
    parser = argparse.ArgumentParser(description="Whales Monitor Script")

    # Add command-line arguments for choosing event type
    parser.add_argument('-l', '--listings', action='store_true', help='Run for new listings')
    parser.add_argument('-s', '--sales', action='store_true', help='Run for successful sales')
    args = parser.parse_args()

    try:
        threads = []
        event_type = 'created' if args.listings else 'successful'
        offset_time = 1000000 if args.listings else 300000

        # Create and start threads
        for i in range(1, 7):
            thread = threading.Thread(target=whales_monitor, args=(f"Whale {i}", i - 1, event_type, offset_time))
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

    except Exception as e:
        print("Error: unable to start thread", e)


if __name__ == "__main__":
    main()
