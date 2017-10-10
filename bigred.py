#!/usr/bin/python
'''
Original build on Jun 29, 2015

@author: mzd2016

A smaller version of big red, restricted to 50,000 patients. This is to 
expedite regression testing.
'''

from db_utils import run_scripts, finalize
from paver.easy import task, needs, no_help


'''The main methods which drive the ETL'''
@task
@needs([
  'bigred.mapping_refresh'
  ,'bigred.miscellaneous_entries'
  ,'bigred.metadata'
  ,'bigred.dimension'
  ,'bigred.demodata'
  ,'bigred.finalize_etl'
])
def etl():
  ''' Full ETL '''
  pass


@task
@needs([ 
  'bigred.mapping_refresh'
  ,'bigred.miscellaneous_entries'
  ,'bigred.dimension'
  ,'bigred.demodata'
  ,'bigred.finalize_etl'
])
def etl_refresh():
  ''' ETL that skips metadata '''
  pass


@task
@needs([
  'bigred.truncate_mapping'
  ,'bigred.miscellaneous_entries'
  ,'bigred.metadata'
  ,'bigred.dimension'
  ,'bigred.demodata'
  ,'bigred.finalize_etl'
])
def unit_test():
  ''' ETL that skips mapping '''
  pass




'''2nd level functions'''
@task
@needs([
  'bigred.drop_indexes_encounter_mapping'
  ,'bigred.drop_indexes_patient_mapping'
  ,'bigred.truncate_mapping'
  ,'bigred.patient_mapping'
  ,'bigred.encounter_mapping'
])
def mapping_refresh():
  '''refresh mapping entries'''
  pass

@task
@needs([
  'bigred.truncate_misc'
  ,'bigred.blacklists_refresh'
  ,'bigred.redcap_preprocessing'
])
@run_scripts(
  'heron'
  ,'etc/truncate_tables_preprocessing.sql'
  ,'demodata/build_code_lookup.sql'
  ,'demodata/build_source_master.sql'
  ,'metadata/build_schemes.sql'
  ,'preprocessing/process_social_history.sql'
  ,'preprocessing/process_tdl_tran.sql'
  ,'preprocessing/process_order_proc.sql'
  ,'preprocessing/process_microbiology.sql'
)
def miscellaneous_entries():
  '''Refresh blacklists, run preprocessing for redcap and other tables, rebuild tables code_lookup, source_master, and schemes'''
  pass

@task
@needs([
  'bigred.drop_indexes_metadata'
  ,'bigred.truncate_metadata'
  ,'bigred.metadata_epic'
  ,'bigred.metadata_other'
  ,'bigred.build_indexes_metadata'
])
def metadata():
  '''refresh all metadata'''
  pass

@task
@needs([
  'bigred.drop_indexes_dimension'
  ,'bigred.truncate_dimension'
  ,'bigred.build_dimension_entries_standard'
  ,'bigred.build_dimension_entries_other'
  ,'bigred.build_indexes_dimension'
])
def dimension():
  '''refresh all dimension data'''
  pass

@task
@needs([
  'bigred.drop_indexes_fact'
  ,'bigred.truncate_fact'
  ,'bigred.observation_fact_epic'
  ,'bigred.observation_fact_other'
  ,'bigred.build_indexes_fact'
])
def demodata():
  '''refresh all observation_fact data'''
  pass

@task
@needs([
  'bigred.redcap_cleanup'
  ,'bigred.create_datamart_report'
  #,'bigred.counting'
  ])
def finalize_etl():
  '''Scripts to be run when finalizing the ETL'''
  pass




'''MAPPING'''
@task
@run_scripts('heron', 'index/drop_indexes_patient_mapping.sql')
def drop_indexes_patient_mapping():
  '''drop patient_mapping indexes'''
  pass

@task
@run_scripts('heron', 'index/drop_indexes_encounter_mapping.sql')
def drop_indexes_encounter_mapping():
  '''drop encounter_mapping indexes'''
  pass

@task
@run_scripts('heron', 'etc/truncate_mapping_tables.sql')
def truncate_mapping():
  ''' Empties i2b2 mapping tables '''
  pass

@task
@run_scripts('heron', 'mapping/build_patient_mapping.sql', 'index/build_patient_mapping_indexes.sql')
def patient_mapping():
  pass

