# AI Medical Support

AI Medical Support is a web application that helps users predict diseases based on symptoms and search for medicines in an extensive Indian medicine database.

## Features

- Disease Prediction: Enter symptoms to get AI-powered disease predictions
- Medicine Search: Search through a comprehensive database of Indian medicines
- Detailed Medicine Information: Get information about medicine prices, manufacturers, uses, side effects, and substitutes
- Dark Mode: Comfortable viewing experience with dark mode support
- Responsive Design: Works seamlessly on desktop and mobile devices

## Technologies Used

- Python 3.x
- Flask
- Bootstrap 5
- SQLite
- HTML/CSS/JavaScript

## Installation

1. Clone the repository:
```bash
git clone https://github.com/meanujraj/ai_medical_support.git
cd ai_medical_support
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Download required data files:
```bash
# Download the data files from GitHub Releases
# Visit: https://github.com/meanujraj/ai_medical_support/releases
# Download the ai_medical_support_data.zip file from the latest release
```

5. Extract and place the data files:
```bash
# Extract the downloaded zip file
# Place medicine.csv in the root directory
# Place svc.pkl in the models directory
# Place the datasets folder contents in your local datasets directory
```

6. Run the application:
```bash
python main.py
```

7. Open your browser and navigate to:
```
http://127.0.0.1:5000/
```

## Features

### Disease Prediction
- Enter symptoms separated by commas
- Get AI-powered disease predictions
- View precautions and recommendations

### Medicine Search
- Search for medicines by name
- View detailed information including:
  - Price
  - Manufacturer
  - Type
  - Uses
  - Side effects
  - Substitutes

### User Interface
- Clean and intuitive design
- Dark mode support
- Responsive layout
- Real-time search suggestions

## Project Structure

```
ai_medical_support/
├── static/
│   ├── css/
│   │   ├── style.css
│   │   └── toggle.css
│   └── js/
│       └── toggle.js
├── templates/
│   ├── index.html
│   ├── medicine_search.html
│   ├── about.html
│   ├── blog.html
│   ├── contact.html
│   └── policies.html
├── datasets/
│   ├── symptom_Description.csv
│   ├── symptom_precaution.csv
│   └── Training.csv
├── models/
│   └── svc.pkl
├── main.py
├── medicine.csv
└── requirements.txt
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

- Email: anujraj1875@gmail.com
- LinkedIn: [meanujraj](https://linkedin.com/in/meanujraj)
- GitHub: [meanujraj](https://github.com/meanujraj)
- X (Twitter): [@meanujraj](https://x.com/meanujraj)
- Instagram: [@meanujraj](https://instagram.com/meanujraj) 