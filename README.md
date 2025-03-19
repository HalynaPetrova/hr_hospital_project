# Hospital Management System

This project is based on Odoo 17. It covers the key operations of a hospital, such as patient management, doctor schedules, appointment bookings, lab test assignments, and diagnosis.

## Patient
1. Inherits from the abstract Person model.
2. Each patient has a personal medical record with:
   - Personal information and a photo
   - Profile of the personal doctor
   - Active appointment records
   - Detailed information on all visits to doctors
   - Assigned tests and their results
3. It includes a wizard for mass reassigning the personal doctor.

## Doctor
1. Inherits from the abstract Person model.
2. Each doctor has their own page with:
   - Personal information and a photo
   - Doctor's schedule
   - A list of all patients they work with
   - Active appointment records
3. If the "Intern" field is active, an intern doctor must be assigned a mentor doctor.
  
## Doctor's Schedule
1. Allows selecting a doctor, patient, date, and time for the visit (only during the doctor's working hours).
2. Each patient can create only one appointment for a specific date and time.
3. Appointments with the statuses "Cancelled" and "Completed" cannot be modified.
4. From the appointment page, a corresponding "Visit" to the doctor can be created.
5. It has a cron job that automatically changes the visit status to "Completed" when the visit time expires.

## Visit
1. A visit page can only be created from the corresponding appointment in the schedule.
2. It contains all necessary visit information, including details about the doctor and patient, and the patient's complaints.
3. If the attending doctor is an intern, their mentor must add their comments on the diagnosis and recommendations.
4. On the visit page, you can assign tests, a follow-up visit, or set a diagnosis.
5. Selecting the corresponding options changes the visit status, which is displayed in the status bar.
6. It has the ability to print a detailed PDF report for each visit.

## Diseases
A hierarchical catalog of diseases used for diagnosis.

## Laboratory Tests
A hierarchical catalog of laboratory tests.

## Project pictures

![image](https://github.com/user-attachments/assets/98a11362-d7e0-48b5-bed2-937f9ac2664a)
![image](https://github.com/user-attachments/assets/fb70fa53-99ff-4671-923f-dca827eec16c)
![image](https://github.com/user-attachments/assets/6ad0b481-1d3f-4224-bced-b484eba784ad)
![image](https://github.com/user-attachments/assets/980461a4-8d43-4f89-97ef-929d126033b2)
![image](https://github.com/user-attachments/assets/16853b62-3ae7-4ad0-b524-99903c6dd01c)
![image](https://github.com/user-attachments/assets/9f1b3601-c1f3-45f9-adee-6705f1f06b62)
![image](https://github.com/user-attachments/assets/58d54a5b-084a-4996-b19a-04446c601778)
![image](https://github.com/user-attachments/assets/6c04c018-a9a6-4d83-a060-a75bdc97b03c)
![image](https://github.com/user-attachments/assets/a060008a-77a6-4795-a38b-6de1e02dc4fc)
![image](https://github.com/user-attachments/assets/235afd2c-cb2a-421d-b2c9-217d56ed73ff)