@task
@needs([
  'bigred.crest_encounter_mapping'
  ,'bigred.ormanager_encounter_mapping'
  ,'bigred.redcap_encounter_mapping'
  ,'bigred.compurecord_encounter_mapping'
  ,'bigred.eclipsys_encounter_mapping'
  ,'bigred.eagle_encounter_mapping'
  ,'bigred.tumor_registry_encounter_mapping'
])
@run_scripts(
  'heron'
  ,'mapping/build_encounter_mapping_epic.sql'
  ,'mapping/build_encounter_mapping_idx.sql'
  ,'index/build_encounter_mapping_indexes.sql'
)
def encounter_mapping():
  pass

@task
@run_scripts('heron', 'index/build_encounter_mapping_indexes.sql')
def build_indexes_encounter_mapping():
  '''build encounter_mapping indexes'''
  pass

@task
@run_scripts('heron', 'index/build_patient_mapping_indexes.sql')
def build_indexes_patient_mapping():
  '''build patient_mapping indexes'''
  pass





'''METADATA'''
@task
@run_scripts('heron', 'index/drop_indexes_metadata.sql')
def drop_indexes_metadata():
  pass

@task
@run_scripts('heron', 'etc/truncate_tables_metadata_fact.sql', 'etc/truncate_tables_metadata.sql')
def truncate_metadata():
  pass

@task
@run_scripts(
  'heron'
  ,'metadata/build_table_access.sql'
  ,'metadata/build_table_access_nlp.sql'
  ,'metadata/build_sourcesystem_ontology.sql'
  ,'metadata/build_demographics_ontology.sql'
  ,'metadata/build_mrn_entry.sql'
  ,'metadata/build_icd9_diagnoses_ontology.sql'
  ,'metadata/build_icd10_diagnoses_ontology.sql'
  ,'metadata/build_encounters_ontology.sql'
  ,'metadata/build_procedures_ontology.sql' 
  ,'metadata/build_medications_ontology.sql'
  ,'metadata/build_social_history_ontology.sql'
  ,'metadata/build_family_history_ontology.sql'
  ,'metadata/build_insurance_ontology.sql'
  ,'metadata/build_results_ontology.sql'
  ,'metadata/build_provider_ontology.sql'
  ,'metadata/build_allergy_ontology.sql'
  ,'metadata/build_micro_ontology.sql'
  ,'metadata/build_nlp_ontology.sql'
  ,'metadata/build_modifier_ontology.sql'
  ,'metadata/rectify_ontological_disparities.sql'
)
def metadata_epic():
  pass

@task
@needs([
   'bigred.crest_metadata'
  ,'bigred.ormanager_metadata'
  ,'bigred.profiler_metadata'
  ,'bigred.redcap_metadata'
  ,'bigred.compurecord_metadata'
  ,'bigred.eclipsys_metadata'
  ,'bigred.eagle_metadata'
  ,'bigred.tumor_registry_metadata'
  ,'bigred.custom_ontology_review'
])
def metadata_other():
  pass

@task
@run_scripts('heron', 'index/build_indexes_metadata.sql')
def build_indexes_metadata():
  pass

@task
@run_scripts('heron', 'metadata/rectify_ontological_disparities_custom.sql')
def custom_ontology_review():
    pass



'''DIMENSION'''
@task
@run_scripts('heron', 'index/drop_indexes_dimension_metadata.sql', 'index/drop_indexes_dimension_data.sql')
def drop_indexes_dimension():
  pass

@task
@run_scripts('heron', 'etc/truncate_tables_dimension_data.sql', 'etc/truncate_tables_dimension_metadata.sql')
def truncate_dimension():
  ''' Empties select I2B2 tables while leaving their structure intact. '''
  pass

@task
@run_scripts(
  'heron'
  ,'demodata/build_patient_dimension_facts.sql'
  ,'demodata/build_visit_dimension_facts.sql'
  ,'demodata/build_provider_dimension_facts.sql'
  ,'demodata/build_concept_dimension_entries.sql'
  ,'demodata/build_modifier_dimension_facts.sql'
)
def build_dimension_entries_standard():
  '''builds dimension entries'''
  pass

