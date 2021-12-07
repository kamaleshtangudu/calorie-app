"""Command for creating super-user."""
import os

from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    """Finds untraslated strings"""

    def handle(self, *args, **options):
        """
        Prints untranslated strings
        """

        for local_path in settings.LOCALE_PATHS:
            for language in os.listdir(local_path):
                if language[:2] != 'en': #skip english translations
                    file = os.path.join(local_path, language, 'LC_MESSAGES', 'django.po')
                    self.stdout.write(
                        self.style.ERROR(f"Following strings are not translated in {file}:")
                    )
                    with open(file) as f:
                        lines = f.readlines()
                        for line_number in range(18, len(lines)):
                            line = lines[line_number]
                            if line[:5] == 'msgid': #starts with `msgid`
                                msgid = line[7:-2] #actual string without quotes

                                line_number += 1 #process from next line till msgstr
                                while lines[line_number][:6] != 'msgstr':
                                    msgid = msgid + str(lines[line_number][1:-2])
                                    line_number += 1

                            elif line[:6] == 'msgstr': #starts with `msgstr`
                                msgstr = line[8:-2] #actual string without quotes

                                line_number += 1 #process from next line till '\n'
                                while(line_number < len(lines) and lines[line_number] != '\n'):
                                    msgstr = msgstr + str(lines[line_number][1:-2])
                                    line_number += 1

                                if msgstr == '':  #if translation is not available
                                    self.stdout.write(msgid)