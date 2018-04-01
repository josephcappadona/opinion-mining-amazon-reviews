import gzip
import time

from django.core.management.base import BaseCommand, CommandError
from amazonapp.models import Category, Product

class Command(BaseCommand):
    help = 'Imports metadata'

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='+', type=str)

    def handle(self, *args, **options):
        def is_valid(meta_dict):
            required = ['asin', 'title', 'imUrl']
            return all(key in meta_dict for key in required)
        
        invalid_rows = []

        for filename in options['filename']:
            count = 0
            for prod_meta in self.get_metadata_lines(filename):
                if count % 10 == 0:
                    print('Processed %d products' % count)

                if not is_valid(prod_meta):
                    invalid_rows.append(prod_meta)
                else:
                    categories = self.create_categories(prod_meta['categories'])

                    product, was_created = Product.objects.get_or_create(
                        id=prod_meta['asin'],
                        title=prod_meta['title'],
                        description=prod_meta.get('description', ''),
                        image_url=prod_meta['imUrl'],
                    )
                    for category in categories:
                        product.categories.add(category)
                    count += 1

        # Write down invalid rows
        self.save_invalid_rows(invalid_rows)

    def get_metadata_lines(self, filename):
        with gzip.open(filename, 'r') as f:
            for line in f:
                meta = eval(line)
                if meta:
                    yield meta


    def create_categories(self, categories):
        """Categories: ['Electronics', 'Computers & Accessories', ...]
        """
        return [(Category.objects.get_or_create(name=name))[0] for name in categories]

    def save_invalid_rows(self, invalid_rows):
        current_time = time.time()
        with open('invalid_rows_%d' % current_time) as f:
            for row in invalid_rows:
                f.write(json.dumps(row))