@task
@needs([
  'bigred.crest_dimension'
  ,'bigred.ormanager_dimension'
  ,'bigred.profiler_dimension'
  ,'bigred.redcap_dimension'
  ,'bigred.compurecord_dimension'
  ,'bigred.eclipsys_dimension'
  ,'bigred.eagle_dimension'
  ,'bigred.tumor_registry_dimension'
])
def build_dimension_entries_other():
  '''builds dimension entries for other source systems'''
  pass

@task
@run_scripts('heron', 'index/build_indexes_dimension.sql')
def build_indexes_dimension():
  pass


@task
@run_scripts('heron' 
  ,'demodata/build_concept_dimension_entries.sql'
  ,'demodata/build_modifier_dimension_facts.sql'
  ,'demodata/build_indexes_dimension.sql')
def refresh_concept_modifier_dimensions():
    ''' Useful only when refreshing only the metadata for a project
        These two tables are truncated and need to be populated with
        updated information. Unused for the full-strength ETL '''
    pass

'''DEMODATA'''
@task
@run_scripts('heron', 'index/drop_indexes_fact.sql', 'etc/recreate_observation_fact_partitions.sql')
def drop_indexes_fact():
  pass

@task
@run_scripts('heron', 'etc/truncate_tables_fact.sql', 'etc/recreate_observation_fact_partitions.sql')
def truncate_fact():
  ''' Empties select I2B2 tables while leaving their structure intact. '''
  pass

@task
@run_scripts(
  'heron'
  ,'demodata/build_observation_facts_gestational_age.sql'
  ,'demodata/build_observation_facts_aco_status.sql'
  ,'demodata/build_observation_facts_vital_status.sql'
  ,'demodata/build_observation_facts_mrns.sql'
  ,'demodata/build_observation_facts_insurance_status.sql'
  ,'demodata/build_observation_facts_surgical_history.sql'
  ,'demodata/build_observation_facts_social_history.sql'
  ,'demodata/build_observation_facts_family_history.sql'
  ,'demodata/build_observation_facts_nlp.sql'
  ,'demodata/build_observation_facts_micro.sql'
  ,'demodata/build_observation_facts_micro_order_sensitivity.sql'
  ,'demodata/build_observation_facts_allergies.sql'
  ,'demodata/build_observation_facts_age_at_encounter.sql'
  ,'demodata/build_observation_facts_diagnoses.sql'
  ,'demodata/build_observation_facts_encounters.sql'
  ,'demodata/build_observation_facts_medications.sql'
  ,'demodata/build_observation_facts_results.sql'
  ,'demodata/build_observation_facts_procedures.sql'
)
def observation_fact_epic():
  pass

@task
@needs([
  'bigred.crest_demodata'
  ,'bigred.ormanager_demodata'
  ,'bigred.profiler_demodata'
  ,'bigred.redcap_demodata'
  ,'bigred.compurecord_demodata'
  ,'bigred.eclipsys_demodata'
  ,'bigred.eagle_demodata'
  ,'bigred.tumor_registry_demodata'
])
def observation_fact_other():
  pass

@task
@run_scripts(
  'heron'
  ,'index/build_indexes_dimension.sql'
  ,'index/build_clustered_index_fact.sql'
  ,'index/build_indexes_fact.sql'
  #,'index/build_patient_counting_nonclustered_indexes_fact.sql'
  #,'index/build_columnstore_index_fact.sql'
)
def build_indexes_fact():
  pass




''' Other source systems '''
'''CREST'''
@task
@run_scripts('heron','mapping/build_encounter_mapping_crest.sql')
def crest_encounter_mapping():
  pass

@task
@run_scripts('heron', 'etc/truncate_crest_metadata.sql', 'etc/truncate_crest_data.sql')
def crest_truncate():
  ''' Truncates only CREST data from table'''
  pass

@task
@run_scripts('heron', 'metadata/build_table_access_crest.sql', 'metadata/build_crest_ontology.sql')
def crest_metadata():
  pass

@task
@run_scripts(
  'heron'
  ,'demodata/build_concept_dimension_entries_crest.sql'
  #,'demodata/build_patient_dimension_facts_crest.sql'
  ,'demodata/build_visit_dimension_facts_crest.sql'
)
def crest_dimension():
  pass

@task
@run_scripts('heron', 'demodata/build_observation_facts_crest.sql')
def crest_demodata():
  pass

