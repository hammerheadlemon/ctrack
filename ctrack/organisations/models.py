from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from slugify import slugify


class AddressType(models.Model):
    descriptor = models.CharField(max_length=50)

    def __str__(self):
        return self.descriptor


class Role(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Person(models.Model):
    TITLES = [
        (1, "Mr"),
        (2, "Mrs"),
        (3, "Miss"),
        (4, "Ms"),
        (5, "Dr."),
        (6, "Professor"),
        (7, "The Rt Hon."),
        (8, "Lord"),
        (9, "Lady"),
    ]

    CLEARANCE_LEVEL = [
        (1, "NA"),
        (2, "BPSS"),
        (3, "CTC"),
        (4, "SC"),
        (5, "DV"),
        (6, "Other"),
    ]

    def get_sentinel_user():  # type: ignore
        """
        We need this so that we can ensure models.SET() is applied with a callable
        to handle when Users are deleted from the system, preventing the Person objects
        related to them being deleted also.
        """
        return get_user_model().objects.get_or_create(username="DELETED USER")[0]

    primary_nis_contact = models.BooleanField(
        default=False, verbose_name="Primary NIS contact"
    )
    voluntary_point_of_contact = models.BooleanField(default=False)
    has_egress = models.BooleanField(default=False, verbose_name="Has Egress")
    title = models.IntegerField(choices=TITLES, default=1)
    job_title = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    organisation = models.ForeignKey("Organisation", on_delete=models.CASCADE)
    role = models.ManyToManyField(Role)
    email = models.EmailField()
    secondary_email = models.EmailField(blank=True)
    mobile = models.CharField(max_length=20, blank=True)
    landline = models.CharField(max_length=20, blank=True)
    date_updated = models.DateField(auto_now=True)
    #    updated_by = models.ForeignKey(
    #        get_user_model(), on_delete=models.SET(get_sentinel_user)
    #    )
    clearance = models.IntegerField(choices=CLEARANCE_LEVEL, default=1)
    clearance_sponsor = models.CharField(max_length=100, blank=True)
    clearance_start_date = models.DateField(blank=True, null=True)
    clearance_last_checked = models.DateField(blank=True, null=True)
    clearance_expiry = models.DateField(blank=True, null=True)
    active = models.BooleanField(default=True)
    date_ended = models.DateField(blank=True, null=True)
    predecessor = models.ForeignKey(
        "self",
        blank=True,
        on_delete=models.CASCADE,
        related_name="previous_person",
        null=True,
    )
    comments = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_organisation_name(self):
        return self.organisation.name

    class Meta:
        verbose_name_plural = "People"


class Mode(models.Model):
    descriptor = models.CharField(max_length=100)

    def __str__(self):
        return self.descriptor


class Submode(models.Model):
    descriptor = models.CharField(max_length=100)
    mode = models.ForeignKey(Mode, on_delete=models.CASCADE)

    def __str__(self):
        return self.descriptor


class Organisation(models.Model):
    DESIGNATION_TYPE = [
        (1, "Automatic"),
        (2, "Reserve Power"),
        (3, "NA"),
    ]

    def get_sentinel_user():  # type: ignore
        """
        We need this so that we can ensure models.SET() is applied with a callable
        to handle when Users are deleted from the system, preventing the Organisations
        related to them being deleted also.
        """
        return get_user_model().objects.get_or_create(username="DELETED USER")[0]

    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from=["name"])
    submode = models.ForeignKey(
        Submode, on_delete=models.CASCADE, blank=True, null=True
    )
    oes = models.BooleanField(default=True)
    designation_type = models.IntegerField(choices=DESIGNATION_TYPE, default=1)
    registered_company_name = models.CharField(max_length=255, blank=True)
    registered_company_number = models.CharField(max_length=100, blank=True)
    date_updated = models.DateField(auto_now=True)
    #    updated_by = models.ForeignKey(
    #        get_user_model(), on_delete=models.SET(get_sentinel_user)
    #    )
    comments = models.TextField(max_length=500, blank=True, null=True)
    active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse("organisations:detail", kwargs={"slug": self.slug})

    def slugify_name(self):
        return slugify(self.name)

    def __str__(self):
        return self.name

    def primary_contacts(self):
        return self.person_set.filter(primary_nis_contact=True)

    def applicable_systems(self):
        # return self.applicablesystem_set.all()
        ess = self.essentialservice_set.all()
        out = []
        for es in ess:
            out.extend(es.systems.all())
        return out

    def systems(self):
        ess = self.essentialservice_set.all()
        out = []
        for es in ess:
            out.extend(list(es.systems.all()))
        return out


