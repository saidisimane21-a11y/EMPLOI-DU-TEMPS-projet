# 📅 EMPLOI-DU-TEMPS - Schedule Management System

A modern schedule management application built with Python and PySide6 for educational institutions.

## ✨ Features

- 📊 **Visual Schedule Management** - Table and calendar views
- 🔍 **Smart Filtering** - Filter by group, teacher, or room
- ⚠️ **Conflict Detection** - Automatic scheduling conflict detection
- 📁 **CSV Export** - Export schedules to CSV format
- 👥 **User Roles** - Administrator, Teacher, and Student roles
- 🎨 **Modern UI** - Clean, intuitive interface with custom styling
- 🤖 **Auto-Scheduling** - Greedy algorithm for automatic schedule generation

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

### Running the Application

The application will launch with demo data pre-loaded. You'll see:

- **Main Window** with schedule display
- **Filter Options** (Group, Teacher, Room)
- **Action Buttons** (Add, Edit, Delete sessions)
- **Export** functionality
- **les accounts**
 - **admin**
      nom d'utilisateur : admin
      Password: admin123
 - **Prof**
      Nom d'utilisateur : prof
      Mot de passe: prof123
 - **Etudiant**
      Nom d'utilisateur : etudiant
      Mot de passe : etudiant123

### User Roles
- **Administrator** - Full access to manage schedules, add/edit/delete sessions
- **Teacher** - View own schedule and availability
- **Student** - View group schedule

### Managing Sessions

1. **Add Session**: Click "Ajouter Séance" button
2. **Edit Session**: Select a session and click "Modifier"
3. **Delete Session**: Select a session and click "Supprimer"
4. **Export**: Click "Exporter CSV" to save schedule

## 🧪 Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=core --cov=services --cov=ui
```

## 📁 Project Structure

```
EMPLOI-DU-TEMPS-projet/
├── core/              # Domain models (Salle, Matiere, Enseignant, etc.)
├── users/             # User management (Administrateur, Etudiant, etc.)
├── ui/                # PySide6 interface components
├── services/          # Business logic (Scheduler, ConflictDetector)
├── data/              # Test data generators
├── tests/             # Unit tests
├── main.py            # Application entry point
└── requirements.txt   # Python dependencies
```

## 🔧 Configuration

### Demo Data

The application includes test data in `data/testDatat.py`. To customize:

- Edit room definitions in `generer_salles()`
- Modify courses in `generer_matieres()`
- Update teacher data in `generer_enseignants()`

### Database (Coming Soon)

Database persistence is currently in development. For now, data is stored in memory.

## 🎨 Customization

### Themes

The application uses PySide6's Fusion style. To change:

```python
# In main.py
app.setStyle("Windows")  # or "Fusion", "WindowsVista", etc.
```

### Colors

Session cards are color-coded by course type:
- 🔵 **Blue** - Lectures (cours)
- 🟠 **Orange** - Tutorial sessions (td)
- 🟢 **Green** - Practical sessions (tp)

Edit in `ui/widgets.py` → `SeanceCard._apply_style()`

## 🛠️ Development

### Adding New Features

1. **Domain Models** → Add to `core/`
2. **UI Components** → Add to `ui/`
3. **Business Logic** → Add to `services/`
4. **Tests** → Add to `tests/`

### Code Style

- Follow PEP 8 guidelines
- Use type hints where possible
- Add docstrings for classes and methods

## 📝 Known Issues

- Database persistence not yet implemented
- Login screen in development
- Reservation approval workflow pending

## 🗺️ Roadmap

- [ ] Database integration with SQLAlchemy
- [ ] Login/authentication system
- [ ] Reservation management UI
- [ ] PDF export functionality
- [ ] Multi-semester planning
- [ ] iCalendar export

## 👥 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is for educational purposes.

## 🆘 Support

For issues or questions, please create an issue in the repository.

## 👨‍💻 Authors

Developed as part of an academic project for schedule management.

---

**Made with ❤️ using Python and PySide6**