@task
@needs([
  'bigred.drop_indexes_encounter_mapping'
  ,'bigred.crest_encounter_mapping'
  ,'bigred.build_indexes_encounter_mapping'
  ,'bigred.crest_truncate'
  ,'bigred.crest_metadata'
  ,'bigred.crest_dimension'
  ,'bigred.crest_demodata'
])
def crest_refresh():
  pass






'''ORMANAGER'''
@task
@run_scripts('heron', 'etc/truncate_ormanager_metadata.sql', 'etc/truncate_ormanager_data.sql')
def ormanager_truncate():
  ''' Truncate from table data imported from ORManager '''
  pass

@task
@run_scripts('heron', 'mapping/build_encounter_mapping_ormanager.sql')
def ormanager_encounter_mapping():
  pass

@task
@run_scripts('heron', 'metadata/build_table_access_ormanager.sql', 'metadata/build_ormanager_ontology.sql')
def ormanager_metadata():
  pass

@task
@run_scripts(
  'heron'
  ,'demodata/build_concept_dimension_entries_ormanager.sql'
  ,'demodata/build_modifier_dimension_facts_ormanager.sql'
  ,'demodata/build_visit_dimension_facts_ormanager.sql'
)
def ormanager_dimension():
  pass

@task
@run_scripts('heron', 'demodata/build_observation_facts_age_at_encounter_ormanager.sql', 'demodata/build_observation_facts_ormanager.sql')
def ormanager_demodata():
  pass

@task
@needs([
  'bigred.drop_indexes_encounter_mapping'
  ,'bigred.ormanager_encounter_mapping'
  ,'bigred.build_indexes_encounter_mapping'
  ,'bigred.ormanager_truncate'
  ,'bigred.ormanager_metadata'
  ,'bigred.ormanager_dimension'
  ,'bigred.ormanager_demodata'
])
def ormanager_refresh():
  ''' Populates mapping dimension and fact tables with data from ORManager '''
  pass






'''PROFILER'''
@task
@run_scripts('heron', 'etc/truncate_profiler_metadata.sql', 'etc/truncate_profiler_data.sql')
def profiler_truncate():
  ''' Truncate only specimens data from table '''
  pass

@task
@run_scripts('heron', 'preprocessing/process_specimen_data.sql')
def profiler_preprocess():
  pass

@task
@run_scripts('heron', 'metadata/build_table_access_profiler.sql', 'metadata/build_specimen_ontology.sql')
def profiler_metadata():
  pass

@task
@run_scripts('heron', 'demodata/build_concept_dimension_entries_profiler.sql')
def profiler_dimension():
  pass

@task
@run_scripts('heron', 'demodata/build_observation_facts_specimen.sql')
def profiler_demodata():
  pass

@task
@needs([
  'bigred.profiler_truncate'
  ,'bigred.profiler_preprocess'
  ,'bigred.profiler_metadata'
  ,'bigred.profiler_dimension'
  ,'bigred.profiler_demodata'
])
def profiler_refresh():
  pass





'''REDCAP'''
@task
@run_scripts('heron', 'mapping/build_encounter_mapping_redcap.sql')
def redcap_encounter_mapping():
  pass

@task
@run_scripts('heron', 'etc/truncate_redcap_metadata.sql', 'etc/truncate_redcap_data.sql')
def redcap_truncate():
  ''' Truncate only REDCap data from table '''
  pass

@task
@run_scripts(
  'heron'
  ,'preprocessing/pre-processing_redcap_tables.sql'
  ,'preprocessing/populate_adjusted_redcap_tables.sql'
  ,'index/create_staging_area_indexes_redcap.sql'
  ,'preprocessing/create_custom_split_function.sql'
)
def redcap_preprocessing():
  ''' Refreshes the REDCap tables prior to ETL and cleans them up '''
  pass

@task
@run_scripts('heron', 'metadata/build_table_access_redcap.sql', 'metadata/build_redcap_ontology.sql')
def redcap_metadata():
  pass

@task
@run_scripts('heron', 'demodata/build_concept_dimension_entries_redcap.sql', 'demodata/build_patient_dimension_facts_redcap.sql')
def redcap_dimension():
  pass

@task
@run_scripts('heron', 'demodata/build_observation_facts_redcap.sql')
def redcap_demodata():
  pass

@task
@run_scripts('heron', 'preprocessing/redcap_cleanup.sql')
def redcap_cleanup():
  pass

