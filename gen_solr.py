from gen import Schema2Doc

activities = Schema2Doc('iati-activities-schema.xsd', lang='en')
# activities.output_docs('iati-activities', 'activity-standard/')
activities.output_solr_order(
    'iati-activities', 'activity-standard/', output=True,
    filename='solr_order.csv'
)
