from django.db import migrations

def populate_doctors(apps, schema_editor):
    Doctor = apps.get_model('map_app', 'Doctor')
    doctors = [
        {
            "name": "Sarah Jenkins",
            "specialty": "Pediatrician",
            "clinic_name": "SF Kids Clinic",
            "address": "1500 Owens St, San Francisco, CA 94158",
            "latitude": 37.768688,
            "longitude": -122.392067,
            "phone_number": "415-555-0101",
            "email": "dr.sarah@sfkids.com",
            "rating": 4.80,
            "website": "https://www.sfkidsclinic.example.com"
        },
        {
            "name": "Robert Chen",
            "specialty": "Cardiologist",
            "clinic_name": "Pacific Cardiovascular Group",
            "address": "2100 Webster St #310, San Francisco, CA 94115",
            "latitude": 37.790518,
            "longitude": -122.431238,
            "phone_number": "415-555-0102",
            "email": "robert.chen@pacificcardio.example.com",
            "rating": 4.90,
            "website": "https://www.pacificcardio.example.com"
        },
        {
            "name": "Emily Rodriguez",
            "specialty": "Dermatologist",
            "clinic_name": "Golden Gate Dermatology",
            "address": "450 Sutter St #1800, San Francisco, CA 94108",
            "latitude": 37.789524,
            "longitude": -122.408226,
            "phone_number": "415-555-0103",
            "email": "emily@goldengatederm.example.com",
            "rating": 4.70,
            "website": "https://www.goldengatederm.example.com"
        },
        {
            "name": "Michael Patel",
            "specialty": "Orthopedist",
            "clinic_name": "SF Joint & Spine Center",
            "address": "2299 Post St, San Francisco, CA 94115",
            "latitude": 37.785361,
            "longitude": -122.437299,
            "phone_number": "415-555-0104",
            "email": "mpatel@sfjointspine.example.com",
            "rating": 4.60,
            "website": "https://www.sfjointspine.example.com"
        },
        {
            "name": "Alice Wong",
            "specialty": "Neurologist",
            "clinic_name": "Bay Area Neurology Associates",
            "address": "450 Stanyan St, San Francisco, CA 94117",
            "latitude": 37.771144,
            "longitude": -122.454238,
            "phone_number": "415-555-0105",
            "email": "alice.wong@bayneurology.example.com",
            "rating": 4.90,
            "website": "https://www.bayneurology.example.com"
        },
        {
            "name": "David Miller",
            "specialty": "General Practitioner",
            "clinic_name": "Mission Family Practice",
            "address": "2480 Mission St, San Francisco, CA 94110",
            "latitude": 37.755474,
            "longitude": -122.418471,
            "phone_number": "415-555-0106",
            "email": "dmiller@missionfamily.example.com",
            "rating": 4.50,
            "website": "https://www.missionfamily.example.com"
        },
        {
            "name": "Lisa Vance",
            "specialty": "Dentist",
            "clinic_name": "Presidio Dental Design",
            "address": "3236 Geary Blvd, San Francisco, CA 94118",
            "latitude": 37.781682,
            "longitude": -122.454483,
            "phone_number": "415-555-0107",
            "email": "lvance@presidiodental.example.com",
            "rating": 4.80,
            "website": "https://www.presidiodental.example.com"
        },
        {
            "name": "James Carter",
            "specialty": "Ophthalmologist",
            "clinic_name": "Eye Care SF",
            "address": "1100 Van Ness Ave, San Francisco, CA 94109",
            "latitude": 37.785934,
            "longitude": -122.421714,
            "phone_number": "415-555-0108",
            "email": "jcarter@eyecaresf.example.com",
            "rating": 4.70,
            "website": "https://www.eyecaresf.example.com"
        }
    ]
    for d in doctors:
        Doctor.objects.create(**d)

def remove_doctors(apps, schema_editor):
    Doctor = apps.get_model('map_app', 'Doctor')
    Doctor.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('map_app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_doctors, remove_doctors),
    ]