@task
@needs([
  'bigred.drop_indexes_encounter_mapping'
  ,'bigred.redcap_encounter_mapping'
  ,'bigred.build_indexes_encounter_mapping'
  ,'bigred.redcap_truncate'
  ,'bigred.redcap_preprocessing'
  ,'bigred.redcap_metadata'
  ,'bigred.redcap_dimension'
  ,'bigred.redcap_demodata'
  ,'bigred.redcap_cleanup'
])
def redcap_refresh():
  ''' Imports data from REDCap Case Report Forms into i2b2 in a relational format '''
  pass





'''COMPURECORD'''
@task
@run_scripts('heron', 'mapping/build_encounter_mapping_compurecord.sql')
def compurecord_encounter_mapping():
  pass

@task
@run_scripts('heron', 'etc/truncate_compurecord_metadata.sql', 'etc/truncate_compurecord_data.sql')
def compurecord_truncate():
  ''' Truncate from table data imported from CompuRecord '''
  pass

@task
@run_scripts('heron', 'metadata/build_table_access_compurecord.sql', 'metadata/build_compurecord_ontology.sql')
def compurecord_metadata():
  pass

@task
@run_scripts(
  'heron'
  ,'demodata/build_concept_dimension_entries_compurecord.sql'
  ,'demodata/build_modifier_dimension_facts_compurecord.sql'
  ,'demodata/build_visit_dimension_facts_compurecord.sql'
)
def compurecord_dimension():
  pass

@task
@run_scripts('heron', 'demodata/build_observation_facts_age_at_encounter_compurecord.sql'
                    , 'demodata/build_observation_facts_compurecord.sql'
                    , 'demodata/build_observation_facts_compurecord_vitals.sql')
def compurecord_demodata():
  pass

@task
@needs([
  'bigred.drop_indexes_encounter_mapping'
  ,'bigred.compurecord_encounter_mapping'
  ,'bigred.build_indexes_encounter_mapping'
  ,'bigred.compurecord_truncate'
  ,'bigred.compurecord_metadata'
  ,'bigred.compurecord_dimension'
  ,'bigred.compurecord_demodata'
])
def compurecord_refresh():
  ''' CompuRecord has no patient_dimension entries because all patients in CR also exist in EPIC '''
  pass





'''ECLIPSYS'''
@task
@run_scripts('heron', 'mapping/build_encounter_mapping_eclipsys.sql')
def eclipsys_encounter_mapping():
  pass

@task
@run_scripts('heron', 'etc/truncate_eclipsys_metadata.sql', 'etc/truncate_eclipsys_data.sql')
def eclipsys_truncate():
  ''' Truncate from table data imported from CDW '''
  pass

@task
@run_scripts('heron', 'metadata/build_encounters_ontology_eclipsys.sql')
def eclipsys_metadata():
  pass

@task
@run_scripts('heron', 'demodata/build_concept_dimension_entries_eclipsys.sql', 'demodata/build_visit_dimension_facts_eclipsys.sql')
def eclipsys_dimension():
  pass

@task
@run_scripts(
  'heron'
  ,'demodata/build_observation_facts_age_at_encounter_eclipsys.sql'
  ,'demodata/build_observation_facts_diagnoses_eclipsys.sql'
  ,'demodata/build_observation_facts_medications_eclipsys.sql'
  ,'demodata/build_observation_facts_jupiter_vitals.sql'
)
def eclipsys_demodata():
  pass

@task
@needs([
  'bigred.drop_indexes_encounter_mapping'
  ,'bigred.eclipsys_encounter_mapping'
  ,'bigred.build_indexes_encounter_mapping'
  ,'bigred.eclipsys_truncate'
  ,'bigred.eclipsys_metadata'
  ,'bigred.eclipsys_dimension'
  ,'bigred.eclipsys_demodata'
])
def eclipsys_refresh():
  pass







'''EAGLE'''
@task
@run_scripts('heron', 'mapping/build_encounter_mapping_eagle.sql')
def eagle_encounter_mapping():
  pass

@task
@run_scripts('heron', 'etc/truncate_eagle_metadata.sql', 'etc/truncate_eagle_data.sql')
def eagle_truncate():
  ''' Truncate from table data imported from CDW '''
  pass

