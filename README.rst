Background
==========

Following the introduction of the `Network and Information Security Directive <https://ec.europa.eu/digital-single-market/en/network-and-information-security-nis-directive>`_, there is a need for Government competent authorities to gather and analyse data about cyber security regimes at Operators of Essential Services (OES) across all relevant sectors.  This is currently being achieved in the UK with the aid of `NCSC's Cyber Assessment Framework (CAF) <https://www.ncsc.gov.uk/blog-post/the-cyber-assessment-framework-3-0>`_.

    "The Cyber Assessment Framework (CAF) provides a systematic and comprehensive approach to assessing the extent to which cyber risks to  essential functions are being managed by the organisation responsible. It is intended to be used either by the responsible organisation itself (self-assessment) or by an independent external entity, possibly a regulator or a suitably qualified organisation acting on behalf of a regulator."
    -- `Cyber Assessment Framework Guidance <https://www.ncsc.gov.uk/collection/caf/cyber-assessment-framework>`_
    
The CAF tool itself currently comprises a multi-sheet Excel document, used to capture assessment scoring and justification text for each contributing outcome in the Directive and to provide a basic dashboard based on cell values.

Automating data collection and analysis
---------------------------------------

The problem faced by competent authorities or other agencies who are typically required to handle dozens (or hundreds) of these files, is to figure out how to collect and analyse the data in a meaningful and efficient way and assess what tooling can be developed to support the ongoing donkey work of collecting and reporting on data, that makes up a typical long term compliance regime.

Excel is often the go-to tool in corporate environments thanks to its ubiquitousness and flexibility. It is easy to create "forms" in Excel for collecting data that can be sent back an forth by email (or more secure means) - however it is not a good tool for long term data storage and/or analysis. A proper database is more appropriate.

What is ctrack?
---------------

Recognising this need, **ctrack** is a proof-of-concept web application developed in-house by the Cyber Compliance Team at the UK Department for Transport that aims to demonstrate the improvements in workflow possible by storing data associated with OES and its associated CAF data in a relational database. It focuses on the absolute basics of managing any business data: *Create*, *Read*, *Update*, *Delete* (CRUD) functionality and demonstrates how collection and analysis of ongoing assessment data - using the CAF as the foundation (the framework, not the spreadsheet) - can be exponentially improved using the simplest of form-based web application.

Technical Notes
---------------

Stakeholders
############

A User can also be associated with a "stakeholder" object, which represents
a Person in the system who is also a User. This means there is an option for
designated third-parties can also have rights to log into the system

Workflow is currently to add Person, User and Stakeholder objects in the Admin.
We would also want to restricted Stakeholder users from being able to do
anything in the system other than X.

Bootstrap
#########

.. code-block:: bash
    
    sudo -u postgres psql postgres
    DROP DATABASE ctrack;
    CREATE DATABASE ctrack;
    \q
    ./utility/trunc_and_populate.sh
    python manage.py migrate
    python manage.py createsuperuser
    python manager.py runserver

