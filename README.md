# FOODPyramid API

A RESTful API for managing a food delivery platform that connects chefs, kitchens, dishes, and clients. Built with Flask, MongoDB, and Flask-RESTful.

## 🍽️ Features

- **Chef Management**: Create, read, update, and delete chef profiles
- **Kitchen Management**: Manage kitchen information with head chef assignments
- **Dish Management**: Handle dish listings with pricing and kitchen associations
- **Client Management**: Manage client accounts and preferences
- **Favorites System**: Allow clients to save favorite dishes
- **Image Support**: Static image serving for chef, kitchen, and dish photos
- **CORS Enabled**: Cross-origin resource sharing for frontend integration

## 🏗️ Architecture

The API follows a RESTful architecture with the following data models:

- **Chef**: Professional chefs with name, description, and profile image
- **Kitchen**: Restaurant kitchens with name, description, image, and head chef
- **Dish**: Menu items with name, price, description, image, and kitchen association
- **Client**: Customer accounts with favorites management

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- MongoDB instance
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd FOODPyramid_API
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirments.txt
   ```

3. **Environment Setup**
   Create a `.env` file in the root directory:
   ```env
   MONGO_URI=mongodb://localhost:27017/foodpyramid
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

## 📚 API Endpoints

### Chefs
- `GET /chefs` - Get all chefs
- `GET /chefs/<chef_id>` - Get specific chef
- `POST /chefs` - Create new chef
- `PUT /chefs/<chef_id>` - Update chef
- `DELETE /chefs/<chef_id>` - Delete chef

### Kitchens
- `GET /kitchens` - Get all kitchens
- `GET /kitchens/<kitchen_id>` - Get specific kitchen
- `POST /kitchens` - Create new kitchen
- `PUT /kitchens/<kitchen_id>` - Update kitchen
- `DELETE /kitchens/<kitchen_id>` - Delete kitchen

### Dishes
- `GET /dishes` - Get all dishes
- `GET /dishes/<dish_id>` - Get specific dish
- `POST /dishes` - Create new dish
- `PUT /dishes/<dish_id>` - Update dish
- `DELETE /dishes/<dish_id>` - Delete dish

### Clients
- `GET /clients` - Get all clients
- `GET /clients/<client_id>` - Get specific client
- `POST /clients` - Create new client
- `PUT /clients/<client_id>` - Update client
- `DELETE /clients/<client_id>` - Delete client

### Client Favorites
- `GET /clients/<client_id>/favorites/` - Get client's favorite dishes
- `POST /clients/<client_id>/favorites/<dish_id>` - Add dish to favorites
- `DELETE /clients/<client_id>/favorites/<dish_id>` - Remove dish from favorites

### Kitchen Dishes
- `GET /kitchens/<kitchen_id>/dishes` - Get all dishes from a specific kitchen

## 🗄️ Database Schema

### Chef
```json
{
  "id": "string",
  "name": "string (required, max 80 chars)",
  "desc": "string",
  "image": "string"
}
```

### Kitchen
```json
{
  "id": "string",
  "name": "string (required, max 80 chars)",
  "desc": "string",
  "image": "string",
  "headchef": "Chef reference (required)"
}
```

### Dish
```json
{
  "id": "string",
  "name": "string (required, max 80 chars)",
  "price": "float (required, 2 decimal precision)",
  "desc": "string",
  "image": "string",
  "kitchen": "Kitchen reference (required)"
}
```

### Client
```json
{
  "id": "string",
  "name": "string (required, max 80 chars)",
  "email": "string (required, unique)",
  "favorites": ["Dish references"]
}
```

## 🖼️ Static Assets

Images are served from the `static/images/` directory and can be accessed via:
- Chef images: `/static/images/chef_image.jpg`
- Kitchen images: `/static/images/kitchen_image.jpg`
- Dish images: `/static/images/dish_image.jpg`

## 🛠️ Technologies Used

- **Flask**: Web framework
- **Flask-RESTful**: REST API framework
- **MongoEngine**: MongoDB ODM
- **Flask-CORS**: Cross-origin resource sharing
- **Python-dotenv**: Environment variable management

## 📁 Project Structure

```
FOODPyramid_API/
├── app.py                 # Main application entry point
├── db.py                  # Database configuration
├── requirments.txt        # Python dependencies
├── models/                # Data models
│   ├── Chef.py
│   ├── Client.py
│   ├── Dish.py
│   └── Kitchen.py
├── resources/             # API resources/endpoints
│   ├── Chef.py
│   ├── Client.py
│   ├── ClientFavoritesResource.py
│   ├── Dish.py
│   ├── Kitchen.py
│   └── KitchenDishesResource.py
└── static/                # Static assets
    └── images/            # Image files
```

## 🔧 Development

To run in development mode:
```bash
python app.py
```

The application runs in debug mode by default, which enables:
- Auto-reload on code changes
- Detailed error messages
- Debug console

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For questions or support, please open an issue in the repository. 