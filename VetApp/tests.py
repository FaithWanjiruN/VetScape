from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Clinic

class AdminPanelTestCase(TestCase):

    def setUp(self):
        # Create an admin user for testing
        self.admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'password123')
        self.client.login(username='admin', password='password123')

    def test_admin_can_add_clinic(self):
        # Get the URL for adding a new clinic
        url = reverse('admin:VetApp_clinic_add')  # Replace with your actual admin URL name
        
        # Simulate submitting the form to add a new clinic
        response = self.client.post(url, {
            'name': 'Happy Paws Clinic',
            'location': 'Westlands',
            'address': '1234 Dog St, Animal City',
            'latitude': 1.2921,
            'longitude': 36.8219
        })
        
        # Verify the response and check that the clinic was added
        self.assertEqual(response.status_code, 302)  # Check for redirect after successful save
        self.assertTrue(Clinic.objects.filter(name='Happy Paws Clinic').exists())  # Ensure the clinic is in the database

    def test_admin_cannot_add_clinic_with_missing_fields(self):
        # Get the URL for adding a new clinic
        url = reverse('admin:VetApp_clinic_add')  # Replace with your actual admin URL name
        
        # Simulate submitting the form with missing required fields (e.g., no 'name')
        response = self.client.post(url, {
            'location': 'Westlands',
            'address': '1234 Dog St, Animal City',
            'latitude': 1.2921,
            'longitude': 36.8219
        })
        
        # Ensure the form is rendered again with errors (status code should be 200, indicating the page was re-rendered)
        self.assertEqual(response.status_code, 200)
        
        # Verify the error message appears in the HTML for the 'name' field
        self.assertContains(response, 'This field is required.', html=True)

    def test_admin_can_update_clinic(self):
        # Create a clinic in the database
        clinic = Clinic.objects.create(
            name='Old Clinic',
            location='Kasarani',
            address='Old Address',
            latitude=1.2921,
            longitude=36.8219
        )
        
        # Get the URL for editing the clinic
        url = reverse('admin:VetApp_clinic_change', args=[clinic.id])  # Replace with your actual admin URL name
        
        # Simulate submitting the form to update the clinic
        response = self.client.post(url, {
            'name': 'Updated Clinic',
            'location': 'Langata',
            'address': 'Updated Address',
            'latitude': 1.3031,
            'longitude': 36.8255
        })
        
       

    
# import time
# from django.test import TestCase
# from django.urls import reverse
# from django.contrib.auth.models import User

# class PerformanceTestCase(TestCase):

#     def setUp(self):
#         # Create an admin user for testing
#         self.admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'password123')
#         self.client.login(username='admin', password='password123')

#     def test_homepage_load_time(self):
#         # Measure the response time when navigating to the homepage
#         start_time = time.time()
#         response = self.client.get(reverse('home'))  # Replace with the actual URL name for homepage
#         load_time = time.time() - start_time
#         self.assertLess(load_time, 2, f"Homepage took {load_time} seconds to load, which is too slow.")  # Assert page loads in under 2 seconds

#     def test_adopt_page_load_time(self):
#         # Measure the response time when navigating to the 'Adopt' page
#         start_time = time.time()
#         response = self.client.get(reverse('adopt'))  # Replace with the actual URL name for the adopt page
#         load_time = time.time() - start_time
#         self.assertLess(load_time, 3, f"'Adopt' page took {load_time} seconds to load, which is too slow.")  # Assert page loads in under 3 seconds

#     def test_clinic_list_page_load_time(self):
#         # Measure the response time when navigating to the clinic list page
#         start_time = time.time()
#         response = self.client.get(reverse('clinic_list'))  # Replace with actual URL for clinic list
#         load_time = time.time() - start_time
#         self.assertLess(load_time, 3, f"Clinic List page took {load_time} seconds to load, which is too slow.")  # Assert page loads in under 3 seconds

#     def test_rapid_button_click_navigation(self):
#         # Simulate rapid clicks and ensure smooth navigation without layout issues
#         start_time = time.time()
        
#         # Click 'Home' button (replace with actual URL)
#         self.client.get(reverse('home'))
        