@task
@run_scripts(
  'heron'
  ,'metadata/build_icd9cm_ontology.sql'
  ,'metadata/build_icd10cm_ontology.sql'
  ,'metadata/build_encounters_ontology_eagle.sql'
  ,'metadata/build_eagle_admission_status_ontology.sql'
  ,'metadata/build_table_access_eagle.sql'
)
def eagle_metadata():
  pass

@task
@run_scripts('heron', 'demodata/build_concept_dimension_entries_eagle.sql', 'demodata/build_visit_dimension_facts_eagle.sql')
def eagle_dimension():
  pass

@task
@run_scripts(
  'heron'
  
  ,'demodata/build_observation_facts_age_at_encounter_eagle.sql'
  ,'demodata/build_observation_facts_diagnoses_eagle.sql'
  ,'demodata/build_observation_facts_procedures_eagle.sql'
  ,'demodata/build_observation_facts_eagle_admission_status.sql'
)
def eagle_demodata():
  pass

@task
@needs([
  'bigred.drop_indexes_encounter_mapping'
  ,'bigred.eagle_encounter_mapping'
  ,'bigred.build_indexes_encounter_mapping'
  ,'bigred.eagle_truncate'
  ,'bigred.eagle_metadata'
  ,'bigred.eagle_dimension'
  ,'bigred.eagle_demodata'
])
def eagle_refresh():
  pass




'''TUMOR REGISTRY'''
@task
@run_scripts('heron', 'mapping/build_encounter_mapping_tumor_registry.sql')
def tumor_registry_encounter_mapping():
  pass

@task
@run_scripts('heron', 'etc/truncate_mapping_tumor_registry_metadata.sql', 'etc/truncate_mapping_tumor_registry_data.sql')
def tumor_registry_truncate():
  ''' Empties i2b2 tables of tumor registry data'''
  pass

@task
@run_scripts('heron', 'metadata/build_table_access_tumor_registry.sql', 'metadata/build_tumor_registry_ontology.sql')
def tumor_registry_metadata():
  pass

@task
@run_scripts('heron', 'demodata/build_concept_dimension_entries_tumor_registry.sql')
def tumor_registry_dimension():
  pass

@task
@run_scripts('heron', 'demodata/build_observation_facts_tumor_registry.sql')
def tumor_registry_demodata():
  pass

@task
@needs([
  'bigred.drop_indexes_encounter_mapping'
  ,'bigred.tumor_registry_encounter_mapping'
  ,'bigred.build_indexes_encounter_mapping'
  ,'bigred.tumor_registry_truncate'
  ,'bigred.tumor_registry_metadata'
  ,'bigred.tumor_registry_dimension'
  ,'bigred.tumor_registry_demodata'
])
def tumor_registry_refresh():
  ''' Imports data from the Tumor Registry into i2b2 in a relational format '''
  pass




'''Building miscellaneous I2B2 tables and related i2b2 tables.'''
@task
@run_scripts('heron', 'etc/truncate_tables_misc.sql')
def truncate_misc():
    ''' Empties select I2B2 tables while leaving their structure intact. '''
    pass

''' Blacklists '''
@task
@run_scripts('heron', 'index/drop_indexes_blacklist.sql')
def drop_indexes_blacklists():
  pass

@task
@run_scripts('heron', 'etc/truncate_blacklists.sql')
def blacklists_truncate():
  ''' Empties select I2B2 tables while leaving their structure intact. '''
  pass

@task
@needs(['bigred.drop_indexes_blacklists', 'bigred.blacklists_truncate'])
@run_scripts('heron', 'preprocessing/create_blacklists.sql')
def blacklists_refresh():
  pass

'''ETL finalization'''
@task
@run_scripts('heron', 'preprocessing/create_datamart_report.sql')
def create_datamart_report():
  ''' Creates a report on the RDR at the end of the ETL '''
  pass

@task
@run_scripts('heron', 'counting/count_patients_concepts.sql'
                    #, 'counting/count_encounters_concepts.sql'
                    )
def counting():
  pass

'''Index management tasks'''
@task
@needs([
  'bigred.drop_indexes_dimension'
  ,'bigred.drop_indexes_fact'
  ,'bigred.drop_indexes_metadata'
  ,'bigred.build_indexes_dimension'
  ,'bigred.build_indexes_fact'
  ,'bigred.build_indexes_metadata'
])
def refresh_indexes():
  '''Drops then rebuilds indexes for metadata, dimension, and facts'''
  pass