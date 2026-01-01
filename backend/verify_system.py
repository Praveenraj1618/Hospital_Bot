"""
Comprehensive system verification script
Checks database, schema, API endpoints, and key functionality
"""
import sys
import requests
from sqlalchemy import inspect, text
from app.database import engine, SessionLocal
from app.models import Doctor, Specialization, Patient, Appointment, Admin

def check_database_connection():
    """Check if database connection works"""
    print("1. Checking database connection...")
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("   [OK] Database connection successful")
        return True
    except Exception as e:
        print(f"   [ERROR] Database connection failed: {e}")
        return False

def check_table_exists():
    """Check if all required tables exist"""
    print("\n2. Checking database tables...")
    inspector = inspect(engine)
    required_tables = ['doctors', 'specializations', 'patients', 'appointments', 'admins', 'banners']
    existing_tables = inspector.get_table_names()
    
    all_exist = True
    for table in required_tables:
        if table in existing_tables:
            print(f"   [OK] Table '{table}' exists")
        else:
            print(f"   [ERROR] Table '{table}' missing")
            all_exist = False
    
    return all_exist

def check_doctors_schema():
    """Check doctors table schema changes"""
    print("\n3. Checking doctors table schema...")
    inspector = inspect(engine)
    
    try:
        columns = {col['name']: col for col in inspector.get_columns('doctors')}
        
        # Check email is nullable
        if columns.get('email', {}).get('nullable', False):
            print("   [OK] Email column is nullable (optional)")
        else:
            print("   [WARNING] Email column is NOT NULL (should be nullable)")
        
        # Check qualification is NOT NULL
        if not columns.get('qualification', {}).get('nullable', True):
            print("   [OK] Qualification column is NOT NULL (required)")
        else:
            print("   [WARNING] Qualification column is nullable (should be required)")
        
        # Check name and specialization are required
        if not columns.get('name', {}).get('nullable', True):
            print("   [OK] Name column is NOT NULL (required)")
        else:
            print("   [WARNING] Name column is nullable (should be required)")
        
        if not columns.get('specialization', {}).get('nullable', True):
            print("   [OK] Specialization column is NOT NULL (required)")
        else:
            print("   [WARNING] Specialization column is nullable (should be required)")
        
        return True
    except Exception as e:
        print(f"   [ERROR] Failed to check schema: {e}")
        return False

def check_backend_api(base_url="http://localhost:8000"):
    """Check if backend API is running"""
    print("\n4. Checking backend API...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("   [OK] Backend API is running")
            return True
        else:
            print(f"   [WARNING] Backend responded with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   [WARNING] Backend API is not running (start with: uvicorn main:app --reload)")
        return False
    except Exception as e:
        print(f"   [ERROR] Failed to check API: {e}")
        return False

def check_api_endpoints(base_url="http://localhost:8000"):
    """Check key API endpoints"""
    print("\n5. Checking API endpoints...")
    endpoints = [
        ("/", "Root endpoint"),
        ("/health", "Health check"),
        ("/api/admin/stats", "Admin stats (requires auth)"),
        ("/api/specializations/active", "Active specializations"),
        ("/api/doctors", "Doctors list"),
    ]
    
    results = []
    for endpoint, description in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code in [200, 401]:  # 401 is OK for protected endpoints
                print(f"   [OK] {description}: {response.status_code}")
                results.append(True)
            else:
                print(f"   [WARNING] {description}: {response.status_code}")
                results.append(False)
        except requests.exceptions.ConnectionError:
            print(f"   [SKIP] {description}: Backend not running")
            results.append(False)
        except Exception as e:
            print(f"   [ERROR] {description}: {e}")
            results.append(False)
    
    return any(results)  # At least some endpoints work

def check_sample_data():
    """Check if there's any sample data"""
    print("\n6. Checking sample data...")
    db = SessionLocal()
    try:
        doctor_count = db.query(Doctor).count()
        spec_count = db.query(Specialization).count()
        patient_count = db.query(Patient).count()
        appointment_count = db.query(Appointment).count()
        admin_count = db.query(Admin).count()
        
        print(f"   Doctors: {doctor_count}")
        print(f"   Specializations: {spec_count}")
        print(f"   Patients: {patient_count}")
        print(f"   Appointments: {appointment_count}")
        print(f"   Admins: {admin_count}")
        
        if admin_count == 0:
            print("   [WARNING] No admin users found. Run setup_db.py to create default admin.")
        
        return True
    except Exception as e:
        print(f"   [ERROR] Failed to check data: {e}")
        return False
    finally:
        db.close()

def check_doctor_validation():
    """Test doctor creation validation"""
    print("\n7. Testing doctor validation...")
    db = SessionLocal()
    try:
        # Check if we can query doctors
        doctors = db.query(Doctor).limit(1).all()
        print("   [OK] Can query doctors table")
        
        # Check if any doctors have NULL qualification (shouldn't happen after migration)
        null_qual = db.query(Doctor).filter(
            (Doctor.qualification == None) | (Doctor.qualification == "")
        ).count()
        
        if null_qual == 0:
            print("   [OK] All doctors have qualifications")
        else:
            print(f"   [WARNING] {null_qual} doctors have NULL/empty qualification")
        
        return True
    except Exception as e:
        print(f"   [ERROR] Validation check failed: {e}")
        return False
    finally:
        db.close()

def main():
    """Run all checks"""
    print("=" * 60)
    print("Hospital Management System - Comprehensive Verification")
    print("=" * 60)
    
    results = []
    
    # Database checks
    results.append(check_database_connection())
    results.append(check_table_exists())
    results.append(check_doctors_schema())
    
    # API checks
    results.append(check_backend_api())
    results.append(check_api_endpoints())
    
    # Data checks
    results.append(check_sample_data())
    results.append(check_doctor_validation())
    
    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Passed: {passed}/{total} checks")
    
    if passed == total:
        print("\n[SUCCESS] All checks passed! System is ready.")
    elif passed >= total * 0.7:
        print("\n[WARNING] Most checks passed, but some issues found.")
        print("Review the warnings above.")
    else:
        print("\n[ERROR] Multiple issues found. Please review the errors above.")
    
    print("\nNext steps:")
    print("1. If backend is not running: cd backend && uvicorn main:app --reload")
    print("2. If no admin exists: cd backend && python setup_db.py")
    print("3. Start frontend: cd frontend && npm run dev")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

