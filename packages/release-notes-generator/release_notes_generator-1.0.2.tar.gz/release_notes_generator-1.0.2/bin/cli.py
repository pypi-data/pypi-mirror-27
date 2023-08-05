import os
from release_note_generator import ReleaseNoteGenerator
from release_note_generator.services import ReleaseNotesFormatter

token = os.getenv('GITHUB_API_TOKEN')
# repos of interest:
# wet_arms
# auto_pipeline
# wetlab-ops
repository_name = "auto_pipeline"

notes = ReleaseNoteGenerator(token, repository_name=repository_name).release_notes()
ReleaseNotesFormatter.output(notes)
