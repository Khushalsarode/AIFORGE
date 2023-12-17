Certainly! Here's a comprehensive README.md file for your project:

---

# AIForge - All In Open Source

AIForge is a platform that facilitates the discovery and sharing of free and open-source AI tools contributed by the community. It includes features for tool submission, approval, and exploration.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Home Page](#home-page)
  - [Add Tool Page](#add-tool-page)
  - [Admin Panel](#admin-panel)
  - [Show Tool Card](#show-tool-card)
- [Contributing](#contributing)
- [License](#license)

## Introduction

AIForge, also known as "All In Open Source," is a platform designed to centralize AI tools, making it easy for users to discover and share open-source tools within the community. The platform includes a home page, an admin panel for tool approval, a tool submission page, and a tool display page.

## Features

- **Home Page:**
  - Overview of the platform's purpose.
  - Welcome message and a brief description of the community.
  - Display key metrics such as total tools available, total categories, and total user contributions.

- **Add Tool Page:**
  - Allows users to contribute their AI tools to the platform.
  - Form for tool submission, including fields for tool icon, name, description, website link, and user email.
  - Validation checks for input fields.
  - Display of warnings for any incomplete or invalid information.

- **Admin Panel:**
  - A secure login system for administrators.
  - Tool approval or rejection functionality.
  - Display of tool submissions for review.
  - Ability to refresh the admin panel.

- **Show Tool Card:**
  - Search functionality for tools based on name or keywords.
  - Display of tool cards with information such as tool name, description, website link, and keywords.

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Python
- MongoDB
- Redis
- Streamlit
- TryCourier (for email notifications)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/AIForge.git
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure the platform by updating the `config.ini` file with MongoDB and Redis connection details.

## Usage

### Home Page

Run the following command to start the home page:

```bash
streamlit run home.py
```

Access the platform at [http://localhost:8501](http://localhost:8501).

### Add Tool Page

Run the following command to start the add tool page:

```bash
streamlit run add_tool.py
```

Access the tool submission page at [http://localhost:8501](http://localhost:8501).

### Admin Panel

Run the following command to start the admin panel:

```bash
streamlit run adminpanel.py
```

Access the admin panel at [http://localhost:8501](http://localhost:8501).

### Show Tool Card

Run the following command to start the show tool card page:

```bash
streamlit run show_tool.py
```

Access the tool card page at [http://localhost:8501](http://localhost:8501).

## Contributing

Feel free to contribute to the project by following our [contribution guidelines](CONTRIBUTING.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
