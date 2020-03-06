from django.db import models

from ctrack.organisations.models import Organisation, Person, Submode
import ctrack.caf.models  # to deal with circular import


class ApplicableSystemManager(models.Manager):
    def with_primary_contact(self):
        """
        Add in the name of the primary nis contact to the context.
        Using Custom Managers Django docs for an example.
        """
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT a.id, a.name, o.id, c.id, sm.id, p.id, o.name
                FROM caf_applicablesystem a, organisations_organisation o, organisations_person p, caf_caf c, organisations_submode sm
                WHERE a.organisation_id = o.id AND a.caf_id = c.id AND p.organisation_id = o.id AND o.submode_id = sm.id AND p.primary_nis_contact = False;
            """)
            result_list = []
            for row in cursor.fetchall():
                org = Organisation.objects.get(pk=row[2])
                caf = ctrack.caf.models.CAF.objects.get(pk=row[3])
                ass = self.model(id=row[0], name=row[1], organisation=org, caf=caf)
                ass.nis_contact = Person.objects.get(pk=row[5])
                result_list.append(ass)
            return result_list
