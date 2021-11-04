from discord_webhook import DiscordWebhook, DiscordEmbed


def publish_message_to_discord(webhook_url, content, embed=None, embed_fields=None):
    webhook = DiscordWebhook(url=webhook_url, content=content)

    if embed is not None:
        embed = DiscordEmbed(
            title=embed.get('title'),
            description=embed.get('description'),
            url=embed.get('url'),
            color=embed.get('color'),
        )
        if embed_fields:
            for embed_field in embed_fields:
                embed.add_embed_field(
                    name=embed_field.get('name'),
                    value=embed_field.get('value'),
                )
        webhook.add_embed(embed)

    response = webhook.execute()
    return response
