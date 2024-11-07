from django.db import models
from django.utils.text import slugify
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Orderable, Page

from pyconph.presentations.models import Schedule, Speaker
from pyconph.sponsors.models import Sponsor, SponsorType


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
        FieldRowPanel(
            [
                FieldPanel("banner_title"),
                FieldPanel("banner_call_to_action"),
                FieldPanel("banner_link"),
            ],
            heading="Promotional Banner",
        ),
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

    def keynote_speakers(self):
        return Speaker.objects.filter(
            is_featured=True,
            keynotespeaker_home__page=self,
        ).order_by("keynotespeaker_home")

    def speakers(self):
        return Speaker.objects.filter(
            is_featured=True,
            speaker_home__page=self,
        ).order_by("speaker_home__sort_order")

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
        return SponsorType.objects.filter(
            sponsor_type_home__page=self,
        ).order_by("sponsor_type_home__sort_order")

    def sponsors(self):
        return Sponsor.objects.filter(
            sponsor_home__page=self,
        ).order_by("sponsor_home__sort_order")
