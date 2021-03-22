def GenerateConfig(context):
    resources = []

    chains = ['crypto_matic']
    entity_types = ['blocks', 'transactions', 'logs', 'token_transfers', 'traces', 'contracts', 'tokens']

    for chain in chains:
        topic_name_prefix = chain

        for entity_type in entity_types:
            topic_name = topic_name_prefix + '.' + entity_type
            topic_resource_name = topic_name.replace('.', '-')
            resources.append({
                'name': topic_resource_name,
                'type': 'pubsub.v1.topic',
                'properties': {
                    'topic': topic_name
                }
            })

    return {'resources': resources}


