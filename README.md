# Project: Web Application
Web application created and developed in the Python programming environment using Django as framework.
# Index
- [Description](#description)
- [Project Requirements](#requirements)
- [Tech stack applied](#stack)

## _Description_ <a name="description"></a>
This is my final project for **Tokio Python programming** course: a web application for selling IT supplies. The app has two main parts: an online store for customers to browse and make purchases, 
and an inventory management section for employees and the admin. It meets the basic requirements of the project, but there's room for future improvements and enhancements. 
The goal is to provide a solid starting point for a company specializing in tech supplies, with a user-friendly platform for both customers and the management team
## _Project Requirements_<a name="requirements"></a> 
The app will meet the following requirements:
- The web app will have two types of access: one for customers and another for employees (administrative) who manage inventory.
  - For suppliers, the following contact details will be stored:
    - Supplier name
    - Email
    - Address
    - Contact number
    - Description
  - For customers/employees, the following user details will be stored:
    - Email
    - Username
    - Contact number
    - Password
- All products will have these fields:
  - Category
  - Name
  - Slug
  - Description
  - Selling price
  - Purchase price
  - Real stock (actual quantity of the product in the warehouse)
  - Maximum stock (maximum quantity of the product to be in the warehouse)
  - Supplier
  - Image
  - Active product status
- There will be an inventory of all products with their quantities, so when stock reaches 90%, employees will be notified.  
- Product purchases from suppliers will be managed through purchase invoices.  
- Customers can view their purchase history through a sales (purchase) chart. For admins (administrative) or employees, charts will be created.

## _Tech stack applied_<a name="stack"></a>
- Programming Language:
  - Python
- Development Framework:
  - Django (version 4.2.6): A high-level web framework for Python.
- Database:
  - SQLite
- Frontend:
  - HTML5, CSS3, JavaScript, jQuery, Jinja2
  - Bootstrap: A design framework for layout and styling.
- Dependency Management:
  - Pip (Python)
  - asgiref==3.7.2
  - certifi==2023.7.22
  - charset-normalizer==3.3.0
  - crispy-bootstrap4==2023.1
  - django-countries==7.5.1
  - django-crispy-forms==2.1
  - django-extensions==3.2.3
  - django-js-asset==2.1.0
  - django-mptt==0.15.0
  - django-pandas==0.6.6
  - idna==3.4
  - numpy==1.26.2
  - packaging==23.2
  - pandas==2.1.3
  - Pillow==10.0.1
  - plotly==5.18.0
  - pydot==1.4.2
  - pyparsing==3.1.1
  - python-dateutil==2.8.2
  - pytz==2023.3.post1
  - requests==2.31.0
  - six==1.16.0
  - sqlparse==0.4.4
  - stripe==6.7.0
  - tenacity==8.2.3
  - typing-extensions==4.8.0
  - tzdata==2023.3
  - urllib3==2.0.6
- Development Tools:
  - Visual Studio Code
- Virtual Environment (for development):
  - virtualenv: Creates Python virtual environments.
- Payment Services:
  - Stripe (version 6.7.0)
