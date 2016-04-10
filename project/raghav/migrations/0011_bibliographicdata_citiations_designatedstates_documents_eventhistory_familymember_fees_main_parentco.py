# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-27 14:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raghav', '0010_auto_20160220_1612'),
    ]

    operations = [
        migrations.CreateModel(
            name='BibliographicData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aliass', models.CharField(blank=True, db_column='Aliass', max_length=150, null=True)),
                ('patent_number', models.CharField(blank=True, db_column='Patent_Number', max_length=150, null=True)),
                ('application_number', models.CharField(blank=True, db_column='Application_Number', max_length=150, null=True)),
                ('filing_date', models.CharField(blank=True, db_column='Filing_Date', max_length=150, null=True)),
                ('entity', models.CharField(blank=True, db_column='Entity', max_length=150, null=True)),
                ('expiration', models.CharField(blank=True, db_column='Expiration', max_length=150, null=True)),
                ('total_amt_due', models.CharField(blank=True, db_column='Total_Amt_Due', max_length=150, null=True)),
                ('surcharge_date', models.CharField(blank=True, db_column='Surcharge_Date', max_length=150, null=True)),
                ('surchg_amt_due', models.CharField(blank=True, db_column='Surchg_Amt_Due', max_length=150, null=True)),
                ('most_recent_events', models.CharField(blank=True, db_column='Most_recent_events', max_length=150, null=True)),
                ('address_for_fee_purposes', models.CharField(blank=True, db_column='Address_for_fee_purposes', max_length=150, null=True)),
                ('issue_date', models.CharField(blank=True, db_column='Issue_Date', max_length=150, null=True)),
                ('title', models.CharField(blank=True, db_column='Title', max_length=150, null=True)),
                ('status', models.CharField(blank=True, db_column='Status', max_length=150, null=True)),
                ('window_opens', models.CharField(blank=True, db_column='Window_Opens', max_length=150, null=True)),
                ('fee_amt_due', models.CharField(blank=True, db_column='Fee_Amt_Due', max_length=150, null=True)),
                ('fee_code', models.CharField(blank=True, db_column='Fee_Code', max_length=150, null=True)),
                ('surcharge_fee_code', models.CharField(blank=True, db_column='Surcharge_Fee_Code', max_length=150, null=True)),
                ('open_date_4th_year', models.CharField(blank=True, db_column='Open_Date_4th_Year', max_length=150, null=True)),
                ('surcharge_date_4th_year', models.CharField(blank=True, db_column='Surcharge_Date_4th_Year', max_length=150, null=True)),
                ('close_date_4th_year', models.CharField(blank=True, db_column='Close_Date_4th_Year', max_length=150, null=True)),
                ('open_date_8th_year', models.CharField(blank=True, db_column='Open_Date_8th_Year', max_length=150, null=True)),
                ('surcharge_date_8th_year', models.CharField(blank=True, db_column='Surcharge_Date_8th_Year', max_length=150, null=True)),
                ('close_date_8th_year', models.CharField(blank=True, db_column='Close_Date_8th_Year', max_length=150, null=True)),
                ('open_date_12th_year', models.CharField(blank=True, db_column='Open_Date_12th_Year', max_length=150, null=True)),
                ('surcharge_date_12th_year', models.CharField(blank=True, db_column='Surcharge_Date_12th_Year', max_length=150, null=True)),
                ('close_date_12th_year', models.CharField(blank=True, db_column='Close_Date_12th_Year', max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Citiations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alias', models.CharField(blank=True, db_column='Alias', max_length=150, null=True)),
                ('document_type', models.CharField(blank=True, db_column='Document_type', max_length=150, null=True)),
                ('reference', models.CharField(blank=True, db_column='Reference', max_length=150, null=True)),
                ('category', models.CharField(blank=True, db_column='Category', max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DesignatedStates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alias', models.CharField(blank=True, db_column='Alias', max_length=150, null=True)),
                ('country_code', models.CharField(blank=True, db_column='Country_Code', max_length=150, null=True)),
                ('lapse', models.CharField(blank=True, db_column='Lapse', max_length=150, null=True)),
                ('link', models.CharField(blank=True, db_column='Link', max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alias', models.CharField(blank=True, db_column='Alias', max_length=150, null=True)),
                ('date', models.CharField(blank=True, db_column='Date', max_length=150, null=True)),
                ('document_type', models.CharField(blank=True, db_column='Document_type', max_length=150, null=True)),
                ('no_of_pages', models.CharField(blank=True, db_column='No_of_Pages', max_length=150, null=True)),
                ('category_procedure', models.CharField(blank=True, db_column='Category_Procedure', max_length=150, null=True)),
                ('link', models.CharField(blank=True, db_column='Link', max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EventHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alias', models.CharField(blank=True, db_column='Alias', max_length=150, null=True)),
                ('input', models.CharField(blank=True, db_column='Input', max_length=150, null=True)),
                ('date', models.CharField(blank=True, db_column='Date', max_length=150, null=True)),
                ('action', models.CharField(blank=True, db_column='Action', max_length=150, null=True)),
                ('european_patent_bulletin_date', models.CharField(blank=True, db_column='European_Patent_Bulletin_date', max_length=150, null=True)),
                ('issue_number', models.CharField(blank=True, db_column='Issue_number', max_length=150, null=True)),
                ('category', models.CharField(blank=True, db_column='Category', max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FamilyMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input', models.CharField(blank=True, db_column='Input', max_length=150, null=True)),
                ('alias', models.CharField(blank=True, db_column='Alias', max_length=150, null=True)),
                ('office', models.CharField(blank=True, db_column='Office', max_length=150, null=True)),
                ('entry_date', models.CharField(blank=True, db_column='Entry_Date', max_length=150, null=True)),
                ('national_number', models.CharField(blank=True, db_column='National_Number', max_length=150, null=True)),
                ('national_status', models.CharField(blank=True, db_column='National_Status', max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Fees',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alias', models.CharField(blank=True, db_column='Alias', max_length=150, null=True)),
                ('input', models.CharField(blank=True, db_column='Input', max_length=150, null=True)),
                ('due_date', models.CharField(blank=True, db_column='Due_Date', max_length=150, null=True)),
                ('the_sum_of_eur', models.CharField(blank=True, db_column='The_sum_of_EUR', max_length=150, null=True)),
                ('payment_type', models.CharField(blank=True, db_column='Payment_Type', max_length=150, null=True)),
                ('payment_reference', models.CharField(blank=True, db_column='Payment_reference', max_length=150, null=True)),
                ('account_number', models.CharField(blank=True, db_column='Account_Number', max_length=150, null=True)),
                ('payment_in_order_no', models.CharField(blank=True, db_column='Payment_In_order_No', max_length=150, null=True)),
                ('customer_reference', models.CharField(blank=True, db_column='Customer_reference', max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Main',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alias', models.CharField(blank=True, db_column='Alias', max_length=150, null=True)),
                ('application_number', models.CharField(blank=True, db_column='Application_Number', max_length=150, null=True)),
                ('legal_status', models.CharField(blank=True, db_column='Legal_status', max_length=150, null=True)),
                ('application_date', models.CharField(blank=True, db_column='Application_date', max_length=150, null=True)),
                ('priority_information', models.CharField(blank=True, db_column='Priority_information', max_length=150, null=True)),
                ('title', models.CharField(blank=True, db_column='Title', max_length=150, null=True)),
                ('applicants_proprietors', models.CharField(blank=True, db_column='Applicants_Proprietors', max_length=150, null=True)),
                ('pub_no', models.CharField(blank=True, db_column='Pub_No', max_length=150, null=True)),
                ('agent', models.CharField(blank=True, db_column='Agent', max_length=150, null=True)),
                ('inventors', models.CharField(blank=True, db_column='Inventors', max_length=150, null=True)),
                ('publication_date', models.CharField(blank=True, db_column='Publication_Date', max_length=150, null=True)),
                ('grant_date', models.CharField(blank=True, db_column='Grant_Date', max_length=150, null=True)),
                ('other_title', models.CharField(blank=True, db_column='Other_Title', max_length=150, null=True)),
                ('parent_application', models.CharField(blank=True, db_column='Parent_application', max_length=150, null=True)),
                ('application_source_type', models.CharField(blank=True, db_column='Application_Source_Type', max_length=150, null=True)),
                ('ipc', models.CharField(blank=True, db_column='IPC', max_length=150, null=True)),
                ('publication_procedural_language', models.CharField(blank=True, db_column='Publication_Procedural_language', max_length=150, null=True)),
                ('filing_language', models.CharField(blank=True, db_column='Filing_Language', max_length=150, null=True)),
                ('not_in_force_date', models.CharField(blank=True, db_column='Not_In_Force_Date', max_length=150, null=True)),
                ('grant_of_patent', models.CharField(blank=True, db_column='Grant_of_Patent', max_length=150, null=True)),
                ('publication_of_notice_in_the_patents_and_designs_journal', models.CharField(blank=True, db_column='Publication_of_notice_in_the_Patents_and_Designs_Journal', max_length=150, null=True)),
                ('next_renewal_date', models.CharField(blank=True, db_column='Next_Renewal_Date', max_length=150, null=True)),
                ('last_annual_fee_paid', models.CharField(blank=True, db_column='Last_annual_fee_paid', max_length=150, null=True)),
                ('paid_annual_fees', models.CharField(blank=True, db_column='Paid_annual_fees', max_length=150, null=True)),
                ('examiner', models.CharField(blank=True, db_column='Examiner', max_length=150, null=True)),
                ('original_applicant', models.CharField(blank=True, db_column='Original_Applicant', max_length=150, null=True)),
                ('abstract', models.CharField(blank=True, db_column='Abstract', max_length=150, null=True)),
                ('attorney_docket_number', models.CharField(blank=True, db_column='Attorney_Docket_Number', max_length=150, null=True)),
                ('entity_status', models.CharField(blank=True, db_column='Entity_Status', max_length=150, null=True)),
                ('aia', models.CharField(blank=True, db_column='AIA', max_length=150, null=True)),
                ('status_date', models.CharField(blank=True, db_column='Status_Date', max_length=150, null=True)),
                ('international_registration_number', models.CharField(blank=True, db_column='International_Registration_Number', max_length=150, null=True)),
                ('international_registration_publication_date', models.CharField(blank=True, db_column='International_Registration_Publication_Date', max_length=150, null=True)),
                ('total_pta_adjustments', models.CharField(blank=True, db_column='Total_PTA_Adjustments', max_length=150, null=True)),
                ('divisional_applicatio', models.CharField(blank=True, db_column='Divisional_applicatio', max_length=150, null=True)),
                ('parent_continuity_data', models.CharField(blank=True, db_column='Parent_Continuity_Data', max_length=150, null=True)),
                ('most_recent_event', models.CharField(blank=True, db_column='Most_recent_event', max_length=150, null=True)),
                ('international_and_supplementary_search_repor', models.CharField(blank=True, db_column='International_and_Supplementary_search_repor', max_length=150, null=True)),
                ('designated_contracting_states', models.CharField(blank=True, db_column='Designated_contracting_states', max_length=150, null=True)),
                ('lapses_during_opposition', models.CharField(blank=True, db_column='Lapses_during_opposition', max_length=150, null=True)),
                ('opposition', models.CharField(blank=True, db_column='Opposition', max_length=150, null=True)),
                ('extension_states', models.CharField(blank=True, db_column='Extension_states', max_length=150, null=True)),
                ('us_patent_number', models.CharField(blank=True, db_column='US_Patent_Number', max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ParentContinuity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alias', models.CharField(blank=True, db_column='Alias', max_length=150, null=True)),
                ('description', models.CharField(blank=True, db_column='Description', max_length=150, null=True)),
                ('parent_number', models.CharField(blank=True, db_column='Parent_Number', max_length=150, null=True)),
                ('parent_filing_or_37', models.CharField(blank=True, db_column='Parent_Filing_or_37', max_length=150, null=True)),
                ('ai', models.CharField(blank=True, db_column='AI', max_length=150, null=True)),
                ('parent_status', models.CharField(blank=True, db_column='Parent_Status', max_length=150, null=True)),
                ('patent_number', models.CharField(blank=True, db_column='Patent_Number', max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PatentFamily',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alias', models.CharField(blank=True, db_column='Alias', max_length=150, null=True)),
                ('source', models.CharField(blank=True, db_column='Source', max_length=150, null=True)),
                ('publication', models.CharField(blank=True, db_column='Publication', max_length=150, null=True)),
                ('publication_date', models.CharField(blank=True, db_column='Publication_date', max_length=150, null=True)),
                ('publication_type', models.CharField(blank=True, db_column='Publication_type', max_length=150, null=True)),
                ('priority_no', models.CharField(blank=True, db_column='Priority_No', max_length=150, null=True)),
                ('priority_date', models.CharField(blank=True, db_column='Priority_date', max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PtoEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input', models.CharField(blank=True, db_column='Input', max_length=150, null=True)),
                ('alias', models.CharField(blank=True, db_column='Alias', max_length=150, null=True)),
                ('viraston', models.CharField(blank=True, db_column='Viraston', max_length=150, null=True)),
                ('hakijan_vastata', models.CharField(blank=True, db_column='Hakijan_vastata', max_length=150, null=True)),
                ('hakijan_vastauspvm', models.CharField(blank=True, db_column='Hakijan_vastauspvm', max_length=150, null=True)),
                ('kirjeen_nimi', models.CharField(blank=True, db_column='Kirjeen_nimi', max_length=150, null=True)),
            ],
        ),
    ]