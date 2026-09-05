"""Application entry point."""
from app import create_app
from app.extensions import db
from app.models.product import Product
from app.models.user import User

app = create_app()

def init_db():
    with app.app_context():
        db.create_all()
        # Seed default products if database is empty
        if Product.query.first() is None:
            products_data = [
                {
                    "name": "Wireless Noise-Canceling Headphones",
                    "description": "Premium over-ear wireless headphones with active noise cancellation and 30-hour battery life.",
                    "category": "Electronics",
                    "stock": 25,
                    "price": 149.99,
                    "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&auto=format&fit=crop&q=60",
                },
                {
                    "name": "Mechanical Gaming Keyboard",
                    "description": "RGB backlit mechanical keyboard with tactile blue switches and durable aluminum frame.",
                    "category": "Electronics",
                    "stock": 15,
                    "price": 89.99,
                    "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=500&auto=format&fit=crop&q=60",
                },
                {
                    "name": "Ergonomic Office Chair",
                    "description": "High-back mesh ergonomic desk chair with lumbar support and adjustable armrests.",
                    "category": "Furniture",
                    "stock": 10,
                    "price": 229.99,
                    "image_url": "https://images.unsplash.com/photo-1505843490538-5133c6c7d0e1?w=500&auto=format&fit=crop&q=60",
                },
                {
                    "name": "Modern Velvet Accent Sofa",
                    "description": "Contemporary 3-seater velvet sofa with plush cushioning and solid wooden legs.",
                    "category": "Furniture",
                    "stock": 8,
                    "price": 499.99,
                    "image_url": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=500&auto=format&fit=crop&q=60",
                },
                {
                    "name": "Minimalist Oak Study Desk",
                    "description": "Solid oak wood study desk with integrated cable management and dual utility drawers.",
                    "category": "Furniture",
                    "stock": 12,
                    "price": 279.99,
                    "image_url": "https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd?w=500&auto=format&fit=crop&q=60",
                },
                {
                    "name": "Industrial Nordic Floor Lamp",
                    "description": "Matte black adjustable standing floor lamp with warm ambient LED bulb included.",
                    "category": "Furniture",
                    "stock": 25,
                    "price": 69.99,
                    "image_url": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=500&auto=format&fit=crop&q=60",
                },
                {
                    "name": "Stainless Steel Water Bottle",
                    "description": "Double-wall vacuum insulated water bottle, keeps drinks cold for 24 hours or hot for 12.",
                    "category": "Lifestyle",
                    "stock": 50,
                    "price": 24.99,
                    "image_url": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500&auto=format&fit=crop&q=60",
                },
                {
                    "name": "Minimalist Leather Backpack",
                    "description": "Water-resistant handcrafted faux leather backpack suitable for 15-inch laptops.",
                    "category": "Accessories",
                    "stock": 20,
                    "price": 79.99,
                    "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500&auto=format&fit=crop&q=60",
                },
                {
                    "name": "Smart Fitness Watch",
                    "description": "Waterproof fitness tracker with heart rate monitor, step counter, and sleep tracking.",
                    "category": "Electronics",
                    "stock": 30,
                    "price": 119.99,
                    "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&auto=format&fit=crop&q=60",
                },
                {
                    "name": "True Wireless ANC Earbuds",
                    "description": "Compact wireless earbuds with active noise canceling and IPX5 water resistance.",
                    "category": "Electronics",
                    "stock": 35,
                    "price": 79.99,
                    "image_url": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=500&auto=format&fit=crop&q=60",
                },
                {
                    "name": "Portable Waterproof Bluetooth Speaker",
                    "description": "360-degree surround sound portable speaker with 16-hour playtime and rugged build.",
                    "category": "Electronics",
                    "stock": 40,
                    "price": 59.99,
                    "image_url": "https://images.unsplash.com/photo-1545454675-3531b543be5d?w=500&auto=format&fit=crop&q=60",
                },
                {
                    "name": "Performance Athletic Running Shoes",
                    "description": "Lightweight breathable mesh athletic sneakers with responsive cushioning soles.",
                    "category": "Lifestyle",
                    "stock": 22,
                    "price": 89.99,
                    "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&auto=format&fit=crop&q=60",
                },
                {
                    "name": "Polarized UV400 Classic Sunglasses",
                    "description": "Retro stylish polarized sunglasses with lightweight acetate frame and 100% UV protection.",
                    "category": "Accessories",
                    "stock": 45,
                    "price": 34.99,
                    "image_url": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=500&auto=format&fit=crop&q=60",
                },
                {
                    "name": "Programmable 12-Cup Drip Coffee Maker",
                    "description": "Stainless steel coffee maker with digital brew-strength selector and 24-hour timer.",
                    "category": "Lifestyle",
                    "stock": 18,
                    "price": 64.99,
                    "image_url": "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=500&auto=format&fit=crop&q=60",
                },
            ]
            for pdata in products_data:
                prod = Product(
                    name=pdata["name"],
                    description=pdata["description"],
                    category=pdata["category"],
                    stock=pdata["stock"],
                    image_url=pdata["image_url"],
                )
                prod.price = pdata["price"]
                db.session.add(prod)
            db.session.commit()

        # Seed default admin user if none exists
        if User.query.filter_by(role="admin").first() is None:
            admin = User(name="Admin User", email="admin@example.com", role="admin")
            admin.set_password("admin123")
            db.session.add(admin)
            db.session.commit()

init_db()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

