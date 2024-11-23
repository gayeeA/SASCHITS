# SASCHITS - Chit Fund Management System

SASCHITS is a web-based application designed to manage and streamline chit fund operations. Built using Django, this application allows administrators to handle subscribers, chit groups, and payments efficiently.

## Features

- **Chit Group Management**: Create, edit, and manage chit groups.
- **Subscriber Management**: Add and maintain subscriber records.
- **Payment Management**: Track payments with details like cheque information and payment status.
- **Dashboard**: Visual overview of current chit fund operations.
- **Custom Templates**: Provides dynamic templates for managing subscribers, payments, and chit groups.

## Installation

To run the SASCHITS project locally, follow these steps:

### Prerequisites

- Python 3.8 or above
- Django 3.2 or later

### Steps

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd chit_fund_project

2. **Install Dependencies**
  ```bash
      pip install -r requirements.txt
      Apply Migrations
```
   ```bash
python manage.py makemigrations
python manage.py migrate
Run the Development Server
```

```bash
python manage.py runserver
```
Visit http://127.0.0.1:8000/ in your browser to access the application.

## Usage
- Login: Access the admin panel to manage chit fund operations.
- Create Chit Groups: Use the dashboard to create new chit groups.
- Add Subscribers: Add subscribers to a specific chit group.
- Manage Payments: Record and update payment statuses.

### File Structure
- chit_fund_app/: Contains the core application logic, including models, views, and templates.
- templates/: Includes HTML templates for rendering pages like subscriber lists and payment forms.
- migrations/: Tracks database schema changes.


### License
This project is licensed under the MIT License.

### Contact
For inquiries or support, contact the maintainer at gayathriande20@gmail.com.

Let me know if you'd like to refine or customize this further!
