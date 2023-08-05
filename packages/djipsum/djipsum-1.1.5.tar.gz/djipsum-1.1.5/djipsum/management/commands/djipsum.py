from __future__ import absolute_import

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError

import sys
from djipsum import __VERSION__
from djipsum.fields import DjipsumFields


class Command(BaseCommand):
    help = 'To generate awesome lorem ipsum for your model!'

    def add_arguments(self, parser):
        parser.add_argument(
            '-dv',
            '--djipsum_version',
            action='store_true',
            help='Show djipsum version number and exit.'
        )
        parser.add_argument(
            '-auto',
            '--auto_gen',
            action='store_true',
            help='Automatic generate lorem ipsum from custom generator class.'
        )
        parser.add_argument(
            '-cg',
            '--custom_generator',
            help='Custom a function generator (full path) for auto-gen.'
        )
        parser.add_argument(
            '--app',
            help='The app name.'
        )
        parser.add_argument(
            '--model',
            help='The model class name.'
        )
        parser.add_argument(
            '--max',
            type=int,
            default=10,
            help='Maximum generate lorem ipsum.'
        )

    def handle(self, *args, **options):
        auto_gen = options['auto_gen']
        custom_generator = options['custom_generator']
        app = options['app']
        model = options['model']
        maximum = options['max']

        if auto_gen and custom_generator:
            components = custom_generator.split('.')
            func_name = components[-1]
            try:
                mod = __import__('.'.join(components[:-1]), fromlist=[func_name])
                generate_cst_faker = getattr(mod, func_name)
                self.stdout.write(
                    self.style.SUCCESS(
                        generate_cst_faker(maximum=maximum)
                    )
                )
                sys.exit()
            except Exception as e:
                raise CommandError(e)

        elif options['djipsum_version']:
            return __VERSION__
        elif app == None:
            return self.print_help('djipsum', '-h')
        try:
            model_class = apps.get_model(app_label=app, model_name=model)
        except Exception as e:
            raise CommandError(e)

        exclude = ['pk', 'id', 'objects']
        # removing `model_class._meta.fields` to `model_class._meta.get_fields()
        # to get all fields.`
        # Ref: http://stackoverflow.com/a/3106314/6396981
        fields = [
            {'field_type': f.__class__.__name__, 'field_name': f.name}
            for f in model_class._meta.get_fields() if f.name not in exclude
        ]
        validated_model_fields = DjipsumFields(
            model_class,
            fields,
            maximum
        ).create_validated_fields()

        def loremInfo():
            return """\n[+] Successfully generate the lorem ipsum for `{0}`\n\n{1}\n""".format(
                model_class,
                validated_model_fields
            )

        self.stdout.write(
            self.style.SUCCESS(
                loremInfo()
            )
        )
