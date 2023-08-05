#!/usr/bin/env python

import os
from release_note_generator.release_note_generator import ReleaseNoteGenerator
from release_note_generator.services import ReleaseNotesFormatter

token = os.getenv('GITHUB_API_TOKEN')
if not token:
    print('ERROR: GITHUB_API_TOKEN must be set in the environment.')
else:
    # repos of interest:
    # wet_arms
    # auto_pipeline
    # wetlab-ops
    repository_name = "auto_pipeline"

    notes = ReleaseNoteGenerator(token, repository_name=repository_name).release_notes()
    ReleaseNotesFormatter.output(notes)
