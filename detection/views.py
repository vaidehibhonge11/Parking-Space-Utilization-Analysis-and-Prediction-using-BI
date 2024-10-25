import easyocr
from django.shortcuts import render
from .models import DetectedVehicle, StudentDetails, VehicleHourlyStats
from datetime import datetime  # Import the `datetime` class directly from `datetime` module
from django.db.models import F
import joblib

# Function to detect number plate
def detect_number_plate(image_path):
    reader = easyocr.Reader(['en'])
    results = reader.readtext(image_path, detail=0)
    return results[0] if results else None

# Function to update vehicle statistics
def update_vehicle_stats():
    """Updates hourly vehicle stats in the VehicleHourlyStats model"""
    current_time = datetime.now()  # Use `datetime.now()` from the `datetime` module
    current_hour = current_time.hour
    current_date = current_time.date()

    # Get the current hour stats or create a new entry
    vehicle_stat, created = VehicleHourlyStats.objects.get_or_create(
        date=current_date, hour=current_hour,
        defaults={'vehicle_count': 0}
    )

    # Increment the vehicle count for this hour
    vehicle_stat.vehicle_count = F('vehicle_count') + 1
    vehicle_stat.save()

    # Reload the object from the database to ensure F expression is resolved
    vehicle_stat.refresh_from_db()

# Load the trained model for peak hour prediction
model = joblib.load('peak_hour_predictor.pkl')

# Function to predict peak hour vehicle count
def predict_peak_hour():
    """Predict the vehicle count for the current hour."""
    current_time = datetime.now()  # Use `datetime.now()`
    current_hour = current_time.hour
    current_weekday = current_time.weekday()

    # Prepare features
    X_pred = [[current_hour, current_weekday]]
    
    # Make a prediction
    predicted_vehicle_count = model.predict(X_pred)
    
    return predicted_vehicle_count[0]

# Function to handle image upload and process it
def upload_image(request):
    if request.method == 'POST':
        image = request.FILES['vehicle_image']
        with open('uploaded_image.jpg', 'wb+') as f:
            for chunk in image.chunks():
                f.write(chunk)

        # Detect the number plate
        detected_plate = detect_number_plate('uploaded_image.jpg')
        if detected_plate:
            DetectedVehicle.objects.create(number_plate=detected_plate)
            update_vehicle_stats()  # Update hourly stats
            
            # Find the student related to this number plate
            student = StudentDetails.objects.filter(number_plate=detected_plate).first()
            predicted_vehicle_count = predict_peak_hour()
            return render(request, 'student_details.html', {'student': student, 'predicted_vehicle_count': predicted_vehicle_count})

    return render(request, 'upload.html')