#         # Click 'Adopt' button (replace with actual URL)
#         self.client.get(reverse('adopt'))
        
#         # Click 'Clinics & Vet Centers' (replace with actual URL)
#         self.client.get(reverse('clinic_list'))
        
#         load_time = time.time() - start_time
#         # Ensure total navigation doesn't take too long
#         self.assertLess(load_time, 5, f"Rapid navigation took {load_time} seconds, which is too slow.")

#     def test_adoption_list_load_time_with_large_data(self):
#         # Simulate the performance with a large set of adoption listings (simulate loading large data)
#         # You might need to add a large number of `Adoption` objects to the database for this test
#         start_time = time.time()
#         response = self.client.get(reverse('adopt'))  # Replace with actual adoption listings URL
#         load_time = time.time() - start_time
#         self.assertLess(load_time, 3, f"Adoption List page took {load_time} seconds to load with large data, which is too slow.")



# # from django.test import TestCase
# # from django.urls import reverse
# # from django.contrib.auth.models import User
# # from django.http import HttpResponse
# # from .models import Clinic

# # class AdoptionProcessTestCase(TestCase):

# #     def setUp(self):
# #         # Create an admin user and log in
# #         self.admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'password123')
# #         self.client.login(username='admin', password='password123')

# #     def test_view_adoption_listings(self):
# #         # Test if the user can view the adoption listings
# #         response = self.client.get(reverse('index'))  # Replace with your adoption listings URL
        
# #         # Check if the response status is 200 (OK)
# #         self.assertEqual(response.status_code, 200)
# #         # Check if the listings are in the context
# #         self.assertContains(response, 'Scout')  # Check if a specific dog name is present

# #     def test_adopt_dog_form_submission(self):
# #         # Test if the form can be submitted successfully with valid data
# #         response = self.client.post(reverse('adopt_submit'), {
# #             'first_name': 'John',
# #             'last_name': 'Doe',
# #             'address': '123 Main St',
# #             'city': 'Animal City',
# #             'phone': '123-456-7890',
# #             'email': 'john.doe@example.com',
# #             'housing_type': 'House',
# #             'adoption_reason': 'Companion for self',
# #             'pet_id': '12345',
# #             'breed': 'Siberian Husky',
# #             'age': '3 years',
# #         })
        
# #         # Check that the form was submitted and the response was a redirect (indicating successful submission)
# #         self.assertEqual(response.status_code, 302)  # Redirect after successful form submission
# #         self.assertRedirects(response, reverse('adopt_thank_you'))  # Replace with the actual redirect URL after submission

# #     def test_incomplete_adoption_form(self):
# #         # Test that incomplete form submissions trigger validation errors
# #         response = self.client.post(reverse('adopt_submit'), {
# #             'first_name': 'John',
# #             'last_name': 'Doe',
# #             'address': '',  # Leave the address empty to simulate incomplete form
# #             'city': 'Animal City',
# #             'phone': '123-456-7890',
# #             'email': 'john.doe@example.com',
# #             'housing_type': 'House',
# #             'adoption_reason': 'Companion for self',
# #             'pet_id': '12345',
# #             'breed': 'Siberian Husky',
# #             'age': '3 years',
# #         })
        
# #         # Check that the form was not submitted and validation errors are returned
# #         self.assertEqual(response.status_code, 200)  # Stay on the same page
# #         self.assertFormError(response, 'form', 'address', 'This field is required.')

# #     def test_adoption_redirect_after_successful_submission(self):
# #         # Test that after successful submission, user is redirected to the thank-you page
# #         response = self.client.post(reverse('adopt_submit'), {
# #             'first_name': 'John',
# #             'last_name': 'Doe',
# #             'address': '123 Main St',
# #             'city': 'Animal City',
# #             'phone': '123-456-7890',
# #             'email': 'john.doe@example.com',
# #             'housing_type': 'House',
# #             'adoption_reason': 'Companion for self',
# #             'pet_id': '12345',
# #             'breed': 'Siberian Husky',
# #             'age': '3 years',
# #         })
        
# #         # Check if the user is redirected to the success page after submission
# #         self.assertRedirects(response, reverse('adopt_thank_you'))  # Replace with your thank you page URL

