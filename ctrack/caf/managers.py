from django.db import connection, models

import ctrack.caf.models as caf_models  # to deal with circular import
import ctrack.organisations.models as org_models


class ApplicableSystemManager(models.Manager):
    def with_primary_contact(self):
        """
        THIS IS NOT CURRENTLY USED BUT LEAVING IT IN FOR REF
        BETTER WAS TO ADD A MODEL METHOD TO FIND THE POC FOR EACH
        ORGANISATION AND ADAPT THE TEMPLATE TO USE THAT.

        Add in the name of the primary nis contact to the context.
        Using Custom Managers Django docs for an example.
        """
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT a.id, a.name, o.id, c.id, sm.id, p.id, o.name
                FROM caf_applicablesystem a, organisations_organisation o, organisations_person p, caf_caf c, organisations_submode sm
                WHERE a.organisation_id = o.id AND a.caf_id = c.id AND p.organisation_id = o.id AND o.submode_id = sm.id AND p.primary_nis_contact = True;
            """
            )
            result_list = []
            for row in cursor.fetchall():
                org = org_models.Organisation.objects.get(pk=row[3])
                caf = ctrack.caf.models.CAF.objects.get(pk=row[3])
                ass = self.model(id=row[0], name=row[1], organisation=org, caf=caf)
                ass.nis_contact = Person.objects.get(pk=row[5])
                result_list.append(ass)
            return result_list
