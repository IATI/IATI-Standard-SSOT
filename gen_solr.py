from gen import Schema2Doc

activities = Schema2Doc('iati-activities-schema.xsd', lang='en')
activities.output_solr(
    'iati-activities', 'activity-standard/', minOccurs='1', maxOccurs='1', output=True,
    filename='solr_schema.xml', out_type='schema'
)
