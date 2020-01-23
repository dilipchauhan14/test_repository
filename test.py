import requests
from static_variables import *


def fetch_data_from_github_api(url):
    token = 'ac08edcd81da07a1e5cfa1904dd44aa6de63f3b4'
    headers = {'Authorization': 'token ' + token}
    response = requests.get(url=url, headers=headers)
    response_in_json = response.json()

    return response_in_json


def fetch_pr_reviewers(review_url):
    reviews_data = fetch_data_from_github_api(review_url)
    unique_reviewers = set()
    for review in reviews_data:
        unique_reviewers.add(review[USER][LOGIN])
    reviewers = []
    for reviewer in unique_reviewers:
        user = {USER: reviewer}
        reviewers.append(user)
    return reviewers


def fetch_pr_commits(commits_url):
    commits_data = fetch_data_from_github_api(commits_url)
    commits = []
    for commit_data in commits_data:
        commit = {SHA: commit_data[SHA], COMMITED_AT: commit_data[COMMIT][AUTHOR][DATE]}
        if commit_data[AUTHOR] is None:
            commit[AUTHOR] = commit_data[COMMIT][AUTHOR][NAME]
        else:
            commit[AUTHOR] = commit_data[AUTHOR][LOGIN]
        commits.append(commit)

    return commits


def fetch_pr_comments(pr_url):
    review_comments = fetch_review_comments(pr_url + "/" + REVIEWS)
    line_comments = fetch_line_comments(pr_url + "/" + COMMENTS)
    comments = review_comments + line_comments
    return comments


def fetch_review_comments(url):
    reviews = fetch_data_from_github_api(url)

    review_comments = []
    for review in reviews:
        if review[BODY] and review[STATE] != PENDING:
            value = {USER: review[USER][LOGIN], BODY: review[BODY], SUBMITTED_AT: review[SUBMITTED_AT]}
            review_comments.append(value)

    return review_comments


def fetch_line_comments(url):
    comments = fetch_data_from_github_api(url)
    line_comments = []
    for comment in comments:
        value = {USER: comment[USER][LOGIN], BODY: comment[BODY], SUBMITTED_AT: comment[UPDATED_AT]}
        line_comments.append(value)

    return line_comments


def get_changed_files(merge_commit_url):
    merge_commit_data = fetch_data_from_github_api(merge_commit_url)
    files_changed = []
    for file in merge_commit_data[FILES]:
        entry = {FILENAME: file[FILENAME], STATUS: file[STATUS], ADDITIONS: file[ADDITIONS], DELETIONS: file[DELETIONS]}
        files_changed.append(entry)

    return files_changed


def get_requested_reviewers(requested_reviewers):
    output = []
    for reviewer in requested_reviewers:
        user = {USER: reviewer[LOGIN]}
        output.append(user)
    return output


def get_merged_by(merged_by):
    if merged_by is None:
        return None
    else:
        return merged_by[LOGIN]
