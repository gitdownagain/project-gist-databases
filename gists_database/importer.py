import requests

# https://learn.rmotr.com/python/base-python-track/database-handling/python-and-sqlite
# 3:52
# NAMED PARAMETERS 26:00

INSERT_GIST_QUERY = """INSERT INTO gists (
    "github_id", "html_url", "git_pull_url",
    "git_push_url", "commits_url",
    "forks_url", "public", "created_at",
    "updated_at", "comments", "comments_url"
) VALUES (
    :github_id, :html_url, :git_pull_url,
    :git_push_url, :commits_url, :forks_url,
    :public, :created_at, :updated_at,
    :comments, :comments_url
);"""

def import_gists_to_database(db, username, commit=True):
    # The INSERT INTO statement is used to insert new records in a table.
    # The first way specifies both the column names and the values to be inserted

    resp = requests.get('https://api.github.com/users/{username}/gists'.format(username=username))
    resp.raise_for_status()
    
    gists_data = resp.json()
    for gist in gists_data:
        params = {
            "github_id": gist['id'],
            "html_url": gist['html_url'],
            "git_pull_url": gist['git_pull_url'],
            "git_push_url": gist['git_push_url'],
            "commits_url": gist['commits_url'],
            "forks_url": gist['forks_url'],
            "public": gist['public'],
            "created_at": gist['created_at'],
            "updated_at": gist['updated_at'],
            "comments": gist['comments'],
            "comments_url": gist['comments_url'],
        }
        
        # straight from 25:00 in the video: https://learn.rmotr.com/python/base-python-track/database-handling/python-and-sqlite
        db.execute(INSERT_GIST_QUERY, params)
        if commit:
            db.commit()