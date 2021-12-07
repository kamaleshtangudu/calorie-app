"""Command for creating super-user."""
import os
import pandas as pd
from pandas.errors import ParserError

from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    """Finds untraslated strings"""

    def add_arguments(self, parser):
        parser.add_argument('--csv', type=str, required=True)
        parser.add_argument('--locale', type=str, required=True)

    def preprocessing(self, data):
        data_frame = pd.DataFrame(columns=['English', 'Spanish'])
        for row in data.iterrows():
            data_frame = data_frame.append(
                {'English': f"msgid \"{row[1][0]}\"", 'Spanish': f"msgstr \"{row[1][1]}\""},
                ignore_index=True
            )
        return data_frame

    def get_translated_text(self, file, data):
        with open(file) as f:
            lines = f.readlines()
            translated_txt = lines[:20]

            self.stdout.write("Following Strings are translated:")

            for line_number in range(20, len(lines)):
                line = lines[line_number]

                if line[0] == '#' or line[:-1] == '': #skip lines which are not useful
                    translated_txt.append(line)

                elif line[:5] == 'msgid':
                    msgid = line[7:-2] #actual string inside the quotes
                    translated_txt.append(line)

                    line_number += 1 #process from next line till msgstr
                    while(lines[line_number][:6] != 'msgstr'):
                        msgid = msgid + str(lines[line_number][1:-2])
                        translated_txt.append(lines[line_number])
                        line_number += 1

                elif line[:6] == 'msgstr': #starts with `msgstr`
                    msgstr = line[8:-2] #actual string inside the quotes

                    line_number += 1 #process from next line till '\n'
                    while(line_number < len(lines) and lines[line_number] != '\n'):
                        msgstr = msgstr + str(lines[line_number][1:-2])
                        line_number += 1

                    if msgstr == '':  #if translation is not available
                        msgid = 'msgid "' + msgid + '"'

                        try:
                            translated_txt.append(data.loc[data.English == msgid]['Spanish'].values[0]+'\n')
                            self.stdout.write(msgid[7:-1]) #print string to show this string is translated
                        except IndexError:
                            #translation is not available for this string
                            translated_txt.append('msgstr ""\n')
                    else:
                        translated_txt.append(f'msgstr "{msgstr}"\n')

        return translated_txt

    def get_file_path(self, locale):
        locale = locale.replace('-', '_')
        for path in settings.LOCALE_PATHS:
            file_path = os.path.join(path, locale, 'LC_MESSAGES', 'django.po')
            if os.path.exists(file_path):
                return file_path

        self.stdout.write(
            self.style.ERROR(f"Can not find translation files for {locale}. "
                             "Run `python manage.py makemessages` first")
        )
        return None

    def handle(self, *args, **options):
        """
        Prints untranslated strings
        """

        translated_csv = options.get('csv')
        locale = options.get('locale')
        file_path = self.get_file_path(locale)

        if not file_path:
            return

        try:
            data = pd.read_csv(translated_csv)
        except FileNotFoundError as error:
            self.stdout.write(self.style.ERROR(str(error)))
            return
        except ParserError as error:
            self.stdout.write(self.style.ERROR("Please provide a valid csv file."))
            return

        data = self.preprocessing(data)
        translated_txt = self.get_translated_text(file_path, data)

        # Rewriting the translation file
        with open(file_path, "w") as f:
            for line in translated_txt:
                f.write(line)