class Address(models.Model):
    organisation = models.ForeignKey(
        Organisation, related_name="addresses", on_delete=models.CASCADE, blank=False
    )
    type = models.ForeignKey(
        AddressType, verbose_name="Address Type", on_delete=models.CASCADE, blank=False
    )
    line1 = models.CharField(max_length=255)
    line2 = models.CharField(max_length=255, blank=True)
    line3 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    county = models.CharField(max_length=100, blank=True)
    postcode = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    other_details = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return " ".join([self.organisation.name, self.line1])

    class Meta:
        verbose_name_plural = "Addresses"


class Stakeholder(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.person.first_name} {self.person.last_name}"


class IncidentReport(models.Model):
    def get_sentinel_user():  # type: ignore
        """
        We need this so that we can ensure models.SET() is applied with a callable
        to handle when Users are deleted from the system, preventing the Person objects
        related to them being deleted also.
        """
        return get_user_model().objects.get_or_create(username="DELETED USER")[0]

    DFT_HANDLE_STATUS = (
        ("QUEUED", "QUEUED"),
        ("REVIEWING", "REVIEWING"),
        ("WAITING", "WAITING"),
        ("COMPLETED", "COMPLETED"),
    )
    INCIDENT_TYPES = (
        ("Cyber", "Cyber"),
        ("Non-Cyber", "Non-Cyber"),
        ("Both", "Both"),
        ("Power Outage", "Power Outage"),
    )
    INCIDENT_STATUS = (
        ("Detected", "Detected"),
        ("Suspected", "Suspected"),
        ("Resolved", "Resolved"),
    )
    INCIDENT_STAGE = (
        ("Ongoing", "Ongoing"),
        ("Ended", "Ended"),
        ("Ongoing but managed", "Ongoing but managed"),
    )
    organisation = models.ForeignKey(
        Organisation, blank=False, on_delete=models.CASCADE
    )
    reporting_person = models.ForeignKey(
        Person,
        blank=False,
        on_delete=models.SET(get_user_model),
        verbose_name="Person " "reporting the incident",
    )
    person_involved = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Name of person reporting/detecting incident",
    )
    role = models.CharField(
        max_length=100,
        blank=True,
        help_text="Role of person reporting/detecting incident",
    )
    phone_number = models.CharField(max_length=30, blank=False)
    email = models.EmailField(blank=False)
    internal_incident_number = models.CharField(max_length=30, blank=True)
    date_time_incident_detected = models.DateTimeField(
        verbose_name="Date/Time incident detected", auto_now=False,
    )
    date_time_incident_reported = models.DateTimeField(
        verbose_name="Date/Time incident reported", auto_now=True
    )
    incident_type = models.CharField(
        choices=INCIDENT_TYPES, help_text="This can be appoximate", max_length=20
    )
    incident_status = models.CharField(choices=INCIDENT_STATUS, max_length=20)
    incident_stage = models.CharField(choices=INCIDENT_STAGE, max_length=20)
    summary = models.TextField(
        help_text="Please provide a summary of your understanding of the incident, including"
        " any impact to services and/or users."
    )
    mitigations = models.TextField(
        verbose_name="Investigations or mitigations",
        help_text="What investigations and/or mitigations have you or a third"
        " party performed or plan to perform?",
    )
    others_informed = models.TextField(
        verbose_name="Others parties informed",
        help_text="Who else has been informed about this incident?"
        "(CSIRT, NCSC, NCA, etc)",
    )
    next_steps = models.TextField(
        verbose_name="Planned next steps", help_text="What are your planned next steps?"
    )
    dft_handle_status = models.CharField(
        choices=DFT_HANDLE_STATUS, max_length=20, default="QUEUED"
    )

    def __str__(self):
        return f"{self.reporting_person} - {self.date_time_incident_reported}"
