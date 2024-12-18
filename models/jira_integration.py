from jira import JIRA

class JiraIntegration:
    def __init__(self, jira_url, jira_user, jira_api_token):
        self.jira = JIRA(server=jira_url, basic_auth=(jira_user, jira_api_token))

    def create_task(self, project_key, summary, description):
        issue_dict = {
            'project': {'key': project_key},
            'summary': summary,
            'description': description,
            'issuetype': {'name': 'Task'},
        }
        return self.jira.create_issue(fields=issue_dict)
