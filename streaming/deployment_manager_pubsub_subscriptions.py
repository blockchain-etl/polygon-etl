def GenerateConfig(context):
    resources = []

    chains = ['crypto_matic']
    entity_types = ['blocks', 'transactions', 'logs', 'token_transfers', 'traces', 'contracts', 'tokens']


    topics_project = context.properties['topics_project']
    if topics_project is None:
        topics_project = context.env['project']

    for chain in chains:
        topic_name_prefix = chain
        subscription_name_prefix = chain + '.dataflow.bigquery'
        # 7 days
        message_retention_duration = '604800s'

        for entity_type in entity_types:
            topic_name = topic_name_prefix + '.' + entity_type
            topic_full_name = f'projects/{topics_project}/topics/{topic_name}'
            subscription_name = subscription_name_prefix + '.' + entity_type
            subscription_resource_name = subscription_name.replace('.', '-')
            resources.append({
                'name': subscription_resource_name,
                'type': 'pubsub.v1.subscription',
                'properties': {
                    'subscription': subscription_name,
                    'topic': topic_full_name,
                    'ackDeadlineSeconds': 30,
                    'retainAckedMessages': True,
                    'messageRetentionDuration': message_retention_duration,
                    'expirationPolicy': {
                    }
                }
            })

    return {'resources': resources}
