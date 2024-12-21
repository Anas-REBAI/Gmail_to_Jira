from jira import JIRA

class JiraIntegration:
    def __init__(self, jira_url, jira_user, jira_token):
        """Initialize the Jira client."""
        self.client = JIRA(server=jira_url, basic_auth=(jira_user, jira_token))

    def create_task(self, project_key, summary, description, priority):
        """Create a Jira task."""
        try:
            # Vérifiez si la priorité existe dans Jira
            available_priorities = {p.name: p.id for p in self.client.priorities()}
            if priority not in available_priorities:
                raise ValueError(f"Invalid priority '{priority}'. Available priorities: {', '.join(available_priorities.keys())}")

            # Création de l'issue
            issue_dict = {
                'project': {'key': project_key},
                'summary': summary,
                'description': description,
                'issuetype': {'name': 'Task'},
                'priority': {'id': available_priorities[priority]}
            }

            new_issue = self.client.create_issue(fields=issue_dict)
            print(f"Created Jira issue: {new_issue.key}")
            return new_issue
        except Exception as e:
            print(f"Error creating Jira task: {e}")
            return None
