import os

DESTINATION = '~/mbs/'

REPOSITORY_URL = 'git@bitbucket.org:MaxiBookingTeam/maxibooking-hotel.git'

DESTINATION = os.path.expanduser('~/mbs')

SOURCE_DIRS = [
    'src', 'tests'
]
SOURCE_EXTENSIONS = [
    '.php', '.js', '.less', '.yml', '.twig', '.ts'
]
