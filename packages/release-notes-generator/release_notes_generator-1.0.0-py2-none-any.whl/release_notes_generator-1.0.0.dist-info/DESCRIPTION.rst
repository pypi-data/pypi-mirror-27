# Usage
Modify the repository_name on line 189 to be one of the commented options (could be any LIMS repository though) and will output to the console release notes of the following form:
```
    h2. SOME TITLE
    CHANGE_TYPE: UI
    DESCRIPTION: Some descriptions
    JIRA TICKET: LIMS-123
    PULL REQUEST: 123
    RISK: LOW
    RISK DESCRIPTION: Some description
```

You will also need to set your github access token:
`export GITHUB_API_TOKEN = <token>`

Then run the script:
`python cli.py`

Optionally redirect to a file:
`python cli.py > release_notes.txt`

# How this Works
You can look at `cli.py` for an example of how to use this script. The name is a bit misleading as it isn't yet a cli app at all (yet).

Essentially, `cli.py` runs the following where the token variable is looking for `GITHUB_API_TOKEN` to be set.

```python
ReleaseNoteGenerator(token, repository_name=repository_name).release_notes()
ReleaseNotesFormatter.output(notes)
```

`ReleaseNoteGenerator` parses the PR numbers from the latest release, if no release exists it will return nothing. It then passes the PR numbers to the pr fetcher which grabs the descriptions. A good entry point it to look at `ReleaseNoteGenerator.release_notes`

# Future Work
This is a quick and dirty initial implementation and we should expand this for easy reuse.

Iteration 1: Packaging and Interface Features
- command line interaction to run with a repository_name arg
```
# print output to the screen
release_notes auto_pipeline --print
```

- test suite
- packaging for easy pip install and use across LIMS projects (ie. use in individual release scripts)
- document API

Iteration 2: Granularity and Robustness Features
- expose the PRFetcher so that we are not coupled to fetching the initial list purely from
- add ability to diff the latest release and previous release and auto generate pr numbers (is this in the ARMS release script?)
- auto generate tag and release adding the PRs to the release notes

Other Features:
- auto ignore markdown comments
- filter out heading fields in the description and only parse the one line description
- include full pull request links


