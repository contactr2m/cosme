# Generated by Django 2.0.8 on 2018-10-30 21:44

import cosme.v1.atomic_elements.organisms
import cosme.v1.blocks
from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0003_menuitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPage',
            fields=[
                ('abstractfilterpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='v1.AbstractFilterPage')),
                ('content', wagtail.core.fields.StreamField([('full_width_text', wagtail.core.blocks.StreamBlock([('content_with_anchor', wagtail.core.blocks.StructBlock([('content_block', wagtail.core.blocks.RichTextBlock()), ('anchor_link', wagtail.core.blocks.StructBlock([('link_id', wagtail.core.blocks.CharBlock(help_text='\n            ID will be auto-generated on save.\n            However, you may enter some human-friendly text that\n            will be incorporated to make it easier to read.\n        ', label='ID for this content block', required=False))]))])), ('content', wagtail.core.blocks.RichTextBlock(icon='edit')), ('media', wagtail.images.blocks.ImageChooserBlock(icon='image')), ('quote', wagtail.core.blocks.StructBlock([('body', wagtail.core.blocks.TextBlock()), ('citation', wagtail.core.blocks.TextBlock(required=False)), ('is_large', wagtail.core.blocks.BooleanBlock(required=False))])), ('cta', wagtail.core.blocks.StructBlock([('slug_text', wagtail.core.blocks.CharBlock(required=False)), ('paragraph_text', wagtail.core.blocks.RichTextBlock(required=False)), ('button', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.CharBlock(required=False)), ('url', wagtail.core.blocks.CharBlock(default='/', required=False)), ('size', wagtail.core.blocks.ChoiceBlock(choices=[('regular', 'Regular'), ('large', 'Large Primary')]))]))])), ('related_links', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock(required=False)), ('paragraph', wagtail.core.blocks.RichTextBlock(required=False)), ('links', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.CharBlock(required=False)), ('url', wagtail.core.blocks.CharBlock(default='/', required=False))])))])), ('table', wagtail.core.blocks.StructBlock([('headers', wagtail.core.blocks.ListBlock(wagtail.core.blocks.CharBlock())), ('rows', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StreamBlock([('hyperlink', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.CharBlock(required=False)), ('url', wagtail.core.blocks.CharBlock(default='/', required=False))])), ('text', wagtail.core.blocks.CharBlock()), ('text_blob', wagtail.core.blocks.TextBlock()), ('rich_text_blob', wagtail.core.blocks.RichTextBlock())])))], editable=False)), ('table_block', cosme.v1.atomic_elements.organisms.AtomicTableBlock(table_options={'renderer': 'html'})), ('image_inset', wagtail.core.blocks.StructBlock([('image', wagtail.core.blocks.StructBlock([('upload', wagtail.images.blocks.ImageChooserBlock(required=False)), ('alt', wagtail.core.blocks.CharBlock(help_text="If the image is decorative (i.e., if a screenreader wouldn't have anything useful to say about it), leave the Alt field blank.", required=False))])), ('image_position', wagtail.core.blocks.ChoiceBlock(choices=[('right', 'right'), ('left', 'left')])), ('is_image_decorative', wagtail.core.blocks.BooleanBlock(label='Image decorative', required=False)), ('image_width', wagtail.core.blocks.ChoiceBlock(choices=[(170, '170px'), (270, '270px')], help_text='Default is 270px.', label='Image Width')), ('text', wagtail.core.blocks.RichTextBlock(required=False)), ('is_bottom_rule', wagtail.core.blocks.BooleanBlock(default=True, label='Bottom Rule', required=False))])), ('reusable_text', cosme.v1.blocks.ReusableTextChooserBlock('v1.ReusableText'))])), ('info_unit_group', wagtail.core.blocks.StructBlock([('format', wagtail.core.blocks.ChoiceBlock(choices=[('50-50', '50/50'), ('33-33-33', '33/33/33'), ('25-75', '25/75')], help_text='Choose the number and width of info unit columns.', label='Format')), ('heading', wagtail.core.blocks.StructBlock([('text', cosme.v1.blocks.HeadingTextBlock(required=False)), ('level', wagtail.core.blocks.ChoiceBlock(choices=[('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4')])), ('icon', cosme.v1.blocks.HeadingIconBlock(help_text='Input the name of an icon to appear to the left of the heading. E.g., approved, help-round, etc. <a href="https://cfpb.github.io/capital-framework/components/cf-icons/#icons">See full list of icons</a>', required=False))], required=False)), ('intro', wagtail.core.blocks.RichTextBlock(help_text='If this field is not empty, the Heading field must also be set.', required=False)), ('link_image_and_heading', wagtail.core.blocks.BooleanBlock(default=True, help_text="Check this to link all images and headings to the URL of the first link in their unit's list, if there is a link.", required=False)), ('has_top_rule_line', wagtail.core.blocks.BooleanBlock(default=False, help_text='Check this to add a horizontal rule line to top of info unit group.', required=False)), ('lines_between_items', wagtail.core.blocks.BooleanBlock(default=False, help_text='Check this to show horizontal rule lines between info units.', label='Show rule lines between items', required=False)), ('info_units', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('image', wagtail.core.blocks.StructBlock([('upload', wagtail.images.blocks.ImageChooserBlock(required=False)), ('alt', wagtail.core.blocks.CharBlock(help_text="If the image is decorative (i.e., if a screenreader wouldn't have anything useful to say about it), leave the Alt field blank.", required=False))])), ('heading', wagtail.core.blocks.StructBlock([('text', cosme.v1.blocks.HeadingTextBlock(required=False)), ('level', wagtail.core.blocks.ChoiceBlock(choices=[('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4')])), ('icon', cosme.v1.blocks.HeadingIconBlock(help_text='Input the name of an icon to appear to the left of the heading. E.g., approved, help-round, etc. <a href="https://cfpb.github.io/capital-framework/components/cf-icons/#icons">See full list of icons</a>', required=False))], default={'level': 'h3'}, required=False)), ('body', wagtail.core.blocks.RichTextBlock(blank=True, required=False)), ('links', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.CharBlock(required=False)), ('url', wagtail.core.blocks.CharBlock(default='/', required=False))]), required=False))]))), ('sharing', wagtail.core.blocks.StructBlock([('shareable', wagtail.core.blocks.BooleanBlock(help_text='If checked, share links will be included below the items.', label='Include sharing links?', required=False)), ('share_blurb', wagtail.core.blocks.CharBlock(help_text='Sets the tweet text, email subject line, and LinkedIn post text.', required=False))]))])), ('expandable', wagtail.core.blocks.StructBlock([('label', wagtail.core.blocks.CharBlock(required=False)), ('is_bordered', wagtail.core.blocks.BooleanBlock(required=False)), ('is_midtone', wagtail.core.blocks.BooleanBlock(required=False)), ('is_expanded', wagtail.core.blocks.BooleanBlock(required=False)), ('content', wagtail.core.blocks.StreamBlock([('paragraph', wagtail.core.blocks.RichTextBlock(required=False)), ('well', wagtail.core.blocks.StructBlock([('content', wagtail.core.blocks.RichTextBlock(label='Well', required=False))])), ('links', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.CharBlock(required=False)), ('url', wagtail.core.blocks.CharBlock(default='/', required=False))])), ('email', wagtail.core.blocks.StructBlock([('emails', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.CharBlock(required=False)), ('url', wagtail.core.blocks.CharBlock(default='/', required=False))])))])), ('phone', wagtail.core.blocks.StructBlock([('fax', wagtail.core.blocks.BooleanBlock(default=False, label='Is this number a fax?', required=False)), ('phones', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('number', wagtail.core.blocks.CharBlock(max_length=15)), ('extension', wagtail.core.blocks.CharBlock(max_length=4, required=False)), ('vanity', wagtail.core.blocks.CharBlock(help_text='A phoneword version of the above number', max_length=15, required=False)), ('tty', wagtail.core.blocks.CharBlock(label='TTY', max_length=15, required=False)), ('tty_ext', wagtail.core.blocks.CharBlock(label='TTY Extension', max_length=4, required=False))])))])), ('address', wagtail.core.blocks.StructBlock([('label', wagtail.core.blocks.CharBlock(required=False)), ('title', wagtail.core.blocks.CharBlock(required=False)), ('street', wagtail.core.blocks.CharBlock(required=False)), ('city', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('state', wagtail.core.blocks.CharBlock(max_length=25, required=False)), ('zip_code', wagtail.core.blocks.CharBlock(max_length=15, required=False))]))], blank=True))])), ('well', wagtail.core.blocks.StructBlock([('content', wagtail.core.blocks.RichTextBlock(label='Well', required=False))])), ('email_signup', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock(required=False)), ('text', wagtail.core.blocks.CharBlock(required=False)), ('gd_code', wagtail.core.blocks.CharBlock(required=False)), ('form_field', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('btn_text', wagtail.core.blocks.CharBlock(required=False)), ('required', wagtail.core.blocks.BooleanBlock(required=False)), ('info', wagtail.core.blocks.RichTextBlock(label='Disclaimer', required=False)), ('label', wagtail.core.blocks.CharBlock(required=True)), ('type', wagtail.core.blocks.ChoiceBlock(choices=[('text', 'Text'), ('checkbox', 'Checkbox'), ('email', 'Email'), ('number', 'Number'), ('url', 'URL'), ('radio', 'Radio')], required=False)), ('placeholder', wagtail.core.blocks.CharBlock(required=False))]), icon='mail', required=False))])), ('feedback', wagtail.core.blocks.StructBlock([('was_it_helpful_text', wagtail.core.blocks.CharBlock(default='Was this page helpful to you?', help_text='Use this field only for feedback forms that use "Was this helpful?" radio buttons.', required=False)), ('intro_text', wagtail.core.blocks.CharBlock(help_text='Optional feedback intro', required=False)), ('question_text', wagtail.core.blocks.CharBlock(help_text='Optional expansion on intro', required=False)), ('radio_intro', wagtail.core.blocks.CharBlock(help_text='Leave blank unless you are building a feedback form with extra radio-button prompts, as in /owning-a-home/help-us-improve/.', required=False)), ('radio_text', wagtail.core.blocks.CharBlock(default='This information helps us understand your question better.', required=False)), ('radio_question_1', wagtail.core.blocks.CharBlock(default='How soon do you expect to buy a home?', required=False)), ('radio_question_2', wagtail.core.blocks.CharBlock(default='Do you currently own a home?', required=False)), ('button_text', wagtail.core.blocks.CharBlock(default='Submit')), ('contact_advisory', wagtail.core.blocks.RichTextBlock(help_text='Use only for feedback forms that ask for a contact email', required=False))])), ('image_text_50_50_group', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock(icon='title', required=False)), ('link_image_and_heading', wagtail.core.blocks.BooleanBlock(default=False, help_text="Check this to link all images and headings to the URL of the first link in their unit's list, if there is a link.", required=False)), ('sharing', wagtail.core.blocks.StructBlock([('shareable', wagtail.core.blocks.BooleanBlock(help_text='If checked, share links will be included below the items.', label='Include sharing links?', required=False)), ('share_blurb', wagtail.core.blocks.CharBlock(help_text='Sets the tweet text, email subject line, and LinkedIn post text.', required=False))])), ('image_texts', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock(required=False)), ('body', wagtail.core.blocks.RichTextBlock(blank=True, required=False)), ('image', wagtail.core.blocks.StructBlock([('upload', wagtail.images.blocks.ImageChooserBlock(required=False)), ('alt', wagtail.core.blocks.CharBlock(help_text="If the image is decorative (i.e., if a screenreader wouldn't have anything useful to say about it), leave the Alt field blank.", required=False))])), ('is_widescreen', wagtail.core.blocks.BooleanBlock(label='Use 16:9 image', required=False)), ('is_button', wagtail.core.blocks.BooleanBlock(label='Show links as button', required=False)), ('links', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.CharBlock(required=False)), ('url', wagtail.core.blocks.CharBlock(default='/', required=False))]), required=False))])))]))])),
            ],
            options={
                'abstract': False,
            },
            bases=('v1.abstractfilterpage',),
        ),
        migrations.CreateModel(
            name='LegacyBlogPage',
            fields=[
                ('abstractfilterpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='v1.AbstractFilterPage')),
                ('content', wagtail.core.fields.StreamField([('content', wagtail.core.blocks.RawHTMLBlock(help_text='Content from WordPress unescaped.')), ('feedback', wagtail.core.blocks.StructBlock([('was_it_helpful_text', wagtail.core.blocks.CharBlock(default='Was this page helpful to you?', help_text='Use this field only for feedback forms that use "Was this helpful?" radio buttons.', required=False)), ('intro_text', wagtail.core.blocks.CharBlock(help_text='Optional feedback intro', required=False)), ('question_text', wagtail.core.blocks.CharBlock(help_text='Optional expansion on intro', required=False)), ('radio_intro', wagtail.core.blocks.CharBlock(help_text='Leave blank unless you are building a feedback form with extra radio-button prompts, as in /owning-a-home/help-us-improve/.', required=False)), ('radio_text', wagtail.core.blocks.CharBlock(default='This information helps us understand your question better.', required=False)), ('radio_question_1', wagtail.core.blocks.CharBlock(default='How soon do you expect to buy a home?', required=False)), ('radio_question_2', wagtail.core.blocks.CharBlock(default='Do you currently own a home?', required=False)), ('button_text', wagtail.core.blocks.CharBlock(default='Submit')), ('contact_advisory', wagtail.core.blocks.RichTextBlock(help_text='Use only for feedback forms that ask for a contact email', required=False))]))])),
            ],
            options={
                'abstract': False,
            },
            bases=('v1.abstractfilterpage',),
        ),
    ]
