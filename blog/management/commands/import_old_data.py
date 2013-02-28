import re

from django.core.management.base import BaseCommand, CommandError

para_re = re.compile('<[pP]>.*</[pP]>')

class Command(BaseCommand):
    """Import data from old site db. Hopefully nobody ever needs to run or look at this again."""

    def handle(self, *args, **options):
        from django.template.defaultfilters import slugify

        from blog.models import Post, Category

        import MySQLdb
        import markdown
        from datetime import datetime

        for category_title in ('News', 'Rants', 'Projects', 'Tips and Tricks', 'Misc',):
            category, created = Category.objects.get_or_create(title=category_title,
                                    slug=slugify(category_title),
                                    frontpage=True)

        db=MySQLdb.connect(user="root", passwd="password",db="dbname")
        c = db.cursor()


        c.execute("""select a.nid, a.title, a.created,
                     b.entity_id, b.body_value, b.body_format from node a, field_data_body b
                     where a.nid=b.entity_id""")

        for row in c.fetchall():
            nid, title, created, entity_id, body_value, body_format = row
            body_value = body_value.decode('cp1252')
            title = title.decode('cp1252')
            if body_format == 'plain_text':
                body_value = markdown.markdown(body_value)
            else:
                lines = []
                for line in body_value.split('\n'):
                    line = line.strip()
                    if line and not para_re.match(line):
                        line = "<p>%s</p>" % line
                    lines.append(line)
                body_value = '\n'.join(lines)

            post = Post.objects.create(
                        title=title,
                        slug=slugify(title)[:30],
                        date=datetime.fromtimestamp(created),
                        body=body_value,
                        published=True,
                        category=category
                        )

