# 📅 EMPLOI-DU-TEMPS - Schedule Management System

A modern schedule management application built with Python and PySide6 for educational institutions.

## ✨ Features

- 📊 **Dynamic Dashboard (Admin)** - Real-time statistics on sessions, hours, and groups.
- 📋 **Visual Schedule Management** - Professional table view with color-coding.
- 🏛️ **Reservation System** - Room booking requests for students/teachers with admin approval workflow.
- 🔍 **Smart Filtering** - Filter schedules by group, teacher, or room.
- ⚠️ **Smart Conflict Detection** - Prevents double bookings with detailed error messages.
- � **CSV Export (Admin)** - Export filtered schedules to CSV format for Excel.
- 👥 **Role-Based Access** - Distinct interfaces for Administrators, Teachers, and Students.
- 🎨 **Modern UI** - Clean, intuitive interface with custom styling and animations.
- 🗄️ **Database Persistence** - Integrated with SQLite using SQLAlchemy ORM.

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository** (or download the project)
   ```bash
   cd EMPLOI-DU-TEMPS-projet
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

## 📖 Usage

### User Roles & Login

- **Administrator**: Access to all management tools (Add/Edit/Delete), Dashboard Stats, and CSV Export.
- **Teacher**: View personalized schedule and request room reservations.
- **Student**: View group schedule and request room reservations.

### Key Workflows

1. **Managing Sessions (Admin)**: Use the "Ajouter", "Modifier", or "Supprimer" buttons in the Table view.
2. **Room Booking**: Go to the "Réservations" tab to request a room. Admins can approve or reject these from the same tab.
3. **Filtering**: Use the dropdown menus at the top to narrow down the schedule.
4. **Data Export (Admin)**: Click "Exporter CSV" at the bottom of the table view to save the current filtered view.

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/ -v
```

## 📁 Project Structure

```
EMPLOI-DU-TEMPS-projet/
├── core/              # Domain models (Salle, Matiere, Enseignant, etc.)
├── users/             # Domain user classes (Administrateur, Etudiant, etc.)
├── ui/                # PySide6 interface (Windows, Dialogs, Widgets)
├── database/          # Persistence layer (SQLAlchemy Models, Repositories)
├── services/          # Business logic and algorithms
├── tests/             # Unit and integration tests
├── main.py            # Application entry point
└── requirements.txt   # Project dependencies
```

## 🎨 Design System

### Colors & Styling
The application uses a customized theme based on the PySide6 Fusion style:
- 🔵 **Lectures (cours)** - Professional blue
- � **Tutorials (td)** - Vibrant orange
- 🟢 **Labs (tp)** - Success green

### Conflict Messages
The system provides specific feedback for conflicts:
- *"La salle 'Amphi 101' est déjà occupée."*
- *"L'enseignant 'Dr. Dupont' a déjà un cours sur ce créneau."*

## �️ Built With

- **Python 3.x** - Core language
- **PySide6** - GUI framework (Qt for Python)
- **SQLAlchemy** - Database ORM
- **Bcrypt** - Secure password hashing
- **SQLite** - Local database storage

## 📄 License

This project is for educational purposes as part of an academic schedule management development.

---

**Made with ❤️ using Python and PySide6**
