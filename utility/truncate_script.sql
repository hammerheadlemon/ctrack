TRUNCATE TABLE organisations_organisation RESTART IDENTITY CASCADE;
TRUNCATE TABLE organisations_person RESTART IDENTITY CASCADE;
TRUNCATE TABLE organisations_person_role RESTART IDENTITY CASCADE;
TRUNCATE TABLE organisations_mode RESTART IDENTITY CASCADE;
TRUNCATE TABLE organisations_role RESTART IDENTITY CASCADE;
TRUNCATE TABLE organisations_address RESTART IDENTITY CASCADE;
TRUNCATE TABLE organisations_addresstype RESTART IDENTITY CASCADE;
TRUNCATE TABLE organisations_incidentreport RESTART IDENTITY CASCADE;
TRUNCATE TABLE register_engagementevent_participants RESTART IDENTITY CASCADE;
TRUNCATE TABLE register_engagementtype RESTART IDENTITY CASCADE;
TRUNCATE TABLE register_engagementevent RESTART IDENTITY CASCADE;
TRUNCATE TABLE caf_grading RESTART IDENTITY CASCADE;
TRUNCATE TABLE caf_caf RESTART IDENTITY CASCADE;
TRUNCATE TABLE caf_documentfile RESTART IDENTITY CASCADE;
TRUNCATE TABLE caf_applicablesystem RESTART IDENTITY CASCADE;
TRUNCATE TABLE caf_filestore RESTART IDENTITY CASCADE;
TRUNCATE TABLE caf_documentfile RESTART IDENTITY CASCADE;
TRUNCATE TABLE register_engagementevent RESTART IDENTITY CASCADE;
TRUNCATE TABLE register_engagementtype RESTART IDENTITY CASCADE;
TRUNCATE TABLE register_engagementevent_participants RESTART IDENTITY CASCADE;
TRUNCATE TABLE assessments_cafcontributingoutcome RESTART IDENTITY CASCADE;
TRUNCATE TABLE assessments_cafobjective RESTART IDENTITY CASCADE;
TRUNCATE TABLE assessments_cafprinciple RESTART IDENTITY CASCADE;
TRUNCATE TABLE assessments_cafselfassessment RESTART IDENTITY CASCADE;
TRUNCATE TABLE assessments_cafselfassessmentoutcomescore RESTART IDENTITY CASCADE;
TRUNCATE TABLE assessments_achievementlevel RESTART IDENTITY CASCADE;
TRUNCATE TABLE assessments_igp RESTART IDENTITY CASCADE;
DELETE FROM users_user WHERE username != 'mrlemon';
