{
    'name': 'HR Hospital',
    'version': '1.1',
    'category': 'Human Resources',
    'depends': ["base", ],
    'description': """
    Hospital HR Management Module
    """,
    'data': [
        "security/ir.model.access.csv",

        "views/hospital_patient_view.xml",
        "views/hospital_doctor_view.xml",
        "views/hospital_diagnosis_view.xml",
        "views/hospital_disease_directory_view.xml",
        "views/hospital_lab_test_view.xml",
        "views/hospital_research_category_view.xml",
        "views/hospital_schedule_view.xml",
        "views/hospital_visit_view.xml",
        "views/menu_items.xml",

        "data/doctor_speciality_data.xml",
        "data/disease_directory_data.xml",
        "data/sample_type_data.xml",
        "data/research_category_data.xml",
        "data/simptom_data.xml",

        "demo/contact_person_demo.xml",
        "demo/patient_demo.xml",
        "demo/doctor_demo.xml",

        "wizard/reassign_doctor_wizard_view.xml",

        "report/visit_report_template.xml",
        "report/visit_report.xml",
    ],
    'controllers': [
        'controllers/main.py',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
