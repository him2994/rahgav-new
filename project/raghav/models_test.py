# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User



class BibliographicData(models.Model):
    aliass = models.CharField(db_column='Aliass', max_length=150, blank=True, null=True)  # Field name made lowercase.
    patent_number = models.CharField(db_column='Patent_Number', max_length=150, blank=True, null=True)  # Field name made lowercase.
    application_number = models.CharField(db_column='Application_Number', max_length=150, blank=True, null=True)  # Field name made lowercase.
    filing_date = models.CharField(db_column='Filing_Date', max_length=150, blank=True, null=True)  # Field name made lowercase.
    entity = models.CharField(db_column='Entity', max_length=150, blank=True, null=True)  # Field name made lowercase.
    expiration = models.CharField(db_column='Expiration', max_length=150, blank=True, null=True)  # Field name made lowercase.
    total_amt_due = models.CharField(db_column='Total_Amt_Due', max_length=150, blank=True, null=True)  # Field name made lowercase.
    surcharge_date = models.CharField(db_column='Surcharge_Date', max_length=150, blank=True, null=True)  # Field name made lowercase.
    surchg_amt_due = models.CharField(db_column='Surchg_Amt_Due', max_length=150, blank=True, null=True)  # Field name made lowercase.
    most_recent_events = models.CharField(db_column='Most_recent_events', max_length=150, blank=True, null=True)  # Field name made lowercase.
    address_for_fee_purposes = models.CharField(db_column='Address_for_fee_purposes', max_length=150, blank=True, null=True)  # Field name made lowercase.
    issue_date = models.CharField(db_column='Issue_Date', max_length=150, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=150, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=150, blank=True, null=True)  # Field name made lowercase.
    window_opens = models.CharField(db_column='Window_Opens', max_length=150, blank=True, null=True)  # Field name made lowercase.
    fee_amt_due = models.CharField(db_column='Fee_Amt_Due', max_length=150, blank=True, null=True)  # Field name made lowercase.
    fee_code = models.CharField(db_column='Fee_Code', max_length=150, blank=True, null=True)  # Field name made lowercase.
    surcharge_fee_code = models.CharField(db_column='Surcharge_Fee_Code', max_length=150, blank=True, null=True)  # Field name made lowercase.
    open_date_4th_year = models.CharField(db_column='Open_Date_4th_Year', max_length=150, blank=True, null=True)  # Field name made lowercase.
    surcharge_date_4th_year = models.CharField(db_column='Surcharge_Date_4th_Year', max_length=150, blank=True, null=True)  # Field name made lowercase.
    close_date_4th_year = models.CharField(db_column='Close_Date_4th_Year', max_length=150, blank=True, null=True)  # Field name made lowercase.
    open_date_8th_year = models.CharField(db_column='Open_Date_8th_Year', max_length=150, blank=True, null=True)  # Field name made lowercase.
    surcharge_date_8th_year = models.CharField(db_column='Surcharge_Date_8th_Year', max_length=150, blank=True, null=True)  # Field name made lowercase.
    close_date_8th_year = models.CharField(db_column='Close_Date_8th_Year', max_length=150, blank=True, null=True)  # Field name made lowercase.
    open_date_12th_year = models.CharField(db_column='Open_Date_12th_Year', max_length=150, blank=True, null=True)  # Field name made lowercase.
    surcharge_date_12th_year = models.CharField(db_column='Surcharge_Date_12th_Year', max_length=150, blank=True, null=True)  # Field name made lowercase.
    close_date_12th_year = models.CharField(db_column='Close_Date_12th_Year', max_length=150, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Bibliographic_Data'


class Citiations(models.Model):
    alias = models.CharField(db_column='Alias', max_length=150, blank=True, null=True)  # Field name made lowercase.
    document_type = models.CharField(db_column='Document_type', max_length=150, blank=True, null=True)  # Field name made lowercase.
    reference = models.CharField(db_column='Reference', max_length=150, blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=150, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Citiations'


class DesignatedStates(models.Model):
    alias = models.CharField(db_column='Alias', max_length=150, blank=True, null=True)  # Field name made lowercase.
    country_code = models.CharField(db_column='Country_Code', max_length=150, blank=True, null=True)  # Field name made lowercase.
    lapse = models.CharField(db_column='Lapse', max_length=150, blank=True, null=True)  # Field name made lowercase.
    link = models.CharField(db_column='Link', max_length=150, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Designated_states'


class Documents(models.Model):
    alias = models.CharField(db_column='Alias', max_length=150, blank=True, null=True)  # Field name made lowercase.
    date = models.CharField(db_column='Date', max_length=150, blank=True, null=True)  # Field name made lowercase.
    document_type = models.CharField(db_column='Document_type', max_length=150, blank=True, null=True)  # Field name made lowercase.
    no_of_pages = models.CharField(db_column='No_of_Pages', max_length=150, blank=True, null=True)  # Field name made lowercase.
    category_procedure = models.CharField(db_column='Category_Procedure', max_length=150, blank=True, null=True)  # Field name made lowercase.
    link = models.CharField(db_column='Link', max_length=150, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Documents'


class EventHistory(models.Model):
    alias = models.CharField(db_column='Alias', max_length=150, blank=True, null=True)  # Field name made lowercase.
    input = models.CharField(db_column='Input', max_length=150, blank=True, null=True)  # Field name made lowercase.
    date = models.CharField(db_column='Date', max_length=150, blank=True, null=True)  # Field name made lowercase.
    action = models.CharField(db_column='Action', max_length=150, blank=True, null=True)  # Field name made lowercase.
    european_patent_bulletin_date = models.CharField(db_column='European_Patent_Bulletin_date', max_length=150, blank=True, null=True)  # Field name made lowercase.
    issue_number = models.CharField(db_column='Issue_number', max_length=150, blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=150, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Event_history'


class FamilyMember(models.Model):
    input = models.CharField(db_column='Input', max_length=150, blank=True, null=True)  # Field name made lowercase.
    alias = models.CharField(db_column='Alias', max_length=150, blank=True, null=True)  # Field name made lowercase.
    office = models.CharField(db_column='Office', max_length=150, blank=True, null=True)  # Field name made lowercase.
    entry_date = models.CharField(db_column='Entry_Date', max_length=150, blank=True, null=True)  # Field name made lowercase.
    national_number = models.CharField(db_column='National_Number', max_length=150, blank=True, null=True)  # Field name made lowercase.
    national_status = models.CharField(db_column='National_Status', max_length=150, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FAMILY_MEMBER'


class Fees(models.Model):
    alias = models.CharField(db_column='Alias', max_length=150, blank=True, null=True)  # Field name made lowercase.
    input = models.CharField(db_column='Input', max_length=150, blank=True, null=True)  # Field name made lowercase.
    due_date = models.CharField(db_column='Due_Date', max_length=150, blank=True, null=True)  # Field name made lowercase.
    the_sum_of_eur = models.CharField(db_column='The_sum_of_EUR', max_length=150, blank=True, null=True)  # Field name made lowercase.
    payment_type = models.CharField(db_column='Payment_Type', max_length=150, blank=True, null=True)  # Field name made lowercase.
    payment_reference = models.CharField(db_column='Payment_reference', max_length=150, blank=True, null=True)  # Field name made lowercase.
    account_number = models.CharField(db_column='Account_Number', max_length=150, blank=True, null=True)  # Field name made lowercase.
    payment_in_order_no = models.CharField(db_column='Payment_In_order_No', max_length=150, blank=True, null=True)  # Field name made lowercase.
    customer_reference = models.CharField(db_column='Customer_reference', max_length=150, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Fees'


class Main(models.Model):
    alias = models.CharField(db_column='Alias', max_length=150, blank=True, null=True)  # Field name made lowercase.
    application_number = models.CharField(db_column='Application_Number', max_length=150, blank=True, null=True)  # Field name made lowercase.
    legal_status = models.CharField(db_column='Legal_status', max_length=150, blank=True, null=True)  # Field name made lowercase.
    application_date = models.CharField(db_column='Application_date', max_length=150, blank=True, null=True)  # Field name made lowercase.
    priority_information = models.CharField(db_column='Priority_information', max_length=150, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=150, blank=True, null=True)  # Field name made lowercase.
    applicants_proprietors = models.CharField(db_column='Applicants_Proprietors', max_length=150, blank=True, null=True)  # Field name made lowercase.
    pub_no = models.CharField(db_column='Pub_No', max_length=150, blank=True, null=True)  # Field name made lowercase.
    agent = models.CharField(db_column='Agent', max_length=150, blank=True, null=True)  # Field name made lowercase.
    inventors = models.CharField(db_column='Inventors', max_length=150, blank=True, null=True)  # Field name made lowercase.
    publication_date = models.CharField(db_column='Publication_Date', max_length=150, blank=True, null=True)  # Field name made lowercase.
    grant_date = models.CharField(db_column='Grant_Date', max_length=150, blank=True, null=True)  # Field name made lowercase.
    other_title = models.CharField(db_column='Other_Title', max_length=150, blank=True, null=True)  # Field name made lowercase.
    parent_application = models.CharField(db_column='Parent_application', max_length=150, blank=True, null=True)  # Field name made lowercase.
    application_source_type = models.CharField(db_column='Application_Source_Type', max_length=150, blank=True, null=True)  # Field name made lowercase.
    ipc = models.CharField(db_column='IPC', max_length=150, blank=True, null=True)  # Field name made lowercase.
    publication_procedural_language = models.CharField(db_column='Publication_Procedural_language', max_length=150, blank=True, null=True)  # Field name made lowercase.
    filing_language = models.CharField(db_column='Filing_Language', max_length=150, blank=True, null=True)  # Field name made lowercase.
    not_in_force_date = models.CharField(db_column='Not_In_Force_Date', max_length=150, blank=True, null=True)  # Field name made lowercase.
    grant_of_patent = models.CharField(db_column='Grant_of_Patent', max_length=150, blank=True, null=True)  # Field name made lowercase.
    publication_of_notice_in_the_patents_and_designs_journal = models.CharField(db_column='Publication_of_notice_in_the_Patents_and_Designs_Journal', max_length=150, blank=True, null=True)  # Field name made lowercase.
    next_renewal_date = models.CharField(db_column='Next_Renewal_Date', max_length=150, blank=True, null=True)  # Field name made lowercase.
    last_annual_fee_paid = models.CharField(db_column='Last_annual_fee_paid', max_length=150, blank=True, null=True)  # Field name made lowercase.
    paid_annual_fees = models.CharField(db_column='Paid_annual_fees', max_length=150, blank=True, null=True)  # Field name made lowercase.
    examiner = models.CharField(db_column='Examiner', max_length=150, blank=True, null=True)  # Field name made lowercase.
    original_applicant = models.CharField(db_column='Original_Applicant', max_length=150, blank=True, null=True)  # Field name made lowercase.
    abstract = models.CharField(db_column='Abstract', max_length=150, blank=True, null=True)  # Field name made lowercase.
    attorney_docket_number = models.CharField(db_column='Attorney_Docket_Number', max_length=150, blank=True, null=True)  # Field name made lowercase.
    entity_status = models.CharField(db_column='Entity_Status', max_length=150, blank=True, null=True)  # Field name made lowercase.
    aia = models.CharField(db_column='AIA', max_length=150, blank=True, null=True)  # Field name made lowercase.
    status_date = models.CharField(db_column='Status_Date', max_length=150, blank=True, null=True)  # Field name made lowercase.
    international_registration_number = models.CharField(db_column='International_Registration_Number', max_length=150, blank=True, null=True)  # Field name made lowercase.
    international_registration_publication_date = models.CharField(db_column='International_Registration_Publication_Date', max_length=150, blank=True, null=True)  # Field name made lowercase.
    total_pta_adjustments = models.CharField(db_column='Total_PTA_Adjustments', max_length=150, blank=True, null=True)  # Field name made lowercase.
    divisional_applicatio = models.CharField(db_column='Divisional_applicatio', max_length=150, blank=True, null=True)  # Field name made lowercase.
    parent_continuity_data = models.CharField(db_column='Parent_Continuity_Data', max_length=150, blank=True, null=True)  # Field name made lowercase.
    most_recent_event = models.CharField(db_column='Most_recent_event', max_length=150, blank=True, null=True)  # Field name made lowercase.
    international_and_supplementary_search_repor = models.CharField(db_column='International_and_Supplementary_search_repor', max_length=150, blank=True, null=True)  # Field name made lowercase.
    designated_contracting_states = models.CharField(db_column='Designated_contracting_states', max_length=150, blank=True, null=True)  # Field name made lowercase.
    lapses_during_opposition = models.CharField(db_column='Lapses_during_opposition', max_length=150, blank=True, null=True)  # Field name made lowercase.
    opposition = models.CharField(db_column='Opposition', max_length=150, blank=True, null=True)  # Field name made lowercase.
    extension_states = models.CharField(db_column='Extension_states', max_length=150, blank=True, null=True)  # Field name made lowercase.
    us_patent_number = models.CharField(db_column='US_Patent_Number', max_length=150, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Main'


class PtoEvent(models.Model):
    input = models.CharField(db_column='Input', max_length=150, blank=True, null=True)  # Field name made lowercase.
    alias = models.CharField(db_column='Alias', max_length=150, blank=True, null=True)  # Field name made lowercase.
    viraston = models.CharField(db_column='Viraston', max_length=150, blank=True, null=True)  # Field name made lowercase.
    hakijan_vastata = models.CharField(db_column='Hakijan_vastata', max_length=150, blank=True, null=True)  # Field name made lowercase.
    hakijan_vastauspvm = models.CharField(db_column='Hakijan_vastauspvm', max_length=150, blank=True, null=True)  # Field name made lowercase.
    kirjeen_nimi = models.CharField(db_column='Kirjeen_nimi', max_length=150, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PTO_EVENT'


class ParentContinuity(models.Model):
    alias = models.CharField(db_column='Alias', max_length=150, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=150, blank=True, null=True)  # Field name made lowercase.
    parent_number = models.CharField(db_column='Parent_Number', max_length=150, blank=True, null=True)  # Field name made lowercase.
    parent_filing_or_37 = models.CharField(db_column='Parent_Filing_or_37', max_length=150, blank=True, null=True)  # Field name made lowercase.
    ai = models.CharField(db_column='AI', max_length=150, blank=True, null=True)  # Field name made lowercase.
    parent_status = models.CharField(db_column='Parent_Status', max_length=150, blank=True, null=True)  # Field name made lowercase.
    patent_number = models.CharField(db_column='Patent_Number', max_length=150, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Parent_continuity'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class PatentFamily(models.Model):
    alias = models.CharField(db_column='Alias', max_length=150, blank=True, null=True)  # Field name made lowercase.
    source = models.CharField(db_column='Source', max_length=150, blank=True, null=True)  # Field name made lowercase.
    publication = models.CharField(db_column='Publication', max_length=150, blank=True, null=True)  # Field name made lowercase.
    publication_date = models.CharField(db_column='Publication_date', max_length=150, blank=True, null=True)  # Field name made lowercase.
    publication_type = models.CharField(db_column='Publication_type', max_length=150, blank=True, null=True)  # Field name made lowercase.
    priority_no = models.CharField(db_column='Priority_No', max_length=150, blank=True, null=True)  # Field name made lowercase.
    priority_date = models.CharField(db_column='Priority_date', max_length=150, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'patent_family'


class RaghavEmail(models.Model):
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'raghav_email'


class RaghavNumberlist(models.Model):
    number = models.CharField(unique=True, max_length=100)
    stype = models.CharField(max_length=10)
    alias = models.CharField(max_length=10)
    update_in = models.IntegerField()
    is_processed = models.IntegerField()
    processed_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'raghav_numberlist'


class RaghavRuser(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'raghav_ruser'
