from slackclient import SlackClient
from google_sheets import GoogleSheets
from datetime import datetime
import time
import sys


class Slack:

    def __init__(self):
        self.token = 'xoxp-185515669264-199828799040-278419184210-9f16965b9abba9335abe137d67065540'
        self.user = 'USLACKBOT'
        self.slack_client = SlackClient(self.token)
        self.api_call = self.slack_client.api_call("im.list")

    def send_message(self, channel, message, as_bot=True):
        self.slack_client.api_call('chat.postMessage', link_names=1, channel=channel, text=message,
                                   as_user=not as_bot, icon_emoji=':robot_face:', username='The Better Manager')


class GoogleParser:

    def __init__(self, slack, debug_mode=False):
        self.slack = slack
        self.debug_mode = debug_mode
        self.gs = GoogleSheets(CLIENT_SECRET_FILE='google_drive_client_secret.json')
        self.gs.set_document('1RVZg7PoqMS0ON-fg1QjfnY5LRczQSS_jsxrZrCEu6lA')
        self.range_testing = self.gs.read_range('Testing Statuses', 'A1', 'L')
        self.range_milestones = self.gs.read_range('Milestones From Form', 'A1', 'L')
        self.range_common = self.gs.read_range('Milestones', 'A1', 'ZZ')
        self.managers = {}
        self.channels = {}
        self.parse_managers()

    def parse_managers(self):
        row_projects = self.range_common[6]
        row_channels = self.range_common[7]
        row_slacks = self.range_common[8]
        for i, project in enumerate(row_projects):
            if not project:
                continue
            self.channels[project] = row_channels[i]
            self.managers[project] = row_slacks[i]

    def get_slack_manager_of_project(self, project):
        return self.managers[project] if not self.debug_mode else 'volodar'

    def get_slack_channel_of_project(self, project):
        return self.channels[project] if not self.debug_mode else 'volodar'

    def get_slack_channel_general(self):
        return '#general' if not self.debug_mode else '@volodar'

    @staticmethod
    def get_header(range):
        header = range[0]
        range = range[1:]
        return header, range

    @staticmethod
    def get_value(header, row, name):
        index = header.index(name)
        return row[index]

    def send_notification_testing_status(self, header, row, message):
        status = GoogleParser.get_value(header, row, 'Status')
        project = GoogleParser.get_value(header, row, 'Project Name')
        manager = self.get_slack_manager_of_project(project)
        channel = self.get_slack_channel_of_project(project)
        slack_message = '```*{}: {}* ({}) Manager - @{}```'.format(project, message, status, manager)
        self.slack.send_message(channel, slack_message)
        self.slack.send_message(self.get_slack_channel_general(), slack_message)

    def warning_testing_statuses(self):
        header, range = GoogleParser.get_header(self.range_testing)
        for row in range:
            project = GoogleParser.get_value(header, row, 'Project Name')
            if not project:
                continue
            status = GoogleParser.get_value(header, row, 'Status')
            if status == 'Approve':
                self.send_notification_testing_status(header, row, 'Send build to store/customer')
            elif status == 'Disapprove':
                self.send_notification_testing_status(header, row, 'SNeed dispatch disapprove')

    def warning_milestones(self):
        header, range = GoogleParser.get_header(self.range_milestones)
        for row in range:
            project = GoogleParser.get_value(header, row, 'Project')
            if not project:
                continue
            status = GoogleParser.get_value(header, row, 'Status')
            if status in ['Release', 'Done', 'Moved']:
                continue
            finish_date = GoogleParser.get_value(header, row, 'Date')
            finish_time = time.mktime(datetime.strptime(finish_date, "%m/%d/%Y").timetuple())
            now = datetime.now()
            now_date = '{}/{}/{}'.format(now.month, now.day, now.year)
            now_time = time.mktime(datetime.strptime(now_date, "%m/%d/%Y").timetuple())

            overdue = now_time > finish_time
            if overdue:
                manager = self.get_slack_manager_of_project(project)
                channel = self.get_slack_channel_of_project(project)
                comment = GoogleParser.get_value(header, row, 'Description').encode('utf-8')
                slack_message = '```Overdue Milestone: *{}* Date of release: {}, Manager @{}\nDescription:\n{}```'.\
                    format(project, finish_date, manager, comment)
                self.slack.send_message(channel, slack_message)
                self.slack.send_message(self.get_slack_channel_general(), slack_message)

    def notify_about_milestones(self):
        header, range = GoogleParser.get_header(self.range_milestones)
        for row in range:
            project = GoogleParser.get_value(header, row, 'Project')
            if not project:
                continue
            status = GoogleParser.get_value(header, row, 'Status')
            if status in ['Release', 'Done']:
                continue
            finish_date = GoogleParser.get_value(header, row, 'Date')
            manager = self.get_slack_manager_of_project(project)
            comment = GoogleParser.get_value(header, row, 'Description').encode('utf-8')
            channel = self.get_slack_channel_of_project(project)
            self.slack.send_message(channel,
                                    '```Notify: *{}* Date of milestone: {}, Manager @{}\nDescription:\n{}```'.
                                    format(project, finish_date, manager, comment))


def run(event, debug_mode=False):
    g = GoogleParser(Slack(), debug_mode)
    if event == 'hour':
        g.warning_testing_statuses()
        g.warning_milestones()
    elif event == 'daily':
        g.notify_about_milestones()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        event = sys.argv[1]
    else:
        event = 'hour'
    run(event)
