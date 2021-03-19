def GenerateConfig(context):
    resources = []

    chains = ['matic']
    entity_types = ['blocks', 'transactions', 'logs', 'token_transfers', 'traces', 'contracts', 'tokens']

    for chain in chains:
        topic_name_prefix = 'crypto_' + chain
        subscription_name_prefix = 'crypto_' + chain + '.dataflow.bigquery'
        # 7 days
        message_retention_duration = '604800s'

        for entity_type in entity_types:
            topic_name = topic_name_prefix + '.' + entity_type
            topic_resource_name = topic_name.replace('.', '-')
            subscription_name = subscription_name_prefix + '.' + entity_type
            subscription_resource_name = subscription_name.replace('.', '-')
            resources.append({
                'name': topic_resource_name,
                'type': 'pubsub.v1.topic',
                'properties': {
                    'topic': topic_name
                }
            })
            resources.append({
                'name': subscription_resource_name,
                'type': 'pubsub.v1.subscription',
                'properties': {
                    'subscription': subscription_name,
                    'topic': '$(ref.' + topic_resource_name + '.name)',
                    'ackDeadlineSeconds': 30,
                    'retainAckedMessages': True,
                    'messageRetentionDuration': message_retention_duration,
                    'expirationPolicy': {
                    }
                }
            })

    return {'resources': resources}
