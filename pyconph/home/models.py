import os
from datetime import datetime

from django.core.cache import cache
from django.db import models
from django.db.models import Count
from django.utils import timezone
from django.utils.text import slugify
from modelcluster.fields import ParentalKey
from requests import exceptions
from wagtail.admin.panels import (FieldPanel, FieldRowPanel, InlinePanel,
                                  MultiFieldPanel)
from wagtail.fields import RichTextField
from wagtail.models import Orderable, Page
from wagtail.snippets.models import register_snippet

from pyconph.presentations.models import Schedule
from pyconph.sponsors.models import Sponsor, SponsorType

from ..services.pretalx import PretalxService


class PageContent(Orderable, models.Model):
    class ImagePositions(models.TextChoices):
        LEFT = ("left", "Left")
        RIGHT = ("right", "Right")

    page = ParentalKey("HomePage", related_name="contents", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
    body = RichTextField()

    image = models.ForeignKey("wagtailimages.Image", on_delete=models.CASCADE)
    image_position = models.CharField(choices=ImagePositions.choices, max_length=32)
    is_subcontent = models.BooleanField(default=False)

    @property
    def slug(self):
        return slugify(self.title)


class Banner(models.Model):
    page = ParentalKey('home.HomePage', related_name='banners', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    call_to_action = models.CharField(max_length=255, blank=True)
    link = models.URLField(blank=True)
    start_date = models.DateField(blank=False)
    start_time = models.TimeField(blank=False, default='00:00')
    end_date = models.DateField(blank=False)
    end_time = models.TimeField(blank=False, default='23:59')

    panels = [
        FieldPanel('title'),
        FieldPanel('call_to_action'),
        FieldPanel('link'),
        FieldPanel('start_date'),
        FieldPanel('start_time'),
        FieldPanel('end_date'),
        FieldPanel('end_time'),
    ]

    def is_active(self):
        now = timezone.now()
        start_datetime = timezone.make_aware(datetime.combine(self.start_date, self.start_time))
        end_datetime = timezone.make_aware(datetime.combine(self.end_date, self.end_time))
        return start_datetime <= now <= end_datetime

    def __str__(self):
        return self.title

register_snippet(Banner)


class HomePage(Page):
    date_start = models.DateField()
    date_end = models.DateField()
    time_start = models.TimeField()

    ticket_link = models.URLField(blank=True)
    cfp_link = models.URLField(blank=True)
    sponsor_link = models.URLField(blank=True)

    location_main = models.CharField(max_length=255)
    location_city = models.CharField(max_length=255)
    location_link = models.URLField(blank=True)
    location_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    keynote_title = models.CharField(max_length=255)
    keynote_subtitle = models.CharField(max_length=255, blank=True)

    speaker_title = models.CharField(max_length=255)
    speaker_subtitle = models.CharField(max_length=255, blank=True)

    schedule_title = models.CharField(max_length=255)
    schedule_subtitle = models.CharField(max_length=255, blank=True)

    sponsor_title = models.CharField(max_length=255)
    sponsor_subtitle = models.CharField(max_length=255, blank=True)

    banner_title = models.CharField(max_length=255, blank=True)
    banner_call_to_action = models.CharField(max_length=255, blank=True)
    banner_link = models.URLField(blank=True)

    content_panels = Page.content_panels + [
        FieldRowPanel(
            [
                FieldPanel("ticket_link"),
                FieldPanel("cfp_link"),
                FieldPanel("sponsor_link"),
            ]
        ),
        InlinePanel('banners', label="Promotional Banner"),
        FieldRowPanel(
            [
                FieldPanel("date_start"),
                FieldPanel("date_end"),
                FieldPanel("time_start"),
            ],
            heading="Date and Time",
        ),
        MultiFieldPanel(
            [
                FieldPanel("location_main"),
                FieldPanel("location_city"),
                FieldPanel("location_link"),
                FieldPanel("location_image"),
            ],
            heading="Location",
        ),
        InlinePanel("contents", label="Contents"),
        MultiFieldPanel(
            [
                FieldPanel("keynote_title", heading="Title"),
                FieldPanel("keynote_subtitle", heading="Subtitle"),
                InlinePanel("home_keynotespeaker", label="Keynote Speakers"),
            ],
            heading="Keynote Speakers",
        ),
        MultiFieldPanel(
            [
                FieldPanel("speaker_title", heading="Title"),
                FieldPanel("speaker_subtitle", heading="Subtitle"),
                InlinePanel("home_speaker", label="Speakers"),
            ],
            heading="Speakers",
        ),
        MultiFieldPanel(
            [
                FieldPanel("schedule_title", heading="Title"),
                FieldPanel("schedule_subtitle", heading="Subtitle"),
                InlinePanel("schedules", label="Schedule"),
            ],
            heading="Program Schedules",
        ),
        MultiFieldPanel(
            [
                FieldPanel("sponsor_title", heading="Title"),
                FieldPanel("sponsor_subtitle", heading="Subtitle"),
                InlinePanel("home_sponsor_type", label="Sponsor Types"),
            ],
            heading="Sponsor Types",
        ),
        InlinePanel("home_sponsor", label="Sponsors"),
    ]

    @property
    def date(self):
        start_day = self.date_start.day
        end = self.date_end.strftime("%d %B, %Y")
        return f"{start_day}-{end}"

    @property
    def doors_open(self):
        return self.time_start.strftime("%-I:%M%p")

    @property
    def day1_date(self):
        return self.date_start.strftime("%B %d")

    @property
    def day2_date(self):
        return self.date_end.strftime("%B %d")

    @property
    def content_topics(self):
        return (
            "Beginner & General Programming",
            "Backend / DevOps",
            "Machine Learning & Artificial Intelligence",
            "Distributed Computing",
            "Personal & Professional Development",
            "Platform / Framework / Architecture / Security",
            "Data Science / Analysis / Engineering",
            "Web / Mobile",
            "Practices",
        )

    @property
    def keynote_speakers(self):
        keynotes = cache.get('keynotes')
        if keynotes:
            return keynotes

        api_token = os.getenv('PRETALX_API_TOKEN')
        base_url = os.getenv('PRETALX_BASE_URL', 'https://pretalx.com')
        slug = os.getenv('PRETALX_SLUG', 'pycon-apac-2025')

        if not api_token:
            return

        service = PretalxService(
            base_url=base_url,
            api_token=api_token
        )
        speakers = []
        try:
            talks = service.get_talks(slug).get('results', [])
            for talk in talks:
                if '[Keynote]' not in talk['title']:
                    continue
                for speaker in talk['speakers']:
                    speakers.append(speaker)

            cache.set('keynotes', speakers, 43200)
        except exceptions.HTTPError:
            pass

        return speakers

    @property
    def speakers(self):
        speakers = cache.get('speakers')
        if speakers:
            return speakers

        api_token = os.getenv('PRETALX_API_TOKEN')
        base_url = os.getenv('PRETALX_BASE_URL', 'https://pretalx.com')
        slug = os.getenv('PRETALX_SLUG', 'pycon-apac-2025')
 
        if not api_token:
            return

        service = PretalxService(
            base_url=base_url,
            api_token=api_token
        )
        speakers = []
        try:
            talks = service.get_talks(slug).get('results', [])
            for talk in talks:
                if '[Keynote]' in talk['title']:
                    continue
                for speaker in talk['speakers']:
                    speakers.append(speaker)

            cache.set('speakers', speakers, 43200)
        except exceptions.HTTPError:
            pass
        return speakers

    def day1_events(self):
        return Schedule.objects.filter(
            page=self,
            day=Schedule.Days.DAY1,
        ).order_by("sort_order")

    def day2_events(self):
        return Schedule.objects.filter(
            page=self,
            day=Schedule.Days.DAY2,
        ).order_by("sort_order")

    def sponsor_types(self):
        return SponsorType.objects.annotate(
            sponsor_count=Count("sponsors")
        ).filter(
            sponsor_type_home__page=self,
            sponsor_count__gt=0,
        ).order_by("sponsor_type_home__sort_order")

    def sponsors(self):
        return Sponsor.objects.filter(
            sponsor_home__page=self,
        ).order_by("sponsor_home__sort_order")

    def active_banner(self):
        for banner in self.banners.all():
            if banner.is_active():
                return banner
