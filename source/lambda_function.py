import json
import backlog
import util
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(event)
    body = json.loads(event['body'])
    try:
        main(body)
        return {
            'statusCode': 200,
            'body': json.dumps('successfully')
        }
    except Exception as e:
        logging.exception("An error occurred: %s", str(e))
        return {
            'statusCode': 500,
            'body': str(e)
        }


def main(webhook_data):
    api_key = util.get_parameter_value('/backlog/api_key')
    project_id = util.get_parameter_value('/backlog/project_id')
    ticket_manager = backlog.BacklogTicketManager(api_key, project_id)

    state = webhook_data.get('state')
    if state == 'ACTIVATED':
        activate_issue(webhook_data, ticket_manager)
    elif state == 'CLOSED':
        close_issue(webhook_data, ticket_manager)
    else:
        logger.info(f'unsupported state. state:{state}')


def activate_issue(webhook_data, ticket_manager):
    activate_time = util.convert_timestamp_to_jst_iso(webhook_data.get('activatedAt'))
    description = f'''
    NrAccount: {webhook_data.get('tagAccount', [''])[0]}
    Time: {activate_time}
    Resource: {webhook_data.get('alertFacet', [''])[0]}
    AlertConditionName: {webhook_data.get('alertConditionNames', [''])[0]}
    nrqlQuery: {webhook_data.get('nrqlQuery', [''])[0]}
    issueUrl: {webhook_data.get('issueUrl')}
    policyUrl: {webhook_data.get('policyUrl')}
    violationChartUrl: {webhook_data.get('violationChartUrl')}
    issueId: {webhook_data.get('id')}
    '''

    payload = {
        'summary': f"NewRelic: [{webhook_data.get('tagAccount')}] {webhook_data.get('title')}",
        'description': description,
        'customField_NrIssueId': webhook_data.get('id')
    }
    create_response = ticket_manager.create_ticket(payload)

    if create_response.status == 201:
        logger.info('created ticket.')
    else:
        logger.erro(f'failed to create ticket. res:{create_response}')


def close_issue(webhook_data, ticket_manager):

    filter = {
        'summary': f"NewRelic: [{webhook_data.get('tagAccount')}] {webhook_data.get('title')}",
        'statusId': 1  # Open
    }
    search_result = ticket_manager.search_tickets(filter)
    if not search_result or 'issues' not in search_result:
        logger.info('ticket not found.')
        return
    ticket_id = search_result['issues'][0]['id']

    status_id = 2  # Close
    update_response = ticket_manager.update_ticket_status(ticket_id, status_id)

    if update_response.status == 200:
        logger.info('updated ticket status.')
    else:
        logger.error(f'failed to update ticket status. res:{update_response}')

    comment_content = 'This is a new comment.'
    comment_response = ticket_manager.add_comment_to_ticket(ticket_id, comment_content)

    if comment_response.status == 201:
        logger.info('added comment.')
    else:
        logger.error(f'failed to add comment. res:{comment_response}')
